import os
import sys
import argparse
from web3 import Web3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_source_from_etherscan, verify_contract, check_verification_status

"""
Utility to verify a deployed contract on an EVM chain using etherscan.
Pass params via CLI or set defaults in the function call.
"""
def main():
    chain_id = 56
    mainnet_address = '0x0377b4daDDA86C89A0091772B79ba67d0E5F7198'
    address_to_verify='0x0377b4daDDA86C89A0091772B79ba67d0E5F7198'
    # Get verification data from etherscan
    verification_data = get_source_from_etherscan(10, mainnet_address, print_debug=True)
    
    # Verify contract on target chain
    verification_data['chain_id'] = chain_id
    guid = verify_contract(chain_id, address_to_verify, print_debug=True)
    # status = check_verification_status(chain_id, guid, print_debug=True)

if __name__ == '__main__':
    main()
