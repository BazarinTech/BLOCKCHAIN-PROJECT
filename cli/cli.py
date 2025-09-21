import argparse
import sys
import os
sys.path.append(os.getcwd())
from wallet.wallet import Wallet
from transactions.transaction import Transaction
from blockchain.blockchain import Blockchain
import json
import getpass  # For password prompting
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from cryptography.hazmat.primitives import serialization


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)


def generate_key(password):
    print("Generating key...")
    password = password.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    print("Key generated.")
    return key


def save_wallet(wallet, filename, password):
    print("Saving wallet...")  # Debugging print
    private_key_bytes = wallet.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key = private_key_bytes.decode()
    key = generate_key(password)
    f = Fernet(key)
    encrypted_private_key = f.encrypt(private_key.encode()).decode()

    with open(filename, 'w') as f:
        json.dump({'public_key': wallet.get_public_key(), 'encrypted_private_key': encrypted_private_key.encode().decode('utf-8')}, f)
    print("Wallet saved.")  # Debugging print


def load_wallet(filename, password):
    print("Loading wallet...")  # Debugging print
    with open(filename, 'r') as f:
        data = json.load(f)
        public_key = data['public_key']
        encrypted_private_key = data['encrypted_private_key']

    key = generate_key(password)
    f = Fernet(key)
    decrypted_private_key = f.decrypt(encrypted_private_key.encode()).decode()

    private_key = serialization.load_pem_private_key(
        decrypted_private_key.encode(),
        password=None,
        backend=default_backend()
    )
    wallet = Wallet()
    wallet.private_key = private_key
    wallet.public_key = private_key.public_key()
    return wallet, public_key


parser = argparse.ArgumentParser(description='Blockchain CLI')
parser.add_argument('--create_wallet', action='store_true', help='Create a new wallet')
parser.add_argument('--send_transaction', nargs=3, metavar=('sender', 'recipient', 'amount'), help='Send a transaction')
parser.add_argument('--mine_block', action='store_true', help='Mine a new block')
parser.add_argument('--view_blockchain', action='store_true', help='View the blockchain')

args = parser.parse_args()

if args.create_wallet:
    print("Creating wallet...")  # Debugging print
    wallet = Wallet()
    print("Wallet created.")  # Debugging print
    filename = 'wallet.json'
    password = getpass.getpass('Enter a password to protect your wallet: ')
    save_wallet(wallet, filename, password)
    print(f'Wallet saved to {filename}')
    print(f'Public Key: {wallet.get_public_key()}')

elif args.send_transaction:
    sender, recipient, amount = args.send_transaction
    amount = int(amount)

    filename = 'wallet.json'
    password = getpass.getpass('Enter password for your wallet: ')
    try:
        wallet, public_key = load_wallet(filename, password)
    except FileNotFoundError:
        print('Wallet file not found.  Create a wallet first.')
        sys.exit(1)
    except Exception as e:
        print(f'Error loading wallet: {e}')
        sys.exit(1)

    transaction = Transaction(sender, recipient, amount)
    transaction.sign_transaction(wallet.private_key)

    blockchain = Blockchain()
    if blockchain.add_transaction(transaction):
        print(f'Sending {amount} from {sender} to {recipient}')
    else:
        print('Transaction failed')

elif args.mine_block:
    blockchain = Blockchain()
    miner_wallet = Wallet()
    block = blockchain.mine_block(miner_wallet.get_public_key())
    print('Mining a new block...')
    print(f'Block Hash: {block.hash}')

elif args.view_blockchain:
    blockchain = Blockchain()
    chain_data = []
    for block in blockchain.chain:
        block_data = {
            'timestamp': block.timestamp,
            'transactions': str(block.transactions),
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
        }
        chain_data.append(block_data)
    print('Viewing the blockchain...')
    print(json.dumps(chain_data, indent=4, cls=CustomEncoder))
