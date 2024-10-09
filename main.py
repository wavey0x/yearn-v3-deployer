import json
import requests
import click
from web3 import Web3
import os
from eth_abi import encode
from constants import REPOSITORIES, CREATE_X_ADDRESS, INIT_GOV, REPO_ADAPTERS
from repo_adapters import yearn_vaults_v3
import importlib
from utils import has_code_at_address

release_data = {}
chain_id = 0
web3 = None

@click.group()
def cli():
    pass

def handle_rpc(rpc=None):
    global web3
    while not rpc or rpc is None:
        print("No RPC URL provided.")
        rpc = click.prompt('Please provide an RPC URL')

    web3 = Web3(Web3.HTTPProvider(rpc))

    while not web3.is_connected():
        print("Failed to connect to the provided RPC URL.")
        rpc = click.prompt('Please provide a valid RPC URL')
        web3 = Web3(Web3.HTTPProvider(rpc))

    print(f"Connected to chain ID {web3.eth.chain_id} | {rpc}")
    return web3

# Step 1: CLI to get RPC URL, Chain ID, and GitHub URL
@cli.command()
@click.option('--rpc', help='The RPC URL of the target EVM chain.', default=None)
def deploy_protocol(rpc):
    global web3
    global release_data
    rpc = os.getenv('ETH_RPC')
    while web3 is None:
        web3 = handle_rpc(rpc)

    if not web3.is_connected():
        print("Failed to connect to the provided RPC URL.")
        return
    
    print('\n--- Repositories ---')

    for i, repo in enumerate(REPOSITORIES.keys(), 1):
        click.echo(f"{i}. {repo}")

    repo_selection = click.prompt("\nInput the index of the repository you want to use", type=int)

    # Validate the selection
    while repo_selection < 1 or repo_selection > len(REPOSITORIES):
        click.echo("Invalid selection. Please try again.")
        repo_selection = click.prompt("Input the index of the repository you want to use", type=int)
    
    selected_repo = list(REPOSITORIES.keys())[repo_selection - 1]

    # Dynamically import the correct adapter
    adapter_module_name = REPO_ADAPTERS.get(selected_repo)
    if not adapter_module_name:
        click.echo(f"No adapter found for repository: {selected_repo}")
        return
    
    try:
        adapter_module = importlib.import_module(f'repo_adapters.{adapter_module_name}')
    except ImportError:
        click.echo(f"Failed to import adapter for repository: {selected_repo}")
        return
    
    click.echo(f"You selected: {selected_repo}. Adapter loaded successfully.")

    # Update the GITHUB_URL with the selected repository
    latest_release = check_latest_release(selected_repo)
    selected_release = latest_release
    

    
    click.echo(f"Using latest release: {selected_release}")

    # Get release data
    release_data = download_release_data(selected_repo, selected_release)
    if release_data is None:
        print("Failed to download release data.")
        return
    

    contract_data = release_data['contracts']
    for contract_name, data in contract_data.items():
        deployment_address = adapter_module.compute_deployment_address(contract_name, data, selected_release)
        has_code = has_code_at_address(deployment_address)
        if has_code:
            click.echo(f"\u2705 {contract_name}: {deployment_address}")
        else:
            click.echo(f"\u2611 {contract_name}: {deployment_address}")

    # https://guest:guest@eth.wavey.info
    # bytecode = contract_data.get('deployment_bytecode')
    # abi = contract_data.get('abi')

    # if not contract_data or not bytecode or not abi:
    #     print("Invalid contract data: missing bytecode or ABI.")
    #     return




def get_releases():
    return [item for item in release_data['releases']]


    

def download_release_data(selected_repo, selected_release):
    """Download the release data from GitHub."""
    url = f'https://github.com/{REPOSITORIES[selected_repo]}/releases/download/{selected_release}/release_data.json'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        return response.json()['releases'][selected_release]
    except requests.RequestException as e:
        print(f"Error downloading contract data: {e}")
        return None
    





def cache_deployment_info(chain_id, contract_address, cache_file='deployments.json'):
    """Cache deployment addresses in a local file."""
    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    data[chain_id] = contract_address
    
    with open(cache_file, 'w') as f:
        json.dump(data, f)


def transform_to_abi(constructor_args):
    abi = [{
        "type": "constructor",
        "inputs": [
            {"name": key, "type": value}
            for key, value in constructor_args.items()
        ]
    }]
    return json.dumps(abi, indent=2)

def check_latest_release(selected_repo):
    tag_url = f'https://api.github.com/repos/{REPOSITORIES[selected_repo]}/tags'
    response = requests.get(tag_url)
    if response.status_code != 200:
        click.echo(f"Failed to fetch tags from GitHub. Status code: {response.status_code}")
        return
    tags = response.json()
    if not tags:
        click.echo("No tags found for the selected repository.")
        return
    
    valid_tags = [tag for tag in tags if '-' not in tag['name'] and 'beta' not in tag['name'].lower()]
    if not valid_tags:
        click.echo("No valid tags found for the selected repository.")
        return None
    latest_tag = sorted(valid_tags, key=lambda x: x['name'], reverse=True)[0]
    latest_version = latest_tag['name']

    url = f'https://github.com/{REPOSITORIES[selected_repo]}/releases/download/{latest_version}/release_data.json'
    response = requests.get(url)
    if response.status_code != 200:
        click.echo(f"No release data found for {latest_version}. Status code: {response.status_code}")
        return
    
    return latest_version

if __name__ == "__main__":
    cli()