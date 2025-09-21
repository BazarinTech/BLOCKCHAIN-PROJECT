def proof_of_work(block, difficulty=2):
    while block.hash[:difficulty] != "0" * difficulty:
        block.nonce += 1
        block.hash = block.calculate_hash()
    return block