import json
import hashlib
from datetime import datetime

class NFTMetadata:
    def __init__(self):
        self.metadata_template = {
            "name": "",
            "description": "",
            "image": "",
            "attributes": [],
            "created_at": "",
            "generator_params": {},
            "hash": ""
        }
    
    def create_metadata(self, name, description, image_path, attributes, generator_params):
        metadata = self.metadata_template.copy()
        metadata["name"] = name
        metadata["description"] = description
        metadata["image"] = image_path
        metadata["attributes"] = attributes
        metadata["created_at"] = datetime.utcnow().isoformat()
        metadata["generator_params"] = generator_params
        
        # Generate unique hash for the NFT
        content_string = f"{name}{description}{image_path}{str(attributes)}"
        metadata["hash"] = hashlib.sha256(content_string.encode()).hexdigest()
        
        return metadata
    
    def save_metadata(self, metadata, file_path):
        try:
            with open(file_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving metadata: {str(e)}")
            return False 