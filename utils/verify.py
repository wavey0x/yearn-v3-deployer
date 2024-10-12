from utils import get_source_from_etherscan, verify_contract, check_verification_status
from web3 import Web3
from constants import NETWORKS
import time
import argparse

"""
Utility to verify a deployed contract on an EVM chain using etherscan.
Pass params via CLI or set defaults in the function call.
"""
def main(
        chain_id=56, 
        mainnet_address='0xe0514dD71cfdC30147e76f65C30bdF60bfD437C3', 
        address_to_verify='0x7aFA431d09D8b0849f183AB8c49a27729ebEf4B2'
    ):

    # Get verification data from etherscan
    verification_data = get_source_from_etherscan(1, mainnet_address)
    
    # Verify contract on target chain
    verification_data['chain_id'] = chain_id

    guid = verify_contract(chain_id, address_to_verify, print_debug=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Verify a deployed contract on an EVM chain using etherscan.")
    parser.add_argument("--chain_id", type=int, default=56, help="Chain ID to verify on")
    parser.add_argument("--mainnet_address", default='0xe0514dD71cfdC30147e76f65C30bdF60bfD437C3', help="Mainnet address of the contract")
    parser.add_argument("--address_to_verify", default='0x7aFA431d09D8b0849f183AB8c49a27729ebEf4B2', help="Address of the contract to verify")
    
    args = parser.parse_args()
    
    main(args.chain_id, args.mainnet_address, args.address_to_verify)
