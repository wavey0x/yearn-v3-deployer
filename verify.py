from utils import get_source_from_etherscan, verify_contract
from web3 import Web3
from constants import NETWORKS

def main():
    rpc = NETWORKS[252]['rpc']
    web3 = Web3(Web3.HTTPProvider(rpc))
    address = '0x254A93feff3BEeF9cA004E913bB5443754e8aB19'
    verification_data = get_source_from_etherscan(web3,address)
    verify_contract(address, verification_data)

if __name__ == '__main__':
    main()