import argparse
from typing import Dict, Any

def parse_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description='AI NFT Generator')
    
    parser.add_argument(
        '--prompt',
        type=str,
        help='Text prompt for generating artwork'
    )
    
    parser.add_argument(
        '--variations',
        type=int,
        default=1,
        help='Number of variations to generate (default: 1)'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=512,
        help='Width of generated image (default: 512)'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=512,
        help='Height of generated image (default: 512)'
    )
    
    parser.add_argument(
        '--steps',
        type=int,
        default=50,
        help='Number of inference steps (default: 50)'
    )
    
    parser.add_argument(
        '--guidance-scale',
        type=float,
        default=7.5,
        help='Guidance scale for generation (default: 7.5)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    
    parser.add_argument(
        '--negative-prompt',
        type=str,
        help='Negative prompt to avoid certain features'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Generate images without minting NFTs'
    )
    
    parser.add_argument(
        '--setup-config',
        action='store_true',
        help='Create default configuration files'
    )
    
    return vars(parser.parse_args()) 