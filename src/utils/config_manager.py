import json
from pathlib import Path
import logging
from typing import Dict, Any, Optional
from .config_validator import ConfigValidator

class ConfigManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validator = ConfigValidator()
        self.config_dir = Path("config")
        
        # Default configuration templates
        self.default_blockchain_config = {
            "provider_url": "https://mainnet.infura.io/v3/YOUR-PROJECT-ID",
            "contract_address": "0xYourContractAddress",
            "contract_abi": [
                {
                    "inputs": [
                        {
                            "internalType": "address",
                            "name": "recipient",
                            "type": "address"
                        },
                        {
                            "internalType": "string",
                            "name": "tokenURI",
                            "type": "string"
                        }
                    ],
                    "name": "mintNFT",
                    "outputs": [
                        {
                            "internalType": "uint256",
                            "name": "",
                            "type": "uint256"
                        }
                    ],
                    "stateMutability": "nonpayable",
                    "type": "function"
                }
            ],
            "wallet_address": "0xYourWalletAddress",
            "private_key": "your-private-key"
        }
        
        self.default_ipfs_config = {
            "pinata_api_key": "your-pinata-api-key",
            "pinata_secret_key": "your-pinata-secret-key"
        }
        
        self.default_art_config = {
            "model_path": "path/to/model",
            "default_style": {
                "height": 512,
                "width": 512,
                "num_inference_steps": 50,
                "guidance_scale": 7.5,
                "negative_prompt": "blurry, low quality, distorted"
            },
            "output_format": "png",
            "batch_size": 4
        }
    
    def create_default_configs(self) -> None:
        """Create default configuration files if they don't exist"""
        self.config_dir.mkdir(exist_ok=True)
        
        configs = {
            "blockchain_config.json": self.default_blockchain_config,
            "ipfs_config.json": self.default_ipfs_config,
            "art_config.json": self.default_art_config
        }
        
        for filename, default_config in configs.items():
            config_path = self.config_dir / filename
            if not config_path.exists():
                try:
                    with config_path.open('w') as f:
                        json.dump(default_config, f, indent=4)
                    self.logger.info(f"Created default configuration: {filename}")
                except Exception as e:
                    self.logger.error(f"Error creating {filename}: {str(e)}")
    
    def load_all_configs(self) -> Optional[Dict[str, Any]]:
        """Load and validate all configuration files"""
        configs = {}
        
        # Load blockchain config
        blockchain_config = self.validator.load_and_validate_config(
            str(self.config_dir / "blockchain_config.json"),
            "blockchain"
        )
        if not blockchain_config:
            return None
        configs["blockchain"] = blockchain_config
        
        # Load IPFS config
        ipfs_config = self.validator.load_and_validate_config(
            str(self.config_dir / "ipfs_config.json"),
            "ipfs"
        )
        if not ipfs_config:
            return None
        configs["ipfs"] = ipfs_config
        
        # Load art config
        try:
            with (self.config_dir / "art_config.json").open('r') as f:
                configs["art"] = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading art configuration: {str(e)}")
            return None
        
        return configs
    
    def update_config(self, config_type: str, updates: Dict[str, Any]) -> bool:
        """Update specific configuration file"""
        config_file = self.config_dir / f"{config_type}_config.json"
        try:
            # Load existing config
            with config_file.open('r') as f:
                config = json.load(f)
            
            # Update config
            config.update(updates)
            
            # Validate updated config
            if config_type in ["blockchain", "ipfs"]:
                is_valid = getattr(self.validator, f"validate_{config_type}_config")(config)
                if not is_valid:
                    return False
            
            # Save updated config
            with config_file.open('w') as f:
                json.dump(config, f, indent=4)
            
            self.logger.info(f"Updated {config_type} configuration")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating {config_type} configuration: {str(e)}")
            return False 