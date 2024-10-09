from web3 import Web3
import click
import requests
from utils import load_abi, fetch_creation_code, compute_create2_address, has_code_at_address, emojify, deploy_create_x, generate_salt
import tqdm
import os
from dotenv import load_dotenv
import json
from constants import ADDRESS_PROVIDER, BLOCKSCOUT_API_BASE, CREATE_X_ADDRESS, NETWORKS
from addresses import V3_PROTOCOL_ADDRESSES
from eth_account import Account

load_dotenv()

web3 = None
address_provider = None
rpc = os.getenv('ETH_RPC')
ZERO_ADDRESS = '0x' + '0' * 40
CREATE_X = None
contract_data = {}
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
            get_wallet_info(web3, True)
            deploy_choice = click.confirm(
                f"Would you like to deploy the V3 protocol to {chain_name} (Chain ID: {chain_id})?",
                default=False
            )
            
            if deploy_choice:
                print(f"Initiating deployment process for {chain_name}...")
                info = V3_PROTOCOL_ADDRESSES['init_gov']
                salt = info['salt_preimage']
                address = info['address']
                creation_code = fetch_creation_code(address)
                computed_address = compute_create2_address(web3, CREATE_X_ADDRESS, info['salt'], creation_code)
                if has_code_at_address(web3, computed_address):
                    print(f'Init Gov alrady deployed at {computed_address}!')
                else:
                    deploy_create_x(web3, CREATE_X, creation_code, salt)

                # Deploy Address Provider
                info = V3_PROTOCOL_ADDRESSES['address_provider']
                salt = info['salt_preimage']
                address = info['address']
                creation_code = fetch_creation_code(address)
                computed_address = compute_create2_address(web3, CREATE_X_ADDRESS, info['salt'], creation_code)
                if has_code_at_address(web3, computed_address):
                    print(f'Address Provider already deployed at {computed_address}!')
                else:
                    deploy_create_x(web3, CREATE_X, creation_code, salt)
            
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
    contract_data.clear()  # Clear existing data
    protocol_deployed = True
    for key, info in tqdm.tqdm(V3_PROTOCOL_ADDRESSES.items(), desc="Loading Yearn V3 Protocol data"):
        if key in ['init_gov', 'address_provider']:
            if has_code_at_address(web3, info['address']):
                continue
            protocol_deployed = False
            break # exit, and return false to indicate that the protocol is not deployed
        id = web3.keccak(text=info['id'])
        address = info['address']
        try:
            address_from_provider = address_provider.functions.getAddress(id).call()
        except Exception as e:
            print(f"Error fetching address from provider: {str(e)}")
            address_from_provider = None
        if key == 'vault_factory':
            if has_code_at_address(web3, V3_PROTOCOL_ADDRESSES['release_registry']['address']):
                release_registry = web3.eth.contract(address=V3_PROTOCOL_ADDRESSES['release_registry']['address'], abi=load_abi('ReleaseRegistry'))
                address_from_provider = release_registry.functions.latestFactory().call()
            else:
                contract_data[key] = {
                    'address': address,
                    'deployed': emojify(False),
                    'is_set': emojify(False),
                    'computed_address': ZERO_ADDRESS
                }
                continue
        is_set_emoji = emojify(address_from_provider == address)
        if key in ['tokenized_strategy', 'vault_implementation']:
            is_set_emoji = '⚠️'
        deployed = has_code_at_address(web3, address)
        computed_address = None
        if address and not deployed:
            computed_address = compute_create2_address(web3, CREATE_X_ADDRESS, 0 if not info['salt'] else info['salt'], fetch_creation_code(address))
            deployed = has_code_at_address(web3, computed_address)
        deployed = emojify(deployed)
        contract_data[key] = {
            'key': key,
            'address': address,
            'deployed': deployed,
            'is_set': is_set_emoji,
            'computed_address': computed_address
        }

    if not protocol_deployed:
        click.echo(click.style(f'\nError: V3 Protocol not deployed on {NETWORKS[chain_id]["name"]} chain id {chain_id}\n', fg='red', bold=True))
        click.echo(click.style(f'Returning to chain selection...'))
        return protocol_deployed
    
    while True:
        print(f"\033[1m{'Contract':<24} | {'Address':<42} | {'Deployed':<8} | {'Addr Provider Set':<16}\033[0m")
        print("-" * 94)  # Separator line
        for i, (key, data) in enumerate(contract_data.items(), 1):
            address = data['address']
            deployed = data['deployed']
            is_set_emoji = data['is_set']
            computed_address = data['computed_address']
            print(f"{i}. \033[1m{key:<24}\033[0m | {color_address(True, ZERO_ADDRESS if not address else address)} | {deployed}\033[0m | {is_set_emoji}\033[0m")
        
        print("\nEnter the number of the contract you want to interact with, or '0' to quit:")
        choice = click.prompt("Your choice", type=int)
        
        if choice == 0:
            break
        
        index = choice - 1
        if 0 <= index < len(contract_data):
            selected_contract = list(contract_data.values())[index]
            interact_with_contract(selected_contract)
        else:
            print("Invalid selection. Please try again.")

    return protocol_deployed

def interact_with_contract(selected_contract):
    key = selected_contract['key']  # Get the key (contract name)
    data = contract_data[key]  # Get the data dictionary
    global_data = V3_PROTOCOL_ADDRESSES[key]
    print(f"\nYou selected: {key}")
    print(f"Mainnet address: {global_data['address']}")
    if data['computed_address']:
        has_code = has_code_at_address(web3, data['computed_address'])
        print(f"Computed deploy address: {data['computed_address']} | {'Already deployed!' if has_code else 'Not yet deployed'} {emojify(has_code)}")
    else:
        print(f"Deployed: {data['deployed']}")
    print(f"Address Provider Set: {data['is_set']}")
    
    # Add more interactive options here
    print("\nWhat would you like to do?")
    print("1. Deploy")
    print("2. Go Back")
    
    action = click.prompt("Your choice", type=int)
    
    if action == 1:
        info = V3_PROTOCOL_ADDRESSES[key]
        creation_code = fetch_creation_code(data['address'])
        
        account, wallet_address, balance_eth = get_wallet_info(web3)
        if not account:
            return

        # Check if balance is zero
        if balance_eth == 0:
            print("\033[91mError: Your wallet balance is 0 ETH. Please add funds to your wallet before proceeding.\033[0m")
            print("Returning to previous screen...")
            return

        # Ask for confirmation
        confirm = click.confirm("Do you want to proceed with the deployment?", default=False)

        if confirm:
            print(f'Deploying {key} with CREATEX...')
            deploy_create_x(web3, CREATE_X, creation_code, info['salt_preimage'])
        else:
            print("Deployment cancelled.")

    elif action == 2:
        return
    else:
        print("Invalid choice. Returning to main menu.")

def get_wallet_info(web3, should_print=True):
    private_key = os.getenv('DEPLOYER_PRIVATE_KEY')
    if not private_key:
        print("Error: DEPLOYER_PRIVATE_KEY not found in .env file.")
        return None, None, None

    account = Account.from_key(private_key)
    wallet_address = account.address
    balance = web3.eth.get_balance(wallet_address)
    balance_eth = web3.from_wei(balance, 'ether')
    if should_print:
        print(f"\nWallet Address: {wallet_address}")
        print(f"Balance: {balance_eth:.4f} ETH")
    return account, wallet_address, balance_eth

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