def validate_transaction(transaction, blockchain):
    if transaction.sender == 'GENESIS':
        return True

    sender_balance = get_balance(transaction.sender, blockchain)
    if sender_balance < transaction.amount:
        return False

    public_key = transaction.sender

    return transaction.verify_transaction(public_key)

def get_balance(public_key, blockchain):
    balance = 0
    for block in blockchain.chain:
        for transaction in block.transactions:
            if transaction.sender == public_key:
                balance -= transaction.amount
            if transaction.recipient == public_key:
                balance += transaction.amount
    return balance