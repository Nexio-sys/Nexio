import requests
import json
from pathlib import Path

class IPFSHandler:
    def __init__(self, pinata_api_key, pinata_secret_key):
        self.pinata_api_key = pinata_api_key
        self.pinata_secret_key = pinata_secret_key
        self.headers = {
            'pinata_api_key': pinata_api_key,
            'pinata_secret_api_key': pinata_secret_key
        }
        self.pin_endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        self.json_endpoint = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    def upload_file(self, file_path):
        try:
            with Path(file_path).open("rb") as fp:
                files = {
                    'file': fp
                }
                response = requests.post(
                    self.pin_endpoint,
                    files=files,
                    headers=self.headers
                )
                if response.status_code == 200:
                    return f"ipfs://{response.json()['IpfsHash']}"
                return None
        except Exception as e:
            print(f"Error uploading to IPFS: {str(e)}")
            return None

    def upload_metadata(self, metadata):
        try:
            response = requests.post(
                self.json_endpoint,
                json=metadata,
                headers=self.headers
            )
            if response.status_code == 200:
                return f"ipfs://{response.json()['IpfsHash']}"
            return None
        except Exception as e:
            print(f"Error uploading metadata to IPFS: {str(e)}")
            return None 