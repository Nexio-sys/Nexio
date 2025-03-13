from art_generator import AIArtGenerator
from nft_metadata import NFTMetadata
from blockchain_interface import BlockchainInterface
from ipfs_handler import IPFSHandler
import os
import json
from pathlib import Path
from utils.config_validator import ConfigValidator
from utils.config_manager import ConfigManager
from utils.helpers import NFTUtils, PromptHelper
import logging
from typing import Optional, Dict, Any

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ['output', 'config']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def load_config(config_path):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return None

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_configurations(config_validator: ConfigValidator) -> Optional[Dict[str, Any]]:
    """Load all configurations"""
    configs = {}
    
    # Load blockchain config
    blockchain_config = config_validator.load_and_validate_config(
        "config/blockchain_config.json",
        "blockchain"
    )
    if not blockchain_config:
        return None
    configs["blockchain"] = blockchain_config
    
    # Load IPFS config
    ipfs_config = config_validator.load_and_validate_config(
        "config/ipfs_config.json",
        "ipfs"
    )
    if not ipfs_config:
        return None
    configs["ipfs"] = ipfs_config
    
    return configs

def generate_nft_collection(
    art_generator: AIArtGenerator,
    prompt: str,
    num_variations: int,
    style_params: Dict[str, Any]
) -> list:
    """Generate a collection of NFT images"""
    return art_generator.generate_variations(prompt, num_variations, style_params)

def main():
    # Setup logging
    logger = setup_logging()
    logger.info("Starting NFT generation process")
    
    # Setup directories
    setup_directories()
    
    # Setup configuration
    config_manager = ConfigManager()
    config_manager.create_default_configs()  # Create default configs if they don't exist
    
    configs = config_manager.load_all_configs()
    if not configs:
        logger.error("Failed to load configurations")
        return
    
    # Initialize utilities
    nft_utils = NFTUtils()
    prompt_helper = PromptHelper()
    
    try:
        # Initialize components
        art_generator = AIArtGenerator(configs["art"]["model_path"])
        nft_metadata = NFTMetadata()
        ipfs_handler = IPFSHandler(
            configs["ipfs"]["pinata_api_key"],
            configs["ipfs"]["pinata_secret_key"]
        )
        
        blockchain = BlockchainInterface(
            configs["blockchain"]["provider_url"],
            configs["blockchain"]["contract_address"],
            configs["blockchain"]["contract_abi"]
        )
        
        # Generate NFT collection
        prompt = "A futuristic cityscape with floating islands and neon lights"
        style_params = {
            'height': 512,
            'width': 512,
            'num_inference_steps': 50,
            'guidance_scale': 7.5,
            'seed': 42,  # Set seed for reproducibility
            'negative_prompt': "blurry, low quality, distorted"
        }
        
        images = generate_nft_collection(art_generator, prompt, num_variations=4, style_params=style_params)
        
        # Process each generated image
        for i, image in enumerate(images, 1):
            if image:
                # Save the generated image
                image_path = f"output/generated_art_{i}.png"
                art_generator.save_image(image, image_path)
                
                # Upload image to IPFS
                image_ipfs_uri = ipfs_handler.upload_file(image_path)
                if not image_ipfs_uri:
                    logger.error(f"Failed to upload image {i} to IPFS")
                    continue
                
                # Create metadata
                attributes = [
                    {"trait_type": "Style", "value": "Futuristic"},
                    {"trait_type": "Theme", "value": "Cityscape"},
                    {"trait_type": "AI Model", "value": "Stable Diffusion"},
                    {"trait_type": "Variation", "value": str(i)}
                ]
                
                metadata = nft_metadata.create_metadata(
                    name=f"AI Generated Futuristic City #{i}",
                    description="A stunning AI-generated artwork featuring a futuristic cityscape",
                    image_path=image_ipfs_uri,
                    attributes=attributes,
                    generator_params=style_params
                )
                
                # Upload metadata to IPFS
                metadata_ipfs_uri = ipfs_handler.upload_metadata(metadata)
                if not metadata_ipfs_uri:
                    logger.error(f"Failed to upload metadata {i} to IPFS")
                    continue
                
                # Mint NFT
                wallet_address = configs["blockchain"]["wallet_address"]
                private_key = configs["blockchain"]["private_key"]
                
                receipt = blockchain.mint_nft(wallet_address, metadata_ipfs_uri, private_key)
                if receipt:
                    logger.info(f"NFT #{i} minted successfully!")
                    logger.info(f"Transaction hash: {receipt['transactionHash'].hex()}")
                    logger.info(f"Image IPFS URI: {image_ipfs_uri}")
                    logger.info(f"Metadata IPFS URI: {metadata_ipfs_uri}")
                else:
                    logger.error(f"Failed to mint NFT #{i}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return

if __name__ == "__main__":
    main() 