# NEXIO - AI-Powered NFT Generation Platform

## Overview

NEXIO is a powerful Python-based platform that combines AI technology with blockchain to create, manage, and mint unique NFT collections. The platform leverages Stable Diffusion for AI art generation and integrates with solana blockchain for NFT minting.

## Features

- **AI Art Generation**

  - Utilizes Stable Diffusion model for high-quality image generation
  - Supports multiple art styles (realistic, anime, abstract, digital)
  - Customizable generation parameters
  - Batch generation capability

- **NFT Management**

  - Automated metadata generation
  - IPFS integration for decentralized storage
  - Unique hash generation for each NFT
  - Comprehensive attribute management

- **Blockchain Integration**

  - Direct minting to Ethereum blockchain
  - Smart contract interaction
  - Transaction management
  - Wallet integration

- **Advanced Features**
  - Configurable prompt enhancement
  - Automatic file organization
  - Detailed generation logging
  - Error handling and recovery

## Requirements

- Python 3.8+
- PyTorch
- Web3.py
- Stable Diffusion
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

```bash
cd NEXIO
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your environment:

- Copy example configuration files
- Update with your credentials
- Set up your Ethereum wallet
- Configure IPFS (Pinata) access

## Configuration

The project uses three main configuration files:

1. `config/blockchain_config.json`:

```json
{
  "provider_url": "your-ethereum-node-url",
  "contract_address": "your-contract-address",
  "wallet_address": "your-wallet-address",
  "private_key": "your-private-key"
}
```

2. `config/ipfs_config.json`:

```json
{
  "pinata_api_key": "your-pinata-api-key",
  "pinata_secret_key": "your-pinata-secret-key"
}
```

3. `config/art_config.json`:

```json
{
  "model_path": "path/to/model",
  "default_style": {
    "height": 512,
    "width": 512,
    "num_inference_steps": 50,
    "guidance_scale": 7.5
  }
}
```

## Usage

1. Basic usage:

```python
python src/main.py
```

2. Custom prompt generation:

```python
python src/main.py --prompt "Your custom prompt" --style realistic
```

3. Batch generation:

```python
python src/main.py --batch-size 4 --variations 3
```

## Project Structure

```
NEXIO/
├── src/
│   ├── art_generator.py
│   ├── blockchain_interface.py
│   ├── ipfs_handler.py
│   ├── nft_metadata.py
│   ├── main.py
│   └── utils/
│       ├── config_manager.py
│       ├── config_validator.py
│       └── helpers.py
├── config/
│   ├── blockchain_config.json
│   ├── ipfs_config.json
│   └── art_config.json
├── output/
├── logs/
└── README.md
```

## Best Practices

- Always backup your private keys and configuration files
- Test with small transactions on testnet first
- Monitor gas prices for optimal minting costs
- Regularly update dependencies for security
- Use strong prompts for better art generation

## Troubleshooting

Common issues and solutions:

1. **Connection Issues**: Verify your Ethereum node URL and internet connection
2. **IPFS Errors**: Check Pinata API credentials and rate limits
3. **Generation Failures**: Ensure model path is correct and GPU has sufficient memory
4. **Minting Errors**: Verify wallet balance and contract permissions

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Contact

[Twitter](https://x.com/nexionft)

## Acknowledgments

- Stable Diffusion team for the AI model
- OpenZeppelin for smart contract templates
- IPFS/Pinata for decentralized storage
- The Ethereum community

## Future Plans

- Integration with more blockchain networks
- Additional AI models support
- Enhanced prompt engineering
- Batch processing improvements
- GUI interface development

---

**Note**: This project is for educational purposes. Always do your own research and use at your own risk when dealing with Cryptocurrencies and NFTs.
