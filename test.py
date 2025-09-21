from blockchain.blockchain import Blockchain
from blockchain.block_module import Block
import time

# Initialize blockchain
blockchain = Blockchain()

# Add some dummy transactions and mine new blocks
timestamp = time.time()
block1 = Block(timestamp, ["Alice pays Bob 10 BTC", "Charlie pays Dave 5 BTC"], blockchain.chain[-1].hash if blockchain.chain else '0')
blockchain.add_block(block1)

timestamp = time.time()
block2 = Block(timestamp, ["Eve pays Frank 2 BTC"], blockchain.chain[-1].hash)
blockchain.add_block(block2)

# Print the blockchain
for idx, block in enumerate(blockchain.chain):
    print(f"Block {idx}:")
    print(f"  Timestamp: {block.timestamp}")
    print(f"  Transactions: {block.transactions}")
    print(f"  Previous Hash: {block.previous_hash}")
    print(f"  Nonce: {block.nonce}")
    print(f"  Hash: {block.hash}")
    print("-" * 40)
