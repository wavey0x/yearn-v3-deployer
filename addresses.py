"""
STOP! Before modifying these addresses, please ensure the following...

1. The following data is mainnet Ethereum data only
2. Each address is the values for the latest canonical deployment of each contract
3. salt_preimage is the value passed into the deployment transaction
4. salt is the value used in the CREATE2 calculation. For createX deployments, this is different than the preimage, and can be found in the emit event.
"""

V3_PROTOCOL_ADDRESSES = {
    'init_gov': {
        'name': 'InitGov.sol',
        'address': '0x6f3cBE2ab3483EC4BA7B672fbdCa0E9B33F88db8',
        'id': 'INIT GOV',
        'salt_preimage': '0xa5529a6fcf3368cf56418456e1e34e7e46ef50503bfd8f4569cd6f8823c5bdde',
        'salt': 'C4B33C43F9AF3781E23E6828BC48D6814D92B625D482A69BBCACF2E3A116D5C0',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'address_provider': {
        'name': 'AddressProvider.sol',
        'address': '0x775F09d6f3c8D2182DFA8bce8628acf51105653c',
        'id': 'ADDRESS PROVIDER',
        'salt_preimage': '0000000000000000000000000000000000000000000000000000000000000000',
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'accountant_factory': {
        'name': 'AccountantFactory.sol',
        'id': 'Accountant Factory',
        'address': '0xF728f839796a399ACc2823c1e5591F05a31c32d1',
        'salt_preimage': '0x6d19e04f85bfa39ce8b6908668c46b2937461f0373aaa91c7619f2364545887d',
        'salt': 'AC9071465478B5F512A3E643F4E60A2B73D82CA7CA34069F6F323FDAF379A886',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'vault_implementation': {
        'name': 'Vault.vy',
        'address': '0xcA78AF7443f3F8FA0148b746Cb18FF67383CDF3f',
        'id': 'VAULT',
        'salt_preimage': '0x6b82dafe35e195e55829e589b42ab27ad15988b069b20615c136226c8a270865',
        'salt': '4B47D8EC7A7A872CAD215D467BFBD768C66BF241F9CA127D4A9ACBC75332980A',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'registry_factory': {
        'name': 'RegistryFactory.sol',
        'address': '0x3A0fa8aac82aD94048098D6af6e8eB36c98816A1',
        'id': 'Registry Factory',
        'salt_preimage': '0000000000000000000000000000000000000000000000000000000000000000',
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'vault_factory': {
        'name': 'VaultFactory.vy',
        'address': '0x5577EdcB8A856582297CdBbB07055E6a6E38eb5f',
        'id': 'VAULT FACTORY',
        'salt_preimage': '0x4b47d8ec7a7a872cad215d467bfbd768c66bf241f9ca127d4a9acbc75332980a',
        'salt': '8E225A77447BAC3E72B29A580123019DC26A28EBD6D9BE4F8F396A1DF8677CCF',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'splitter_factory': {
        'name': 'SplitterFactory.vy',
        'address': '0xe28fCC9FB2998ba57754789F6666DAa8C815614D',
        'id': 'Splitter Factory',
        'salt_preimage': '0x4f63ede797a190c28b8121ae0f2ebc20ac89032ab047d98aeb464b20e2fcdf7a',
        'salt': '13ECA8D94F3DA78059363A546A770E520526A76D822F88F7E2500AFAD7332733',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'tokenized_strategy': {
        'name': 'TokenizedStrategy.sol',
        'address': '0x254A93feff3BEeF9cA004E913bB5443754e8aB19',
        'id': 'TOKENIZED STRATEGY',
        'salt_preimage': '0x76ce3962b8fa14419a4050782902ebac2d936ba86eb83ca48b362c1cd2d244dc',
        'salt': '4AB76E39AC6D0E3B29FDFEB8BBA6D4B01E1826E4D6C59064A8965470F9B91E1B',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'release_registry': {
        'name': 'ReleaseReigstry.sol',
        'address': '0x0377b4daDDA86C89A0091772B79ba67d0E5F7198',
        'id': 'Release Registry',
        'salt_preimage': '0000000000000000000000000000000000000000000000000000000000000000',
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'base_fee_provider': {
        'name': 'BaseFeeProvider.sol',
        'address': '0xe0514dD71cfdC30147e76f65C30bdF60bfD437C3',
        'id': 'Base Fee Provider',
        'salt_preimage': 0,
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed' # CREATE1
    },
    'apr_oracle': {
        'name': 'AprOracle.sol',
        'address': '0x1981AD9F44F2EA9aDd2dC4AD7D075c102C70aF92',
        'id': 'APR Oracle',
        'salt_preimage': '0000000000000000000000000000000000000000000000000000000000000000', # Value passed into CreateX
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563', # Processed salt used in create2
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'common_report_trigger': {
        'name': 'CommonReportTrigger.sol',
        'address': '0xA045D4dAeA28BA7Bfe234c96eAa03daFae85A147',
        'id': 'Common Report Trigger',
        'salt_preimage': '0000000000000000000000000000000000000000000000000000000000000000',
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'keeper': {
        'name': 'Keeper.sol',
        'address': '0x52605BbF54845f520a3E94792d019f62407db2f8',
        'id': 'Keeper',
        'salt_preimage': '0x7cc943b2ded12c38a61c6da1aba5b5ce13b561acc23a95b3df121765c5e5af20',
        'salt': 'CE9FB45842E90271765DB6D885A5977664D8168AE146A33DBF4ADDD5A6D51FBC',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'role_manager_factory': {
        'name': 'RoleManagerFactory.sol',
        'address': '0xca12459a931643BF28388c67639b3F352fe9e5Ce',
        'id': 'Role Manager Factory',
        'salt_preimage': '0000000000000000000000000000000000000000000000000000000000000000',
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'allocator_factory': {
        'name': 'AllocatorFactory.sol',
        'address': '0x03D43dF6FF894C848fC6F1A0a7E8a539Ef9A4C18',
        'id': 'Debt Allocator Factory',
        'salt_preimage': '0000000000000000000000000000000000000000000000000000000000000000',
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    }
}