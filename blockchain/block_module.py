class Block:
    def __init__(self, timestamp, transactions, previous_hash, nonce=0):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        if not hasattr(self, 'nonce'):
            self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        import hashlib
        nonce = self.nonce
        data = str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(nonce)
        return hashlib.sha256(data.encode()).hexdigest()