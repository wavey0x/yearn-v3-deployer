from web3 import Web3
import click
import requests
from utils import load_abi, fetch_creation_code, has_code_at_address, emojify
import tqdm
import os
from dotenv import load_dotenv
import json
from constants import ADDRESS_PROVIDER, BLOCKSCOUT_API_BASE, CREATE_X_ADDRESS, NETWORKS
from addresses import V3_PROTOCOL_ADDRESSES
from web3.datastructures import AttributeDict
from hexbytes import HexBytes

load_dotenv()

web3 = None
address_provider = None
rpc = os.getenv('ETH_RPC')
ZERO_ADDRESS = '0x' + '0' * 40
CREATE_X = None

latest_release = None
contract_data = {
    'accountant_factory': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'registry_factory': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'vault_factory': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'splitter_factory': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'tokenized_strategy': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'release_registry': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'base_fee_provider': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'apr_oracle': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'common_report_trigger': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'keeper': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'role_manager_factory': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'allocator_factory': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'registry_factory': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''},
    'router': {'id': '', 'creation_bytecode': '', 'address': '', 'salt': ''}
}



@click.group()
def cli():
    pass

@cli.command()
def check():
    global web3, contract_data
    while web3 is None:
        web3 = handle_rpc(rpc)

    load_create_x()

    
        

    # compute_create2(contract_data)


    for chain_id, _rpc in RPCS.items():
        web3 = handle_rpc(_rpc)
        print_chain_deployment_report()





def print_chain_deployment_report():
    global address_provider, contract_data, latest_release
    address_provider = web3.eth.contract(address=ADDRESS_PROVIDER, abi=load_abi('AddressProvider'))
    print("-" * 94)  # Separator line
    contracts = []
    for key, info in V3_PROTOCOL_ADDRESSES.items():
        id = web3.keccak(text=info['id'])
        address = info['address']
        provider_address = address_provider.functions.getAddress(id).call()
        if key == 'vault_factory':
            release_registry = web3.eth.contract(address=V3_PROTOCOL_ADDRESSES['release_registry']['address'], abi=load_abi('ReleaseRegistry'))
            provider_address = release_registry.functions.latestFactory().call()
        is_set_emoji = emojify(provider_address == address)
        if key == 'tokenized_strategy':
            is_set_emoji = '⚠️'
        deployed = emojify(has_code_at_address(web3, address))
        contracts.append((key, address, deployed, is_set_emoji))
    
    while True:
        print(f"\033[1m{'Contract':<24} | {'Address':<42} | {'Deployed':<8} | {'Addr Provider Set':<16}\033[0m")
        print("-" * 94)  # Separator line
        for i, (key, address, deployed, is_set_emoji) in enumerate(contracts, 1):
            print(f"{i}. \033[1m{key:<24}\033[0m | \033[94m{address:<42}\033[0m | {deployed} | {is_set_emoji}")
        
        print("\nEnter the number of the contract you want to interact with, or 'q' to quit:")
        choice = click.prompt("Your choice", type=str)
        
        if choice.lower() == 'q':
            break
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(contracts):
                selected_contract = contracts[index]
                interact_with_contract(selected_contract)
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

def interact_with_contract(contract):
    key, address, deployed, is_set_emoji = contract
    print(f"\nYou selected: {key}")
    print(f"Address: {address}")
    print(f"Deployed: {deployed}")
    print(f"Address Provider Set: {is_set_emoji}")
    
    # Add more interactive options here
    print("\nWhat would you like to do?")
    print("1. Deploy")
    print("2. Go Back")
    
    action = click.prompt("Your choice", type=int)
    
    if action == 1:
        deploy(address)
    elif action == 2:
        return
    else:
        print("Invalid choice. Returning to main menu.")

def deploy():
    pass

def load_address_provider_data():
    global address_provider, contract_data, latest_release
    address_provider = web3.eth.contract(address=ADDRESS_PROVIDER, abi=load_abi('AddressProvider'))
    for key, info in tqdm.tqdm(V3_PROTOCOL_ADDRESSES.items(), desc="Loading Yearn V3 Protocol data"):
        id = web3.keccak(text=info['id'])
        address = info['address']
        provider_address = address_provider.functions.getAddress(id).call()
        print(f"\033[1m{key:<22}\033[0m | \033[94m{address:<42}\033[0m | {emojify(has_code_at_address(web3, address))} | {emojify(provider_address == address)}")
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
    create_x = CREATE_X.functions.computeCreate2Address(salt, init_code_hash, factory).call()
    # Compute init_code_hash
    
    
    # Compute CREATE2 address
    address = Web3.to_checksum_address(
        web3.keccak(
            b'\xff' +
            Web3.to_bytes(hexstr=factory) +
            salt +
            init_code_hash
        )[12:]
    )
    
    return address, create_x

def handle_rpc(_rpc=None):
    global web3
    while not _rpc or _rpc is None:
        print("No RPC URL provided.")
        rpc = click.prompt('Please provide an RPC URL')

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

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        if isinstance(obj, AttributeDict):
            return dict(obj)
        return super().default(obj)

def save_contract_data(data):
    """Save the contract_data dictionary to a JSON file."""
    try:
        with open('cached_data.json', 'w') as f:
            json.dump(data, f, indent=4, cls=CustomJSONEncoder)
        print("Contract data successfully saved to cached_data.json")
    except Exception as e:
        print(f"Error saving contract data: {e}")

def load_data():
    """Read the cached data from JSON file and return it as a dictionary."""
    try:
        with open('cached_data.json', 'r') as f:
            loaded_data = json.load(f)
        print("Contract data successfully loaded from cached_data.json")
        return loaded_data
    except FileNotFoundError:
        print("cached_data.json not found. No data loaded.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON from cached_data.json. No data loaded.")
        return {}
    except Exception as e:
        print(f"Error loading contract data: {e}")
        return {}
    
if __name__ == "__main__":
    cli()