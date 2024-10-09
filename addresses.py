V3_PROTOCOL_ADDRESSES = {
    'init_gov': {
        'address': '0x6f3cBE2ab3483EC4BA7B672fbdCa0E9B33F88db8',
        'id': 'INIT GOV',
        'salt_preimage': '0xa5529a6fcf3368cf56418456e1e34e7e46ef50503bfd8f4569cd6f8823c5bdde',
        'salt': 'C4B33C43F9AF3781E23E6828BC48D6814D92B625D482A69BBCACF2E3A116D5C0',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'address_provider': {
        'address': '0x1e9778aAD41Aa3E0884C276fB4C2D03C4036Aa0B',
        'id': 'ADDRESS PROVIDER',
        'salt_preimage': '0x4bee2c2f956cf45fd11afbff2210b9ea37a48bf5fd2a3d12a1d1337d5e8f101e',
        'salt': 'E73A7A1B14BBE30BBF03553EFE35C214D43215F1D25EEC45D0613B29418C696E',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'accountant_factory': {
        'id': 'ACCOUNTANT FACTORY',
        'address': '0xF728f839796a399ACc2823c1e5591F05a31c32d1',
        'salt_preimage': '0x6d19e04f85bfa39ce8b6908668c46b2937461f0373aaa91c7619f2364545887d',
        'salt': 'AC9071465478B5F512A3E643F4E60A2B73D82CA7CA34069F6F323FDAF379A886',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'vault_implementation': {
        'address': '0xcA78AF7443f3F8FA0148b746Cb18FF67383CDF3f',
        'id': 'VAULT',
        'salt_preimage': '0x6b82dafe35e195e55829e589b42ab27ad15988b069b20615c136226c8a270865',
        'salt': '4B47D8EC7A7A872CAD215D467BFBD768C66BF241F9CA127D4A9ACBC75332980A',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'registry_factory': {
        'address': '0x8648FF16ed48FAD456BF0e0e2190AeA8710BdC81',
        'id': 'REGISTRY FACTORY',
        'salt_preimage': '0x872491a30d60d598962de6e7b834ab76b2aa65fbab102c6ebaaae6acdc238822',
        'salt': 'E7D2E348FD5170DC047F1017CB189DF6CA153AA32DAE3805D098DADCC9770DB9',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'vault_factory': {
        'address': '0x5577EdcB8A856582297CdBbB07055E6a6E38eb5f',
        'id': 'VAULT FACTORY',
        'salt_preimage': '0x6b82dafe35e195e55829e589b42ab27ad15988b069b20615c136226c8a270865',
        'salt': '8E225A77447BAC3E72B29A580123019DC26A28EBD6D9BE4F8F396A1DF8677CCF',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'splitter_factory': {
        'address': '0xe28fCC9FB2998ba57754789F6666DAa8C815614D',
        'id': 'SPLITTER FACTORY',
        'salt_preimage': '0x6d19e04f85bfa39ce8b6908668c46b2937461f0373aaa91c7619f2364545887d',
        'salt': '13ECA8D94F3DA78059363A546A770E520526A76D822F88F7E2500AFAD7332733',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'tokenized_strategy': {
        'address': '0x254A93feff3BEeF9cA004E913bB5443754e8aB19',
        'id': 'TOKENIZED STRATEGY',
        'salt_preimage': '0x76ce3962b8fa14419a4050782902ebac2d936ba86eb83ca48b362c1cd2d244dc',
        'salt': '4AB76E39AC6D0E3B29FDFEB8BBA6D4B01E1826E4D6C59064A8965470F9B91E1B',
        'deployer': '0x254A93feff3BEeF9cA004E913bB5443754e8aB19'
    },
    'release_registry': {
        'address': '0x990089173D5d5287c344092Be0bB37950A67d17B',
        'id': 'RELEASE REGISTRY',
        'salt_preimage': '0x872491a30d60d598962de6e7b834ab76b2aa65fbab102c6ebaaae6acdc238822',
        'salt': '61126846202173470780239454055476050204342965826331442198108521154130340972578',
        'deployer': '0x8D85e7c9A4e369E53Acc8d5426aE1568198b0112'
    },
    'base_fee_provider': {
        'address': '0xe0514dD71cfdC30147e76f65C30bdF60bfD437C3',
        'id': 'BASE FEE PROVIDER',
        'salt_preimage': 0,
        'salt': '290DECD9548B62A8D60345A988386FC84BA6BC95484008F6362F93160EF3E563',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed' # CREATE1
    },
    'apr_oracle': {
        'address': '0x27aD2fFc74F74Ed27e1C0A19F1858dD0963277aE',
        'id': 'APR ORACLE',
        'salt_preimage': '0x92308d754fefe74f180a813f808c0966735868624696943110ce3b77ef4da6fc', # Value passed into CreateX
        'salt': '300044A4E6C832AAA06DA4F2AEE13EE67F62388F2A4F5E57AD6E86C8CB843D19', # Processed salt used in create2
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'common_report_trigger': {
        'address': '0xD98C652f02E7B987e0C258a43BCa9999DF5078cF',
        'id': 'COMMON REPORT TRIGGER',
        'salt_preimage': '0x6d19e04f85bfa39ce8b6908668c46b2937461f0373aaa91c7619f2364545887d',
        'salt': 96024494127036433653418792335021124045183520027330983676371068081276756155280,
        'deployer': '0x8D85e7c9A4e369E53Acc8d5426aE1568198b0112'
    },
    'keeper': {
        'address': '0x52605BbF54845f520a3E94792d019f62407db2f8',
        'id': 'KEEPER',
        'salt_preimage': '0x7cc943b2ded12c38a61c6da1aba5b5ce13b561acc23a95b3df121765c5e5af20',
        'salt': 'CE9FB45842E90271765DB6D885A5977664D8168AE146A33DBF4ADDD5A6D51FBC',
        'deployer': '0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed'
    },
    'role_manager_factory': {
        'address': '',
        'id': 'ROLE MANAGER FACTORY',
        'salt_preimage': '',
        'salt': '',
        'deployer': ''
    },
    'allocator_factory': {
        'address': '',
        'id': 'ALLOCATOR FACTORY',
        'salt_preimage': '',
        'salt': '',
        'deployer': ''
    },
    'router': {
        'address': '0x1112dbCF805682e828606f74AB717abf4b4FD8DE',
        'id': 'ROUTER',
        'salt_preimage': '',
        'salt': '',
        'deployer': ''
    },
    
}