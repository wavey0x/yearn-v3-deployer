from web3 import Web3
import click
import requests
from utils import load_abi, fetch_creation_code, verify_contract, compute_create2_address, has_code_at_address, emojify, is_contract_verified, deploy_create2, get_chain_name
import tqdm
import os
from dotenv import load_dotenv
from constants import ADDRESS_PROVIDER, NETWORKS
from addresses import V3_PROTOCOL_ADDRESSES
from eth_account import Account

load_dotenv()

class YearnV3Deployer:
    def __init__(self):
        self.web3 = None
        self.address_provider = None
        self.rpc = None
        self.contract_data = {}
        self.latest_release = None
        self.ZERO_ADDRESS = '0x' + '0' * 40

    def initialize(self):
        pass

    def handle_rpc(self, _rpc=None):
        while not _rpc or _rpc is None:
            print("No RPC URL provided.")
            rpc = click.prompt('Please provide an RPC URL', type=int)

        self.web3 = Web3(Web3.HTTPProvider(_rpc))

        while not self.web3.is_connected():
            print("Failed to connect to the provided RPC URL.")
            _rpc = click.prompt('Please provide a valid RPC URL')
            self.web3 = Web3(Web3.HTTPProvider(_rpc))

        print(f"\nConnected to {get_chain_name(self.web3.eth.chain_id)} chain ID {self.web3.eth.chain_id} | {_rpc}")
        return self.web3

    def select_network(self):
        print("\nSelect a network:\n")
        print(f"{'ID':<8} {'Network':<20}")
        print("-" * 28)
        print(f"{'0':<8} {'🌐 Custom RPC':<20}")
        for chain_id, info in NETWORKS.items():
            print(f"{chain_id:<8} {info['name']:<20}")
        
        choice = click.prompt("\nEnter the chain ID or '0' for Custom RPC", type=int)
        
        if choice == 0:
            custom_rpc = click.prompt("Enter custom RPC URL")
            self.web3 = self.handle_rpc(custom_rpc)
            chain_id = self.web3.eth.chain_id
        else:
            chain_id = choice
            if chain_id in NETWORKS:
                self.web3 = self.handle_rpc(NETWORKS[chain_id]['rpc'])
            else:
                print(f"Chain ID {chain_id} not found in known networks. Please try again.")
                return self.select_network()
        
        return chain_id

    def print_chain_deployment_report(self):
        chain_id = self.web3.eth.chain_id
        self.address_provider = self.web3.eth.contract(address=ADDRESS_PROVIDER, abi=load_abi('AddressProvider'))
        print("-" * 94)  # Separator line
        self.contract_data.clear()  # Clear existing data
        protocol_deployed = True
        for key, info in tqdm.tqdm(V3_PROTOCOL_ADDRESSES.items(), desc="Loading Yearn V3 Protocol data"):
            if key in ['init_gov', 'address_provider']:
                if has_code_at_address(self.web3, info['address']):
                    continue
                protocol_deployed = False
                break # exit, and return false to indicate that the protocol is not deployed
            id = self.web3.keccak(text=info['id'])
            address = info['address']
            try:
                address_from_provider = self.address_provider.functions.getAddress(id).call()
            except Exception as e:
                print(f"Error fetching address from provider: {str(e)}")
                address_from_provider = None
            if key == 'vault_factory':
                if has_code_at_address(self.web3, V3_PROTOCOL_ADDRESSES['release_registry']['address']):
                    release_registry = self.web3.eth.contract(address=V3_PROTOCOL_ADDRESSES['release_registry']['address'], abi=load_abi('ReleaseRegistry'))
                    try:
                        address_from_provider = release_registry.functions.latestFactory().call()
                    except Exception as e:
                        address_from_provider = None
                else:
                    self.contract_data[key] = {
                        'address': address,
                        'deployed': False,
                        'is_set': False,
                        'computed_address': self.ZERO_ADDRESS,
                        'is_verified': is_contract_verified(chain_id, address)
                    }
                    continue
            deployed = has_code_at_address(self.web3, address)
            computed_address = None
            if address:
                computed_address = compute_create2_address(
                    self.web3, 
                    info['deployer'], 
                    0 if not info['salt'] else info['salt'], 
                    fetch_creation_code(address)
                )
                deployed = has_code_at_address(self.web3, computed_address)
            self.contract_data[key] = {
                'key': key,
                'address': address,
                'deployed': deployed,
                'is_set': None if key in ['tokenized_strategy', 'vault_implementation'] else address_from_provider == address,
                'computed_address': computed_address,
                'is_verified': is_contract_verified(chain_id, computed_address if computed_address else address)
            }

        if not protocol_deployed:
            click.echo(click.style(f'\nNotice: V3 Protocol not deployed on {get_chain_name(chain_id)} chain id {chain_id}\n', fg='yellow', bold=True))
            return protocol_deployed
        
        while True:
            self.display_contract_list()
            print("\nEnter the number of the contract you want to interact with, or '0' to quit, or 'D' to deploy all undeployed contracts:")
            choice = input("Enter your choice: ").strip().lower()
            
            if choice == 0:
                break
            elif choice == 'd':
                account, wallet_address, balance_eth = self.get_wallet_info()
                if not account:
                    raise ValueError("Private key must be added to .env file in order to deploy.")
                if balance_eth == 0:
                    print("\033[91mError: Your wallet balance is 0 ETH. Please add funds to your wallet before proceeding.\033[0m")
                    print("Returning to previous screen...")
                    return
                
                confirm = click.confirm("Do you want to proceed with the deployment?", default=False)
                if confirm:
                    chain_name = get_chain_name(self.web3.eth.chain_id)
                    print(f'Deploying {key} to {chain_name} ...')
                    self.deploy_all_undeployed_contracts()
                else:
                    print("Deployment cancelled.")
                    continue
            elif choice.isdigit() and 1 <= int(choice) <= len(self.contract_data):
                selected_contract = list(self.contract_data.values())[int(choice)-1]
                self.interact_with_contract(selected_contract)
            else:
                print("Invalid selection. Please try again.")

        return protocol_deployed

    def display_contract_list(self):
        print(f"\n\033[1m{'Contract':<28} | {'Address':<42} | {'Dplyd':<5} | {'Vrfd':<5} | {'Prvdr':<5} \033[0m")
        print("-" * 95)  # Separator line
        for i, (key, data) in enumerate(self.contract_data.items(), 1):
            address = data['address']
            deployed = data['deployed']
            is_set = data['is_set']
            computed_address = data['computed_address']
            is_verified = data['is_verified']
            print(f"{i:2}. {key:<24.24} | {self.color_address(True, self.ZERO_ADDRESS if not computed_address else computed_address):<42} | {emojify(deployed):<4} | {emojify(is_verified):<4} |{emojify(is_set):<4} ")

    def interact_with_contract(self, selected_contract):
        key = selected_contract['key']  # Get the key (contract name)
        data = self.contract_data[key]  # Get the data dictionary
        global_data = V3_PROTOCOL_ADDRESSES[key]
        print(f"\nYou selected: {key}")
        print(f"Mainnet address: {'Not yet deployed' if global_data['address'] == '' else global_data['address']}")
        has_code = False
        if data['computed_address']:
            has_code = has_code_at_address(self.web3, data['computed_address'])
            print(f"Computed deploy address: {data['computed_address']} | {'Already deployed!' if has_code else 'Not yet deployed'} {emojify(has_code)}")
        else:
            print(f"Deployed: {emojify(data['deployed'])}")
        print(f"Source is verified: {emojify(data['is_verified'])}")
        print(f"Address Provider Set: {emojify(data['is_set'])}")
        
        # Add more interactive options here
        print("\nWhat would you like to do?")
        print("1. Deploy")
        print("2. Verify")
        print("3. Go Back")
        
        action = click.prompt("Your choice", type=int)
        
        if action == 1:
            info = V3_PROTOCOL_ADDRESSES[key]
            if data['address'] == '':
                print(f"\033[91m{data['key']} cannot be deployed yet because there is no known address for it on mainnet.\033[0m")
                return
            creation_code = fetch_creation_code(data['address'])
            
            account, wallet_address, balance_eth = self.get_wallet_info()
            if not account:
                raise ValueError("Private key must be added to .env file in order to deploy.")
            if balance_eth == 0:
                print("\033[91mError: Your wallet balance is 0 ETH. Please add funds to your wallet before proceeding.\033[0m")
                print("Returning to previous screen...")
                return

            # Ask for confirmation
            confirm = click.confirm("Do you want to proceed with the deployment?", default=False)

            if confirm:
                chain_name = get_chain_name(self.web3.eth.chain_id)
                print(f'Deploying {key} to {chain_name} ...')
                deploy_create2(self.web3, info['deployer'], info['salt_preimage'], creation_code)
                self.update_contract_data(key)
            else:
                print("Deployment cancelled.")

        elif action == 2:
            if has_code:
                verify_contract(self.web3.eth.chain_id, data['computed_address'], wait_before_request=0)
                self.contract_data[key]['is_verified'] = is_contract_verified(self.web3.eth.chain_id, data['computed_address'])
            else:
                print("Contract not yet deployed. Please deploy the contract first.")
        elif action == 3:
            return
        else:
            print("Invalid choice. Returning to main menu.")

    def update_contract_data(self, key):
        info = V3_PROTOCOL_ADDRESSES[key]
        address = info['address']
        id = self.web3.keccak(text=info['id'])
        try:
            address_from_provider = self.address_provider.functions.getAddress(id).call()
        except Exception as e:
            # print(f"Error fetching address from provider: {str(e)}")
            address_from_provider = None

        computed_address = compute_create2_address(
            self.web3, 
            info['deployer'], 
            0 if not info['salt'] else info['salt'], 
            fetch_creation_code(address)
        )
        deployed = emojify(has_code_at_address(self.web3, computed_address))

        self.contract_data[key] = {
            'key': key,
            'address': address,
            'deployed': deployed,
            'is_set': None if key in ['tokenized_strategy', 'vault_implementation'] else address_from_provider == address,
            'computed_address': computed_address,
            'is_verified': is_contract_verified(self.web3.eth.chain_id, computed_address)
        }

    def get_wallet_info(self, should_print=True):
        private_key = os.getenv('DEPLOYER_PRIVATE_KEY')
        if not private_key:
            print("Error: DEPLOYER_PRIVATE_KEY not found in .env file.")
            return None, None, None

        account = Account.from_key(private_key)
        wallet_address = account.address
        balance = self.web3.eth.get_balance(wallet_address)
        balance_eth = self.web3.from_wei(balance, 'ether')
        if should_print:
            print(f"\nWallet Address: {wallet_address}")
            print(f"Balance: {balance_eth:.4f} ETH")
        return account, wallet_address, balance_eth

    def deploy_protocol(self, chain_name, chain_id):
        print(f"Initiating deployment process for {chain_name}...")
        self.deploy_all_undeployed_contracts(full_deployment=True)
        # self.deploy_contract('init_gov')
        # self.deploy_contract('address_provider')

    def deploy_contract(self, contract_key):
        info = V3_PROTOCOL_ADDRESSES[contract_key]
        salt_preimage = info['salt_preimage']
        address = info['address']
        creation_code = fetch_creation_code(address)
        computed_address = compute_create2_address(self.web3, info['deployer'], info['salt'], creation_code)
        
        if has_code_at_address(self.web3, computed_address):
            print(f'{contract_key.capitalize()} already deployed at {computed_address}!')
        else:
            deploy_create2(self.web3, info['deployer'], salt_preimage, creation_code)

    def color_address(self, is_true, value):
        color = "\033[94m" if is_true else "\033[93m"
        return f"{color}{value}\033[0m"
    
    def deploy_all_undeployed_contracts(self, full_deployment=False):
        print("Deploying all undeployed contracts...")
        to_deploy = []
        if self.contract_data and len(self.contract_data) > 0:
            for contract_name, data in self.contract_data.items():
                if not data['deployed']:
                    if data['address'] == '':
                        # print(f"Skipping {contract_name} , no known address on mainnet.")
                        continue
                    to_deploy.append(data)
        else:
            for contract_name, info in V3_PROTOCOL_ADDRESSES.items():
                if info['address'] == '':
                    continue
                info['key'] = contract_name
                to_deploy.append(info)
        
        if len(to_deploy) == 0:
            print("Eligible contracts have already been deployed! Exiting...")
            return
        
        print(f"\nDetected {len(to_deploy)} contracts to deploy. Please be patient, this may take a while...")
        for i, data in enumerate(to_deploy):
            contract_name = data['key']
            print(f"\nDeploying {contract_name} ({i+1}/{len(to_deploy)})...")
            try:
                self.deploy_contract(contract_name)
                self.update_contract_data(contract_name)
            except Exception as e:
                print(f"Error deploying {contract_name}: {str(e)}")
        print("Finished deploying all undeployed contracts.")

@click.group()
def cli():
    pass

@cli.command()
def cli():
    deployer = YearnV3Deployer()
    deployer.initialize()

    while True:
        chain_id = deployer.select_network()
        if deployer.print_chain_deployment_report():
            break
        else:
            deployer.get_wallet_info(True)
            chain_name = get_chain_name(chain_id)
            deploy_choice = click.confirm(
                f"Would you like to deploy the V3 protocol to {chain_name} (Chain ID: {chain_id})?",
                default=False
            )
            
            if deploy_choice:
                deployer.deploy_protocol(chain_name, chain_id)
            
            break

if __name__ == "__main__":
    cli()
