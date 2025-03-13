import json
from pathlib import Path
import logging
from typing import Dict, Any, Optional

class ConfigValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def validate_blockchain_config(self, config: Dict[str, Any]) -> bool:
        """Validate blockchain configuration"""
        required_fields = [
            "provider_url",
            "contract_address",
            "contract_abi",
            "wallet_address",
            "private_key"
        ]
        
        return self._validate_config(config, required_fields, "blockchain")
    
    def validate_ipfs_config(self, config: Dict[str, Any]) -> bool:
        """Validate IPFS configuration"""
        required_fields = [
            "pinata_api_key",
            "pinata_secret_key"
        ]
        
        return self._validate_config(config, required_fields, "IPFS")
    
    def _validate_config(self, config: Dict[str, Any], required_fields: list, config_name: str) -> bool:
        """Generic configuration validator"""
        if not config:
            self.logger.error(f"Empty {config_name} configuration")
            return False
            
        for field in required_fields:
            if field not in config:
                self.logger.error(f"Missing required field '{field}' in {config_name} configuration")
                return False
            if not config[field]:
                self.logger.error(f"Empty value for required field '{field}' in {config_name} configuration")
                return False
                
        return True
    
    def load_and_validate_config(self, config_path: str, config_type: str) -> Optional[Dict[str, Any]]:
        """Load and validate configuration file"""
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                self.logger.error(f"Configuration file not found: {config_path}")
                return None
                
            with config_file.open('r') as f:
                config = json.load(f)
                
            if config_type == "blockchain":
                is_valid = self.validate_blockchain_config(config)
            elif config_type == "ipfs":
                is_valid = self.validate_ipfs_config(config)
            else:
                self.logger.error(f"Unknown configuration type: {config_type}")
                return None
                
            if is_valid:
                return config
            return None
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            return None 