import os
import subprocess
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# --- Configuration ---
VAULT_URL = "https://<your-keyvault-name>.vault.azure.net/"
SNOW_INSTANCE = "https://<your-instance>.service-now.com"
SNOW_TABLE_URL = f"{SNOW_INSTANCE}/api/now/table/incident"

def get_secrets():
    """Fetches credentials securely from Azure Key Vault."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=VAULT_URL, credential=credential)
    
    username = client.get_secret("SNOW-USER").value
    password = client.get_secret("SNOW-PWD").value
    return username, password

def create_snow_incident(user, pwd, short_description):
    """Sends a POST request to ServiceNow Table API."""
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "short_description": short_description,
        "comments": "Automated entry via Azure Python SDK"
    }
    
    response = requests.post(
        SNOW_TABLE_URL, 
        auth=(user, pwd), 
        headers=headers, 
        json=payload
    )
    
    if response.status_code == 201:
        print("Successfully created ServiceNow incident.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# --- Git Automation ---
def git_push(commit_message):
    """Automates the Git Add, Commit, and Push process."""
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Code successfully pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}")

if __name__ == "__main__":
    # 1. Integration Logic
    # user, pwd = get_secrets()
    # create_snow_incident(user, pwd, "Azure Automation Test")
    
    # 2. Upload to Git
    git_push("Add ServiceNow Azure integration script")