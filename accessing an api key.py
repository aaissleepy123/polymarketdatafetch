import os
from py_clob_client.client import ClobClient
from dotenv import load_dotenv
load_dotenv('keys.env')

# Load the environment variables from the specified .env file
key = os.getenv("PK")
print("Loaded PK:", key)

def main():
    host = "https://clob.polymarket.com/"
    key = os.getenv("PK")
    chain_id = 137  # Polygon Mainnet chain ID

    # Ensure the private key is loaded correctly
    if not key:
        raise ValueError("Private key not found. Please set PK in the environment variables.")

    # Initialize the client with your private key
    client = ClobClient(host, key=key, chain_id=chain_id)

    # Create or derive API credentials
    try:
        api_creds = client.create_or_derive_api_creds()
        print("API Key:", api_creds.api_key)
        print("Secret:", api_creds.api_secret)
        print("Passphrase:", api_creds.api_passphrase)

        # Save these securely in a secure environment
    except Exception as e:
        print("Error creating or deriving API credentials:", e)

if __name__ == "__main__":
    main()
