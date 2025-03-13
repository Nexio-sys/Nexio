from web3 import Web3
import json

class BlockchainInterface:
    def __init__(self, provider_url, contract_address, contract_abi):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=contract_abi
        )
    
    def mint_nft(self, wallet_address, token_uri, private_key):
        try:
            nonce = self.w3.eth.get_transaction_count(wallet_address)
            
            # Build transaction
            transaction = self.contract.functions.mintNFT(
                wallet_address,
                token_uri
            ).build_transaction({
                'chainId': 1,  # Ethereum mainnet
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=private_key
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as e:
            print(f"Error minting NFT: {str(e)}")
            return None 