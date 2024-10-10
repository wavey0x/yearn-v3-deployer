from utils import get_source_from_etherscan, _verify_contract
from web3 import Web3
from constants import NETWORKS
import json

def main():
    chain_id = 8453 # Chain to verify on
    mainnet_address = '0xe0514dD71cfdC30147e76f65C30bdF60bfD437C3'
    address_to_verify = '0x98F69a88144279774c1a7034F5a2eb37791D6b5f'

    # Get verification data from etherscan
    verification_data = get_source_from_etherscan(1, mainnet_address)
    
    # Verify contract on target chain
    verification_data['chain_id'] = chain_id
    _verify_contract(address_to_verify, verification_data)

if __name__ == '__main__':
    main()