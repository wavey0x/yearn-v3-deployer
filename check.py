from web3 import Web3
import click
import requests
from utils import load_abi, fetch_creation_code, has_code_at_address, emojify, deploy_create_x, generate_salt
import tqdm
import os
from dotenv import load_dotenv
import json
from constants import ADDRESS_PROVIDER, BLOCKSCOUT_API_BASE, CREATE_X_ADDRESS, NETWORKS
from addresses import V3_PROTOCOL_ADDRESSES


load_dotenv()

web3 = None
address_provider = None
rpc = os.getenv('ETH_RPC')
ZERO_ADDRESS = '0x' + '0' * 40
CREATE_X = None

latest_release = None



@click.group()
def cli():
    pass

@cli.command()
def check():
    global web3
    while web3 is None:
        web3 = handle_rpc(rpc)

    load_create_x()

    while True:
        # Present network options to the user
        print("\nSelect a network:")
        print(f"{'ID':<8} {'Network':<20}")
        print("-" * 28)
        print(f"{'0':<8} {'🌐 Custom RPC':<20}")
        for chain_id, info in NETWORKS.items():
            print(f"{chain_id:<8} {info['name']:<20}")
        
        choice = click.prompt("\nEnter the chain ID or '0' for Custom RPC", type=int)
        
        if choice == 0:
            custom_rpc = click.prompt("Enter custom RPC URL")
            web3 = handle_rpc(custom_rpc)
            chain_id = web3.eth.chain_id
        else:
            chain_id = choice
            if chain_id in NETWORKS:
                web3 = handle_rpc(NETWORKS[chain_id]['rpc'])
            else:
                print(f"Chain ID {chain_id} not found in known networks. Please try again.")
                continue
        
        if print_chain_deployment_report():
            break
        else:
            # Ask if the user wants to deploy the V3 protocol
            chain_name = NETWORKS[chain_id]['name']
            deploy_choice = click.confirm(
                f"Would you like to deploy the V3 protocol to {chain_name} (Chain ID: {chain_id})?",
                default=False
            )
            
            if deploy_choice:
                print(f"Initiating deployment process for {chain_name}...")
                address = contract_data['init_gov']['address']
                salt = contract_data['address_provider']['salt_preimage']
                creation_code = fetch_creation_code(address)
                deploy_create_x(web3, CREATE_X, creation_code, salt)
            else:
                print("Deployment cancelled. Returning to chain selection...")
            
            # Whether the user chose to deploy or not, we'll break the loop to re-run the chain selection
            break

    load_create_x()
    # load_address_provider_data()


def color_address(is_true, value):
    color = "\033[92m" if is_true else "\033[93m"
    return f"{color}{value}\033[0m"


def print_chain_deployment_report():
    global address_provider, contract_data, latest_release
    chain_id = web3.eth.chain_id
    address_provider = web3.eth.contract(address=ADDRESS_PROVIDER, abi=load_abi('AddressProvider'))
    print("-" * 94)  # Separator line
    contracts = []
    protocol_deployed = True
    for key, info in tqdm.tqdm(V3_PROTOCOL_ADDRESSES.items(), desc="Loading Yearn V3 Protocol data"):
        if key == 'address_provider':
            if has_code_at_address(web3, info['address']):
                continue
            protocol_deployed = False
            return protocol_deployed
        id = web3.keccak(text=info['id'])
        address = info['address']
        try:
            address_from_provider = address_provider.functions.getAddress(id).call()
        except Exception as e:
            print(f"Error fetching address from provider: {str(e)}")
            address_from_provider = None
        if key == 'vault_factory':
            release_registry = web3.eth.contract(address=V3_PROTOCOL_ADDRESSES['release_registry']['address'], abi=load_abi('ReleaseRegistry'))
            address_from_provider = release_registry.functions.latestFactory().call()
        is_set_emoji = emojify(address_from_provider == address)
        if key in ['tokenized_strategy', 'vault_implementation']:
            is_set_emoji = '⚠️'
        deployed = has_code_at_address(web3, address)
        computed_address = None
        if address and not deployed: # It is possible that 
            computed_address = compute_create2_address(CREATE_X_ADDRESS, info['salt'], fetch_creation_code(address))
            deployed = has_code_at_address(web3, computed_address)
        deployed = emojify(deployed)
        contracts.append((key, address, deployed, is_set_emoji, computed_address))
    
    if not protocol_deployed:
        click.echo(click.style(f'\nError: V3 Protocol not deployed on {NETWORKS[chain_id]["name"]} chain id {chain_id}\n', fg='red', bold=True))
        click.echo(click.style(f'Returning to chain selection...'))
        return protocol_deployed
    
    while True:
        print(f"\033[1m{'Contract':<24} | {'Address':<42} | {'Deployed':<8} | {'Addr Provider Set':<16}\033[0m")
        print("-" * 94)  # Separator line
        for i, (key, address, deployed, is_set_emoji, computed_address) in enumerate(contracts, 1):
            print(f"{i}. \033[1m{key:<24}\033[0m | {color_address(address and (not computed_address or computed_address == address), ZERO_ADDRESS if not address else address)} | {deployed}\033[0m | {is_set_emoji}\033[0m")
        
        print("\nEnter the number of the contract you want to interact with, or '0' to quit:")
        choice = click.prompt("Your choice", type=int)
        
        if choice == 0:
            break
        
        index = choice - 1
        if 0 <= index < len(contracts):
            selected_contract = contracts[index]
            interact_with_contract(selected_contract)
        else:
            print("Invalid selection. Please try again.")

    return protocol_deployed

def interact_with_contract(contract):
    key, address, deployed, is_set_emoji, computed_address = contract
    print(f"\nYou selected: {key}")
    print(f"Mainnet address: {address}")
    if computed_address:
        has_code = has_code_at_address(web3, computed_address)
        print(f"Computed deploy address: {computed_address} | {'Already deployed!' if has_code else 'Not yet deployed'} {emojify(has_code_at_address(web3, computed_address))}")
    else:
        print(f"Deployed: {deployed}")
    print(f"Address Provider Set: {is_set_emoji}")
    
    # Add more interactive options here
    print("\nWhat would you like to do?")
    print("1. Deploy")
    print("2. Go Back")
    
    action = click.prompt("Your choice", type=int)
    
    if action == 1:
        info = V3_PROTOCOL_ADDRESSES[key]
        creation_code = fetch_creation_code(address)
        print(f'Deploying {key} with CREATEX...')
        deploy_create_x(web3, CREATE_X, creation_code, info['salt'])

    elif action == 2:
        return
    else:
        print("Invalid choice. Returning to main menu.")


def load_address_provider_data():
    global address_provider, contract_data, latest_release
    address_provider = web3.eth.contract(address=ADDRESS_PROVIDER, abi=load_abi('AddressProvider'))
    for key, info in tqdm.tqdm(V3_PROTOCOL_ADDRESSES.items(), desc="Loading Yearn V3 Protocol data"):
        id = web3.keccak(text=info['id'])
        address = info['address']
        provider_address = address_provider.functions.getAddress(id).call()
        has_code = has_code_at_address(web3, address)
        if not has_code: # It is possible that 
            computed_address = compute_create2_address(address, info['salt'], fetch_creation_code(address))
            print(f'Computed Address: {computed_address} | Salt {info["salt"]}')
            has_code = has_code_at_address(web3, computed_address)
        
        print(f"\033[1m{key:<22}\033[0m | \033[94m{address:<42}\033[0m | {emojify(has_code)} | {emojify(provider_address == address)}")
        # contract_data[key]['address'] = address
    #     if address != ZERO_ADDRESS:
    #         creation_code = fetch_creation_code(address)
    #         if creation_code:
    #             contract_data[key]['creation_bytecode'] = creation_code
        

    # release_registry = web3.eth.contract(address=contract_data['release_registry']['address'], abi=load_abi('ReleaseRegistry'))
    # latest_factory = release_registry.functions.latestFactory().call()
    # contract_data['vault_factory']['address'] = latest_factory
    # contract_data['vault_factory']['creation_bytecode'] = fetch_creation_code(latest_factory)
    # latest_release = release_registry.functions.latestRelease().call()

    # for key, string in ADDRESS_PROVIDER_IDS.items():
    #     if key in ADDRESS_PROVIDER_DEPLOY_DATA:
    #         salt = ADDRESS_PROVIDER_DEPLOY_DATA[key]['salt']
    #         contract_data[key]['salt'] = salt
    #         contract_data[key]['deployer'] = ADDRESS_PROVIDER_DEPLOY_DATA[key]['deployer']
    # save_contract_data(contract_data)

def compute_create2(contract_data):
    for key in contract_data:
        if (
            contract_data[key].get('deployer', '') == '' or
            contract_data[key].get('creation_bytecode', '') == '' or
            contract_data[key]['address'] == ZERO_ADDRESS
        ):
            continue
        address, cx_address = compute_create2_address(contract_data[key]['deployer'], contract_data[key]['salt'], contract_data[key]['creation_bytecode'])
        # print(f'Compare: {contract_data[key]["address"]} {address} {cx_address}')


def compute_create2_address(factory, salt, creation_code):
    global CREATE_X
    if isinstance(salt, int):
        salt = salt.to_bytes(32, byteorder='big')
    elif isinstance(salt, str):
        salt = web3.to_bytes(hexstr=salt)
    elif isinstance(salt, bytes):
        salt = salt.rjust(32, b'\0')
    else:
        raise ValueError("Salt must be either an integer, a hexadecimal string, or bytes")

    init_code_hash = web3.keccak(hexstr=creation_code)
    # address = CREATE_X.functions.computeCreate2Address(salt, init_code_hash, factory).call()

    # Compute CREATE2 address
    address = web3.to_checksum_address(
        web3.keccak(
            b'\xff' +
            web3.to_bytes(hexstr=factory) +
            salt +
            init_code_hash
        )[12:]
    )
    
    return address

def handle_rpc(_rpc=None):
    global web3
    while not _rpc or _rpc is None:
        print("No RPC URL provided.")
        rpc = click.prompt('Please provide an RPC URL', type=int)

    web3 = Web3(Web3.HTTPProvider(_rpc))

    while not web3.is_connected():
        print("Failed to connect to the provided RPC URL.")
        _rpc = click.prompt('Please provide a valid RPC URL')
        web3 = Web3(Web3.HTTPProvider(_rpc))

    print(f"Connected to chain ID {web3.eth.chain_id} | {_rpc}")
    return web3

def load_create_x():
    global CREATE_X
    CREATE_X = web3.eth.contract(address=CREATE_X_ADDRESS, abi=load_abi('CreateX'))

    
if __name__ == "__main__":
    cli()