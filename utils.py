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

def deploy_create_x(web3, create_x, creation_code, salt):
    # Convert salt to bytes32
    if isinstance(salt, int):
        salt_bytes32 = salt.to_bytes(32, 'big')
    elif isinstance(salt, str):
        if salt.startswith('0x'):
            salt_bytes32 = bytes.fromhex(salt[2:])
        else:
            salt_bytes32 = bytes.fromhex(salt)
    else:
        raise ValueError("Salt must be an integer or a hex string")

    # Ensure salt_bytes32 is exactly 32 bytes
    if len(salt_bytes32) != 32:
        raise ValueError("Salt must be exactly 32 bytes long")

    # Load private key from .env file
    private_key = os.getenv('DEPLOYER_PRIVATE_KEY')
    if not private_key:
        raise ValueError("Private key not found in .env file")

    # Get the account from the private key
    account = web3.eth.account.from_key(private_key)
    print(f"Account address: {account.address}")

    priority_fee = int(1e5)
    max_fee_per_gas = web3.eth.gas_price
    # Build the transaction
    transaction = create_x.functions.deployCreate2(salt_bytes32, creation_code).build_transaction({
        'from': account.address,
        'gas': 2000000,  # Adjust gas limit as needed
        'maxFeePerGas': max_fee_per_gas,
        'maxPriorityFeePerGas': priority_fee,
        'nonce': web3.eth.get_transaction_count(account.address),
        'chainId': web3.eth.chain_id
    })

    # Sign the transaction
    signed_txn = account.sign_transaction(transaction)

    # Send the transaction
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f'Sending txn: {tx_hash.hex()}')
        
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
        
        print(f"\nTransaction successful. Transaction hash: {tx_receipt.transactionHash.hex()}")
    except Exception as e:
        print(f"\nError sending transaction: {str(e)}")
        return None

    return tx_receipt.contractAddress

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

def compute_deployment_address():
    pass
def encode_constructor_args():
    pass

def compute_deployment_address(contract_name, contract_data, selected_version):
    bytecode = contract_data['bytecode']
    constructor_args = encode_constructor_args(contract_name, contract_data['abi'], selected_version)
    if constructor_args:
        bytecode += constructor_args[2:] if constructor_args.startswith('0x') else constructor_args
    
    # print(f"\n\nBytecode: {bytecode}\n\n")
    create_x = web3.eth.contract(address=CREATE_X_ADDRESS, abi=load_abi('CreateX'))
    salt = Web3.to_bytes(generate_salt(selected_version))
    init_code_hash = Web3.keccak(text=bytecode)
    # print(f"Salt: {salt}")
    # print(f"Init code hash: {init_code_hash}")
    deployment_address = create_x.functions.computeCreate2Address(Web3.to_bytes(salt), init_code_hash).call()
    print(f'Deployment address: {deployment_address}')

    return deployment_address
    if has_code_at_address(web3, deployment_address):
        print(f"Protocol already deployed on chain id {chain_id} at {deployment_address}. Exiting.")
        return

def encode_constructor_args(contract_name, abi, selected_version):
    constructor_args = extract_constructor_args(abi)
    if not constructor_args:
        return None
    contract = web3.eth.contract(abi=abi)
    if contract_name == 'VaultFactory':
        vault_implementation = '0xcA78AF7443f3F8FA0148b746Cb18FF67383CDF3f'
        encoded_args = encode(
            ['string', 'address', 'address'],
            [
                f'Yearn {selected_version} Vault Factory',
                vault_implementation,
                INIT_GOV
            ]
        )
        return encoded_args.hex()
    return None

def deploy_contract(web3, create_x, salt, bytecode):
    deployed_address = deploy_contract(web3, create_x, salt, bytecode)
    
    if deployed_address:
        print(f"Contract deployed at address: {deployed_address}")
        # Step 6: Cache deployment info
        cache_deployment_info(chain_id, deployed_address)

def deploy_contract(web3, create_x, salt, bytecode):
    private_key = os.getenv('PRIVATE_KEY')
    deployer = web3.eth.account.from_key(private_key)
    try:
        # Create transaction to deploy the contract
        tx = create_x.functions.deployCreate2(
            salt, bytecode
        ).transact({
            'from': deployer.address,
            # 'gas': 10_000_000,  # Custom gas limit
            'maxFeePerGas': web3.to_wei(10, 'gwei'),  # 10 gwei
            'maxPriorityFeePerGas': web3.to_wei(0.001, 'gwei'),  # 1 gwei
            'nonce': web3.eth.getTransactionCount(deployer.address)  # Set nonce if necessary
        })
        
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        print(f"Transaction successful with receipt: {tx_receipt}")
        return tx_receipt.contractAddress
    
    except Exception as e:
        print(f"Error deploying contract: {e}")
        return None
    
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