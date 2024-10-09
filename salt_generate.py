from utils import generate_salt
from web3 import Web3
import hashlib
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
    main()