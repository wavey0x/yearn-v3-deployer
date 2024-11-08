"""
STOP! Before modifying these addresses, please ensure the following...

1. The following data is mainnet Ethereum data only
2. `address` should be the value for the latest canonical deployment of each contract 
    as deployed on Ethereum.
3. `salt` is the user supplied argument value passed into the deployment transaction. 
    Note: In the case of createX, this is different than the salt used in the CREATE2 calculation.
4. `deployer` is the address of the account/factory that deployed the contract. 
    Should always be CREATEX, but other CREATE2 factories will also work.
"""

V3_PROTOCOL_ADDRESSES = {
    'init_gov': {
        'name': 'InitGov.sol',
        'address': '0x6f3cBE2ab3483EC4BA7B672fbdCa0E9B33F88db8',
        'id': 'INIT GOV',
        'salt': '0xa5529a6fcf3368cf56418456e1e34e7e46ef50503bfd8f4569cd6f8823c5bdde',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'address_provider': {
        'name': 'AddressProvider.vy',
        'address': '0x775F09d6f3c8D2182DFA8bce8628acf51105653c',
        'id': 'ADDRESS PROVIDER',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'accountant_factory': {
        'name': 'AccountantFactory.sol',
        'id': 'Accountant Factory',
        'address': '0xF728f839796a399ACc2823c1e5591F05a31c32d1',
        'salt': '0x6d19e04f85bfa39ce8b6908668c46b2937461f0373aaa91c7619f2364545887d',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'vault_implementation': {
        'name': 'Vault.vy',
        'address': '0xd8063123BBA3B480569244AE66BFE72B6c84b00d',
        'id': 'VAULT',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'registry_factory': {
        'name': 'RegistryFactory.sol',
        'address': '0x3A0fa8aac82aD94048098D6af6e8eB36c98816A1',
        'id': 'Registry Factory',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'vault_factory': {
        'name': 'VaultFactory.vy',
        'address': '0x770D0d1Fb036483Ed4AbB6d53c1C88fb277D812F',
        'id': 'VAULT FACTORY',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'splitter_factory': {
        'name': 'SplitterFactory.vy',
        'address': '0xe28fCC9FB2998ba57754789F6666DAa8C815614D',
        'id': 'Splitter Factory',
        'salt': '0x4f63ede797a190c28b8121ae0f2ebc20ac89032ab047d98aeb464b20e2fcdf7a',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'tokenized_strategy': {
        'name': 'TokenizedStrategy.sol',
        'address': '0xD377919FA87120584B21279a491F82D5265A139c',
        'id': 'TOKENIZED STRATEGY',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'release_registry': {
        'name': 'ReleaseReigstry.sol',
        'address': '0x0377b4daDDA86C89A0091772B79ba67d0E5F7198',
        'id': 'Release Registry',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'base_fee_provider': {
        'name': 'BaseFeeProvider.sol',
        'address': '0xe0514dD71cfdC30147e76f65C30bdF60bfD437C3',
        'id': 'Base Fee Provider',
        'salt': 0,
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed' # CREATE1
    },
    'apr_oracle': {
        'name': 'AprOracle.sol',
        'address': '0x1981AD9F44F2EA9aDd2dC4AD7D075c102C70aF92',
        'id': 'APR Oracle',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000', # Value passed into CreateX
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'common_report_trigger': {
        'name': 'CommonReportTrigger.sol',
        'address': '0xA045D4dAeA28BA7Bfe234c96eAa03daFae85A147',
        'id': 'Common Report Trigger',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'keeper': {
        'name': 'Keeper.sol',
        'address': '0x52605BbF54845f520a3E94792d019f62407db2f8',
        'id': 'Keeper',
        'salt': '0x7cc943b2ded12c38a61c6da1aba5b5ce13b561acc23a95b3df121765c5e5af20',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'role_manager_factory': {
        'name': 'RoleManagerFactory.sol',
        'address': '0xca12459a931643BF28388c67639b3F352fe9e5Ce',
        'id': 'Role Manager Factory',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'allocator_factory': {
        'name': 'AllocatorFactory.sol',
        'address': '0x03D43dF6FF894C848fC6F1A0a7E8a539Ef9A4C18',
        'id': 'Debt Allocator Factory',
        'salt': '0000000000000000000000000000000000000000000000000000000000000000',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    }
}