import time
from .block_module import Block
from .proof_of_work import proof_of_work
from transactions.transaction import Transaction
from transactions.transaction_validation import validate_transaction
from wallet.wallet import Wallet
import json
import os

class Blockchain:
    def __init__(self, chain_file='blockchain.json'):
        self.chain_file = chain_file
        self.chain = self.load_chain()
        self.difficulty = 2
        self.transaction_pool = []
        self.genesis_wallet = Wallet()

    def create_genesis_block(self):
        # Manually construct a genesis block with index 0 and arbitrary previous hash
        return Block(0, [], "0", 0)

    def add_transaction(self, transaction):
        if validate_transaction(transaction, self):
            self.transaction_pool.append(transaction)
            return True
        return False

    def mine_block(self, miner_address):
        transactions = self.transaction_pool[:]
        self.transaction_pool = []

        timestamp = time.time()
        previous_hash = self.chain[-1].hash if self.chain else '0'
        new_block = Block(timestamp, transactions, previous_hash, 0)
        new_block = proof_of_work(new_block, self.difficulty)
        self.chain.append(new_block)
        self.save_chain()
        reward_transaction = Transaction('GENESIS', miner_address, 1)
        reward_transaction.sign_transaction(self.genesis_wallet.private_key)
        self.add_transaction(reward_transaction)
        return new_block

    def add_block(self, block):
        # Convert the block data to a Block object
        block = Block(block['timestamp'], block['transactions'], block['previous_hash'], block['nonce'])
        block.previous_hash = self.chain[-1].hash
        block.hash = block.calculate_hash()
        self.chain.append(block)
        self.save_chain()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.is_chain_valid():
            self.chain = new_chain
            self.save_chain()
            return True
        return False

    def load_chain(self):
        if os.path.exists(self.chain_file):
            with open(self.chain_file, 'r') as f:
                chain_data = json.load(f)
                chain = []
                for block_data in chain_data:
                    block = Block(block_data['timestamp'], block_data['transactions'], block_data['previous_hash'], block_data['nonce'])
                    chain.append(block)
                return chain
        else:
            return [self.create_genesis_block()]

    def save_chain(self):
        chain_data = []
        for block in self.chain:
            block_data = {
                'timestamp': block.timestamp,
                'transactions': block.transactions,
                'previous_hash': block.previous_hash,
                'hash': block.hash,
                'nonce': block.nonce
            }
            chain_data.append(block_data)

        with open(self.chain_file, 'w') as f:
            json.dump(chain_data, f)