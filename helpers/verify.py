import os
import sys
import argparse
from web3 import Web3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_source_from_etherscan, verify_contract, check_verification_status


contracts = [
    "0x6f3cBE2ab3483EC4BA7B672fbdCa0E9B33F88db8",
    "0x775F09d6f3c8D2182DFA8bce8628acf51105653c",
    "0xF728f839796a399ACc2823c1e5591F05a31c32d1",
    "0xd8063123BBA3B480569244AE66BFE72B6c84b00d",
    "0x3A0fa8aac82aD94048098D6af6e8eB36c98816A1",
    "0x770D0d1Fb036483Ed4AbB6d53c1C88fb277D812F",
    "0xe28fCC9FB2998ba57754789F6666DAa8C815614D",
    "0xD377919FA87120584B21279a491F82D5265A139c",
    "0x0377b4daDDA86C89A0091772B79ba67d0E5F7198",
    "0x7aFA431d09D8b0849f183AB8c49a27729ebEf4B2",
    "0x1981AD9F44F2EA9aDd2dC4AD7D075c102C70aF92",
    "0xA045D4dAeA28BA7Bfe234c96eAa03daFae85A147",
    "0x52605BbF54845f520a3E94792d019f62407db2f8",
    "0xca12459a931643BF28388c67639b3F352fe9e5Ce",
    "0x03D43dF6FF894C848fC6F1A0a7E8a539Ef9A4C18",
]

contractss = [
    "0xCfA510188884F199fcC6e750764FAAbE6e56ec40",
    "0xd42b64272bAC138C75bDF3580FF3010E806f6303"
]
"""
Utility to verify a deployed contract on an EVM chain using etherscan.
Pass params via CLI or set defaults in the function call.
"""
def main():
    chain_id = 999
    for contract in contracts:
        mainnet_address = contract
        address_to_verify = contract
        # Get verification data from etherscan
        verification_data = get_source_from_etherscan(1, mainnet_address, print_debug=True)
        print(verification_data)
        # Verify contract on target chain
        verification_data['chain_id'] = chain_id
        guid = verify_contract(chain_id, address_to_verify, print_debug=True)
        # status = check_verification_status(chain_id, guid, print_debug=True)

if __name__ == '__main__':
    main()
