from eth_abi import encode
import hashlib
import json
import os
import requests
from hexbytes import HexBytes
from constants import BLOCKSCOUT_API_BASE, DEPLOYERS, CREATE_X_ADDRESS, ETHERSCAN_API_BASE, NETWORKS, ETHERSCAN_API_BASE_V2
from web3.datastructures import AttributeDict
from dotenv import load_dotenv
import os
import time
import sys

load_dotenv()

ETHERSCAN_KEY = os.getenv('ETHERSCAN_KEY')

def compute_create2_address(web3, factory, salt, creation_code, print_debug=False):
    """
    If using createx, salt must be the guarded salt generated internally by createx
    """
    global CREATE_X
    if print_debug:
        print(f"Factory: {factory}")
        print(f"Salt: {salt}")
        print(f"Creation code: {creation_code[:30]}")
    if isinstance(salt, int):
        if salt.bit_length() > 256:
            raise ValueError("Salt integer must be 32 bytes or less")
        salt = hex(salt)[2:]
    elif isinstance(salt, str):
        if len(salt) != 64 and len(salt) != 66: # Account for 0x chars
            raise ValueError("Salt hex string must be 32 bytes (64 characters) long")
        salt = salt[2:] if salt.startswith('0x') else salt
        

    # Note: We dont need this if we pass the original salt to createx
    # For CreateX, the salt is a keccak256 hash of the original salt
    # if factory == DEPLOYERS['CREATEX']:
    #     salt = web3.keccak(hexstr=salt).hex()
        
    salt = web3.to_bytes(hexstr=salt) if isinstance(salt, str) else salt
        
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

def deploy_create2(web3, factory, salt, creation_code):
    if not has_code_at_address(web3, factory):
        print(f"\n\033[91mError: Deployer {factory} does not exist on chain id {web3.eth.chain_id} ... Now exiting.\033[0m\n")
        return False
    
    # Validate salt
    if isinstance(salt, int):
        if salt.bit_length() > 256:
            raise ValueError("Salt integer must be 32 bytes or less")
        salt = salt.to_bytes(32, 'big').hex()
    elif isinstance(salt, str):
        if len(salt) != 64 and len(salt) != 66: # Account for 0x chars
            raise ValueError("Salt hex string must be 32 bytes (64 characters) long")
        salt = salt[2:] if salt.startswith('0x') else salt
    
    final_salt = salt
    if factory == DEPLOYERS['CREATEX']:
        final_salt = web3.keccak(hexstr=salt).hex()

    salt = web3.to_bytes(hexstr=salt)

    # Load private key from .env file
    private_key = os.getenv('DEPLOYER_PRIVATE_KEY')
    if not private_key:
        raise ValueError("Private key not found in .env file")

    # Get the account from the private key
    deployment_address = compute_create2_address(web3, factory, final_salt, creation_code)

    if has_code_at_address(web3, deployment_address):
        print(f"Contract already deployed at {deployment_address}. Now exiting.")
        return deployment_address
    account = web3.eth.account.from_key(private_key)
    priority_fee = int(1e5)
    max_fee_per_gas = web3.eth.gas_price
    # gas_limit = web3.eth.estimate_gas(transaction)
    print(f"Gas price: {max_fee_per_gas / 1e9:,.4f} gwei | Priority fee: {priority_fee / 1e9:,.4f} gwei")
    # Build the transaction

    if factory == DEPLOYERS['CREATEX']:
        create_x = web3.eth.contract(address=CREATE_X_ADDRESS, abi=load_abi('CreateX'))
        transaction = create_x.functions.deployCreate2(salt, creation_code).build_transaction({
            'from': account.address,
            # 'gas': gas_limit,  # Adjust gas limit as needed
            'maxFeePerGas': max_fee_per_gas,
            # 'maxPriorityFeePerGas': priority_fee,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': web3.eth.chain_id
        })
    else:
        factory = web3.eth.contract(address=factory, abi=load_abi('Create2Factory'))
        salt = int.from_bytes(salt, 'big')
        transaction = factory.functions.deploy(creation_code, salt).build_transaction({
            'from': account.address,
            # 'gas': gas_limit,  # Adjust gas limit as needed
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': priority_fee,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': web3.eth.chain_id
        })

    signed_txn = account.sign_transaction(transaction)
    
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction receipt with a loading animation and timeout
        print(f"Waiting for transaction to be mined: 0x{tx_hash.hex()}", end="")
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
        return False

    # Process all events in the receipt
    print(f"\nDeployed at: \033[92m{deployment_address}\033[0m\n")
    verify_contract(web3.eth.chain_id, deployment_address)
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
    if some_bool is None:
        return '    '
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
        "apikey": ETHERSCAN_KEY
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
    
def get_source_from_etherscan(chain_id, address):
    url = f'{ETHERSCAN_API_BASE}/api?module=contract&action=getsourcecode&address={address}&apikey={ETHERSCAN_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'result' not in data:
        print(f'No result found for {address}')
        return None
    if 'SourceCode' not in data['result'][0]:
        print(f'No source code found for {address}')
        return None
    verification_data = {
        'contract_name': data['result'][0]['ContractName'],
        'source': data['result'][0]['SourceCode'],
        'compiler_version': data['result'][0]['CompilerVersion'],
        'constructor_args': data['result'][0]['ConstructorArguments'],
        'optimization_used': data['result'][0]['OptimizationUsed'],
        'runs': data['result'][0]['Runs'],
        'license': data['result'][0]['LicenseType'],
        'chain_id': chain_id,
        'code_format': 'solidity-single-file',
    }
    return verification_data

def _verify_contract(address, verification_data, print_debug=False):
    url = f'{ETHERSCAN_API_BASE}/api?module=contract&action=verifysourcecode&apikey={ETHERSCAN_KEY}'
    data = {
        'chainId': verification_data['chain_id'],
        'codeformat': verification_data['code_format'],
        'sourceCode': verification_data['source'],
        'constructorArguements': verification_data['constructor_args'],
        'contractaddress': address,
        'contractname': verification_data['contract_name'],
        'compilerversion': verification_data['compiler_version'],
        'optimizationUsed': verification_data['optimization_used'],
        'runs': verification_data['runs'],
        'licenseType': verification_data['license']
    }
    response = requests.post(url, data=data)
    success = False
    if print_debug:
        print("Verification data:")
        data_to_print = data.copy()
        data_to_print['sourceCode'] = data_to_print['sourceCode'][:20] + '...'
        print(json.dumps(data_to_print, indent=2, cls=CustomJSONEncoder))
    try:
        success = response.json()['status'] == '1' and response.json()['message'] == 'OK'
        guid = response.json()['result']
    except KeyError:
        print(f'Unexpected response structure when verifying {data["contractaddress"]} on chain id: {data["chainId"]}:\n{response.json()}')
        return False
    if success:
        print(f'Verification info submitted for {data["contractaddress"]} on chain id: {data["chainId"]}')
    return guid

def verify_contract(chain_id, address, print_debug=False, poll_interval=5, wait_before_request=10):
    if not isinstance(poll_interval, int):
        raise ValueError("poll_interval must be an integer")
    verification_data = get_source_from_etherscan(chain_id, address)
    if 'vyper' in verification_data['compiler_version'].lower():
        print('\033[93m' + f'\033[1mWarning\033[0m\033[93m: Vyper contracts are not supported by Etherscan API. This contract must be manually verified.' + '\033[0m')
        return 0
    time.sleep(wait_before_request) # Before request, we wait a bit to let etherscan catch up
    guid = _verify_contract(address, verification_data, print_debug)
    status = check_verification_status(guid, print_debug)
    return

def check_verification_status(guid, print_debug=False, poll_interval=5):
    if not isinstance(poll_interval, int):
        raise ValueError("poll_interval must be an integer")
    time.sleep(poll_interval)
    url = f'{ETHERSCAN_API_BASE}/api?module=contract&action=checkverifystatus&guid={guid}&apikey={ETHERSCAN_KEY}'
    fail_count = 0
    while True:
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError(
                f"Status {response.status_code} when querying {url}: {response.text}"
            )
        data = response.json()
        if data["result"] == "Pending in queue":
            print("Verification pending...")
        elif "Unable to locate ContractCode" in data["result"]:
            fail_count += 1
            if print_debug:
                print(f"Verification attempt {fail_count} response:\n{data['result']}")
            if fail_count * poll_interval > 90: # 90s timeout
                print(f"\033[91mVerification failed. {data['result']}\033[0m")
                break
            time.sleep(poll_interval)
            continue
        else:
            print(f"\033[92mVerification complete. {data['result']}\033[0m")
            return data["message"] == "OK"
        time.sleep(poll_interval)

def is_contract_verified(chain_id, address):
    api_url_base = f'{ETHERSCAN_API_BASE_V2}/'
    url = f'{api_url_base}/api?chainid={chain_id}&module=contract&action=getabi&address={address}&apikey={ETHERSCAN_KEY}'
    response = requests.get(url)
    data = response.json()
    return response.status_code != 200 or data['message'] != 'NOTOK'

def get_chain_name(chain_id):
    return NETWORKS[chain_id]['name'] if chain_id in NETWORKS else 'unknown-chain'