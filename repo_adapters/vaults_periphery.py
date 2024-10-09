from utils import extract_constructor_args, encode_constructor_args, load_abi, generate_salt
import web3
from constants import CREATE_X_ADDRESS, INIT_GOV
from eth_abi import encode
web3 = None

def prepare_bytecode(_web3, contract_name, contract_data, selected_version):
    global web3
    web3 = _web3
    bytecode = contract_data['bytecode']
    constructor_args = encode_constructor_args(contract_name, contract_data['abi'], selected_version)
    if constructor_args:
        bytecode += constructor_args[2:] if constructor_args.startswith('0x') else constructor_args
    
    return bytecode

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

def build_creation_code(contract_name, contract_data, selected_version):
    bytecode = contract_data['bytecode']
    constructor_args = encode_constructor_args(contract_name, contract_data['abi'], selected_version)
    if constructor_args:
        bytecode += constructor_args[2:] if constructor_args.startswith('0x') else constructor_args
    return bytecode

def compute_deployment_address(contract_name, contract_data, selected_version):
    creation_code = build_creation_code(contract_name, contract_data, selected_version)
    # print(f"\n\nBytecode: {bytecode}\n\n")
    create_x = web3.eth.contract(address=CREATE_X_ADDRESS, abi=load_abi('CreateX'))
    salt = web3.to_bytes(generate_salt(selected_version))
    init_code_hash = web3.keccak(text=creation_code)
    # print(f"Salt: {salt}")
    # print(f"Init code hash: {init_code_hash}")
    deployment_address = create_x.functions.computeCreate2Address(web3.to_bytes(salt), init_code_hash).call()
    print(f'Deployment address: {deployment_address}')

    return deployment_address