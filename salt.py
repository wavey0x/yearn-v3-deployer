from utils import generate_salt
from web3 import Web3
import hashlib
from addresses import V3_PROTOCOL_ADDRESSES
from utils import compute_create2_address, fetch_creation_code
from constants import DEPLOYERS

def audit():
    """
    loop thru all v3 protocol addresses and make sure the computed salt pre-image matches
    what is given in the addresses file.
    """
    for key, item in V3_PROTOCOL_ADDRESSES.items():
        if 'salt' not in item or item["salt"] == '':
            print(f'------------ {key} --------------')
            print(f'Skipping {key} because no salt')
            continue

        deployer = item['deployer']
        deployer_key = next((key for key, value in DEPLOYERS.items() if value == deployer), None)
        salt_preimage = item['salt_preimage']
        if deployer == DEPLOYERS['CREATEX']:
            # If salt is an int, convert to hex
            salt_preimage = hex(salt_preimage) if isinstance(salt_preimage, int) else salt_preimage
            computed_salt = Web3.keccak(hexstr=salt_preimage).hex()
        else:
            computed_salt = salt_preimage
        actual_salt = item["salt"].lower() if isinstance(item["salt"], str) else item["salt"]
        creation_code = fetch_creation_code(item['address'])
        computed_address = compute_create2_address(Web3(), item['deployer'], computed_salt, creation_code)
        print(f'------------ {key} | {deployer_key} --------------')
        print(f'Preimage: {salt_preimage}')
        print(f'Salt: {emojify(computed_salt == actual_salt)} {computed_salt} {actual_salt}')
        print(f'Address: {emojify(computed_address == item["address"])} {computed_address} {item["address"]}')


def emojify(some_bool):
    if some_bool:
        return '🟢'
    else:
        return '🔴'

def main():
    contracts = [
        'Accountant Factory',
        'Protocol Address Provider',
        'Debt Allocator Factory',
        'Keeper',
        'registry', # release registry
        'Role Manager',
        'Splitter Factory',
        'v3.0.3',
        'APR Oracle',
    ]
    for name in contracts:
        salt = generate_salt(name)
        hex_salt = Web3.to_hex(salt)
        print(f"{name}: {hex_salt}")

    print('apr oracle', Web3.keccak(text='APR Oracle').hex())
    print('Auction Factory', Web3.keccak(text='Auction Factory').hex())
    print('Common Trigger', Web3.keccak(text='Common Trigger').hex())
    print('Init Gov', Web3.keccak(text='Init Gov').hex())
    print('Tokenized Strategy', Web3.keccak(text='v3.0.3').hex())
    print('Vault Factory', Web3.keccak(text='v3.0.3').hex())
    print('Vault 303', Web3.keccak(text='v3.0.3').hex())

    salt_string = "v3.0.3"

    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    # Update the hash object with the string data
    hash_object.update(salt_string.encode("utf-8"))
    # Get the hexadecimal representation of the hash
    hex_hash = hash_object.hexdigest()
    # Convert the hexadecimal hash to an integer
    salt = int(hex_hash, 16)
    print(salt)
    print(Web3.to_hex(salt))

if __name__ == '__main__':
    audit()