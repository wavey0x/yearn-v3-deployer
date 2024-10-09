ADDRESS_PROVIDER = '0x1e9778aAD41Aa3E0884C276fB4C2D03C4036Aa0B'
INIT_GOV = '0x6f3cBE2ab3483EC4BA7B672fbdCa0E9B33F88db8'
CREATE_X_ADDRESS = '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
CREATE_2_DEPLOYER = '0x8D85e7c9A4e369E53Acc8d5426aE1568198b0112'
BLOCKSCOUT_API_BASE =  'https://eth.blockscout.com/api/v2/smart-contracts/'
# REPOSITORIES = {
#     'yearn-vaults-v3': 'wavey0x/yearn-vaults-v3',
#     'vault-periphery': 'wavey0x/vault-periphery',
#     'Yearn-ERC4626-Router': 'yearn/Yearn-ERC4626-Router',
#     'tokenized-strategy': 'yearn/tokenized-strategy',
#     'tokenized-strategy-periphery': 'yearn/tokenized-strategy-periphery',
# }

# REPO_ADAPTERS = {
#     'yearn-vaults-v3': 'yearn_vaults_v3',
#     'vault-periphery': 'vault_periphery',
#     'Yearn-ERC4626-Router': 'yearn_erc4626_router',
#     'tokenized-strategy': 'tokenized_strategy',
#     'tokenized-strategy-periphery': 'tokenized_strategy_periphery',
# }

# V3_PROTOCOL_ADDRESSES = {
#     'accountant_factory': {
#         'id': 'ACCOUNTANT FACTORY',
#         'address': '0xF728f839796a399ACc2823c1e5591F05a31c32d1',
#         'salt': 'AC9071465478B5F512A3E643F4E60A2B73D82CA7CA34069F6F323FDAF379A886',
#         'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
#     },
#     'registry_factory': {
#         'address': '0x8648FF16ed48FAD456BF0e0e2190AeA8710BdC81',
#         'id': 'REGISTRY FACTORY',
#         'salt': 'E7D2E348FD5170DC047F1017CB189DF6CA153AA32DAE3805D098DADCC9770DB9',
#         'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
#     },
#     'vault_factory': {
#         'address': '0x5577EdcB8A856582297CdBbB07055E6a6E38eb5f',
#         'id': 'VAULT FACTORY',
#         'salt': '8E225A77447BAC3E72B29A580123019DC26A28EBD6D9BE4F8F396A1DF8677CCF',
#         'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
#     },
#     'splitter_factory': {
#         'address': '0xe28fCC9FB2998ba57754789F6666DAa8C815614D',
#         'id': 'SPLITTER FACTORY',
#         'salt': '13ECA8D94F3DA78059363A546A770E520526A76D822F88F7E2500AFAD7332733',
#         'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
#     },
#     'tokenized_strategy': {
#         'address': '0x254A93feff3BEeF9cA004E913bB5443754e8aB19',
#         'id': 'TOKENIZED STRATEGY',
#         'salt': '4AB76E39AC6D0E3B29FDFEB8BBA6D4B01E1826E4D6C59064A8965470F9B91E1B',
#         'deployer': '0x254A93feff3BEeF9cA004E913bB5443754e8aB19'
#     },
#     'release_registry': {
#         'address': '0x990089173D5d5287c344092Be0bB37950A67d17B',
#         'id': 'RELEASE REGISTRY',
#         'salt': 61126846202173470780239454055476050204342965826331442198108521154130340972578,
#         'deployer': '0x8D85e7c9A4e369E53Acc8d5426aE1568198b0112'
#     },
#     'base_fee_provider': {
#         'address': '0xe0514dD71cfdC30147e76f65C30bdF60bfD437C3',
#         'id': 'BASE FEE PROVIDER',
#         'salt': '',
#         'deployer': '' # CREATE1
#     },
#     'apr_oracle': {
#         'address': '0x27aD2fFc74F74Ed27e1C0A19F1858dD0963277aE',
#         'id': 'APR ORACLE',
#         'salt': '300044A4E6C832AAA06DA4F2AEE13EE67F62388F2A4F5E57AD6E86C8CB843D19',
#         'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
#     },
#     'common_report_trigger': {
#         'address': '0xD98C652f02E7B987e0C258a43BCa9999DF5078cF',
#         'id': 'COMMON REPORT TRIGGER',
#         'salt': 96024494127036433653418792335021124045183520027330983676371068081276756155280,
#         'deployer': '0x8D85e7c9A4e369E53Acc8d5426aE1568198b0112'
#     },
#     'keeper': {
#         'address': '0x52605BbF54845f520a3E94792d019f62407db2f8',
#         'id': 'KEEPER',
#         'salt': 'CE9FB45842E90271765DB6D885A5977664D8168AE146A33DBF4ADDD5A6D51FBC',
#         'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
#     },
#     'role_manager_factory': {
#         'address': '',
#         'id': 'ROLE MANAGER FACTORY',
#         'salt': '',
#         'deployer': ''
#     },
#     'allocator_factory': {
#         'address': '',
#         'id': 'ALLOCATOR FACTORY',
#         'salt': '',
#         'deployer': ''
#     },
#     'router': {
#         'address': '',
#         'id': 'ROUTER',
#         'salt': '',
#         'deployer': ''
#     }
# }

NETWORKS = {
    1: {
        'name': 'Ethereum',
        'rpc': 'https://eth.llamarpc.com'
    },
    10: {'name': 'Optimism',
        'rpc': 'https://mainnet.optimism.io/'
    },
    42161: {
        'name': 'Arbitrum',
        'rpc': 'https://arb1.arbitrum.io/rpc'
    },
    8453: {
        'name': 'Base',
        'rpc': 'https://1rpc.io/base'
    },
    137: {
        'name': 'Polygon',
        'rpc': 'https://polygon.llamarpc.com'
    },
    81457: {
        'name': 'Blast',
        'rpc': 'https://rpc.blast.io'
    },
    100: {
        'name': 'Gnosis',
        'rpc': 'https://rpc.ankr.com/gnosis'
    },
    252: {
        'name': 'Fraxtal',
        'rpc': 'https://rpc.frax.com'
    }
}