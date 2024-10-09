from web3 import Web3
from eth_abi import encode
import hashlib
import json
import os
import requests
from hexbytes import HexBytes
from constants import BLOCKSCOUT_API_BASE
from web3.datastructures import AttributeDict
from dotenv import load_dotenv
import os
import time
import sys

load_dotenv()

def compute_create2_address(web3,factory, salt, creation_code):
    global CREATE_X
    if isinstance(salt, int):
        if salt.bit_length() > 256:
            raise ValueError("Salt integer must be 32 bytes or less")
        salt = salt.to_bytes(32, byteorder='big')
    elif isinstance(salt, str):
        print(f"Salt: {salt}")
        if len(salt) != 64 and len(salt) != 66: # Account for 0x chars
            raise ValueError("Salt hex string must be 32 bytes (64 characters) long")
        salt = salt[2:] if salt.startswith('0x') else salt
        # Convert hex string to bytes
        salt = bytes.fromhex(salt)

    init_code_hash = web3.keccak(hexstr=creation_code)

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

def deploy_create_x(web3, create_x, creation_code, salt):
    # Validate salt
    if isinstance(salt, int):
        if salt.bit_length() > 256:
            raise ValueError("Salt integer must be 32 bytes or less")
        salt = salt.to_bytes(32, byteorder='big')
    elif isinstance(salt, str):
        if len(salt) != 64 and len(salt) != 66: # Account for 0x chars
            raise ValueError("Salt hex string must be 32 bytes (64 characters) long")
    # Load private key from .env file
    private_key = os.getenv('DEPLOYER_PRIVATE_KEY')
    if not private_key:
        raise ValueError("Private key not found in .env file")

    # Get the account from the private key
    deployment_address = compute_create2_address(web3, create_x.address, web3.keccak(hexstr=salt).hex(), creation_code)
    if has_code_at_address(web3, deployment_address):
        print(f"Contract already deployed at {deployment_address}. Exiting.")
        return deployment_address
    account = web3.eth.account.from_key(private_key)
    print(f"Account address: {account.address}")

    priority_fee = int(1e5)
    max_fee_per_gas = web3.eth.gas_price
    # Build the transaction

    transaction = create_x.functions.deployCreate2(salt, creation_code).build_transaction({
        'from': account.address,
        'gas': 20000000,  # Adjust gas limit as needed
        'maxFeePerGas': max_fee_per_gas,
        'maxPriorityFeePerGas': priority_fee,
        'nonce': web3.eth.get_transaction_count(account.address),
        'chainId': web3.eth.chain_id
    })

    # Sign the transaction
    signed_txn = account.sign_transaction(transaction)

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f'Sending txn: 0x{tx_hash.hex()}')
        
        # Wait for the transaction receipt with a loading animation and timeout
        print("Waiting for transaction to be mined", end="")
        spinner = "|/-\\"
        idx = 0
        start_time = time.time()
        while True:
            if time.time() - start_time > 100:  # 100 seconds timeout
                print("\nTransaction mining timed out after 100 seconds.")
                return None
            try:
                tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
                if tx_receipt is not None:
                    break
            except Exception:
                pass
            sys.stdout.write(f"\rWaiting for transaction to be mined {spinner[idx % len(spinner)]}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)
        
    except Exception as e:
        print(f"\nError processing transaction: {str(e)}")
        return None

    # Process all events in the receipt
    print(f"\nDeployed at: \033[92m{deployment_address}\033[0m\n")
    return deployment_address

def get_creation_code(contract_address):
    url = f"https://eth.blockscout.com/api/v2/smart-contracts/{contract_address}"
    response = requests.get(url)
    data = response.json()
    creation_code = data.get('creation_code', '')
    return creation_code

def has_code_at_address(web3, deployment_address):
    """Check if the contract is already deployed by checking if code exists at the address."""
    if not web3.is_address(deployment_address):
        return False
    code = web3.eth.get_code(deployment_address)
    return code != b''

def emojify(some_bool):
    return "✅" if some_bool else "❌"

def generate_salt(salt_string):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    # Update the hash object with the string data
    hash_object.update(salt_string.encode("utf-8"))
    # Get the hexadecimal representation of the hash
    hex_hash = hash_object.hexdigest()
    # Convert the hexadecimal hash to an integer
    salt = int(hex_hash, 16)
    return salt


    
def extract_constructor_args(abi):
    constructor = next((item for item in abi if item['type'] == 'constructor'), None)
    if not constructor:
        return {}  # No constructor, return an empty dict
    
    abi_args = constructor['inputs']
    constructor_args = {arg['name']: arg['type'] for arg in abi_args}
    return constructor_args

def load_abi(contract_name):
    abi_path = os.path.join('abis', f'{contract_name}.json')
    with open(abi_path, 'r') as abi_file:
        return json.load(abi_file)
    return None

def get_contract_bytecode(contract_address, api_key):
    """
    Retrieves the contract creation bytecode from Etherscan for a given contract address.
    :param contract_address: The Ethereum contract address.
    :param api_key: Your Etherscan API key.
    :return: The contract bytecode or an error message.
    """
    from dotenv import load_dotenv
    load_dotenv()
    url = "https://api.etherscan.io/api"
    params = {
        "module": "proxy",
        "action": "eth_getCode",
        "address": contract_address,
        "tag": "latest",  # Use 'latest' to get the most recent bytecode
        "apikey": os.getenv('ETHERSCAN_KEY')
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Check if the response contains the bytecode
        if data["status"] == "1" and "result" in data:
            bytecode = data["result"]
            print(f"Bytecode for contract at {contract_address}:")
            print(bytecode)
            return bytecode
        else:
            error_message = data.get("message", "Unknown error")
            print(f"Error fetching bytecode: {error_message}")
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")

    return None

def fetch_creation_code(address):
    url = f'{BLOCKSCOUT_API_BASE}{address}'
    response = requests.get(url)
    success = response.status_code == 200
    if not success:
        print(f'API request to get creation code for {address} failed with status code {response.status_code}')
        return None
    if 'creation_bytecode' not in response.json():
        print(f'No creation bytecode found for {address}')
        raise Exception(f'No creation bytecode found via API for {address} | {url}')
    creation_code = response.json()['creation_bytecode']
    if not creation_code or creation_code == '0x':
        print(f'Creation code for {address} is empty')
        return None
    return creation_code

def save_file(data):
    """Save the contract_data dictionary to a JSON file."""
    try:
        with open('cached_data.json', 'w') as f:
            json.dump(data, f, indent=4, cls=CustomJSONEncoder)
        print("Contract data successfully saved to cached_data.json")
    except Exception as e:
        print(f"Error saving contract data: {e}")

def load_file(file_name):
    """Read the cached data from JSON file and return it as a dictionary."""
    try:
        with open(file_name, 'r') as f:
            loaded_data = json.load(f)
        print(f"Contract data successfully loaded from {file_name}")
        return loaded_data
    except FileNotFoundError:
        print(f"{file_name} not found. No data loaded.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_name}. No data loaded.")
        return {}
    except Exception as e:
        print(f"Error loading contract data: {e}")
        return {}
    
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        if isinstance(obj, AttributeDict):
            return dict(obj)
        return super().default(obj)