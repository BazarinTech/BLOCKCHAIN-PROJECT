import os
import sys
sys.path.append(os.getcwd())
from flask import Flask, request, jsonify
from blockchain.blockchain import Blockchain
import json
from transactions.transaction import Transaction
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from cryptography.hazmat.primitives import serialization
from wallet.wallet import Wallet

app = Flask(__name__)

# Get the port from the environment variable, default to 5000
PORT = int(os.environ.get('PORT', 5000))

# Replace with your actual node address
NODE_ADDRESS = f'http://localhost:{PORT}'

# Initialize the blockchain
blockchain = Blockchain()

# Peer list (hardcoded for now)
PEER_NODES = [
    'http://localhost:5000',
    'http://localhost:5001',
    'http://localhost:5002'
]

# Remove self from the peer list
PEER_NODES = [peer for peer in PEER_NODES if peer != NODE_ADDRESS]


def generate_key(password):
    print("Generating key...")
    try:
        password = password.encode()
        salt = b'salt_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
            backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password))
        print("Key generated.")
        return key
    except Exception as e:
        print(f"Error generating key: {e}")
        raise e


def load_wallet(filename, password):
    print("Loading wallet...")
    try:
        with open(filename, 'r') as f:
            print("File opened successfully.")
            data = json.load(f)
            print("JSON loaded successfully.")
            public_key = data['public_key']
            encrypted_private_key = data['encrypted_private_key']

        key = generate_key(password)
        print("Key" + str(key))
        f = Fernet(key)
        print("Fernet" + str(f))
        decrypted_private_key = f.decrypt(encrypted_private_key.encode()).decode().rstrip()
        import os
        import sys
        sys.path.append(os.getcwd())
        from wallet.wallet import Wallet

        private_key = serialization.load_pem_private_key(
            decrypted_private_key.encode(),
            backend=default_backend()
        )
        wallet = Wallet()
        wallet.private_key = private_key
        wallet.public_key = private_key.public_key()
        return wallet, public_key
    except Exception as e:
        print(f"Error in load_wallet: {e}")
        raise e

@app.route('/get_chain', methods=['GET'])
def get_chain():
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
    return jsonify(chain_data)

@app.route('/add_block', methods=['POST'])
def add_block():
    block_data = request.get_json()
    # TODO: Validate the block before adding it
    blockchain.add_block(block_data)
    return jsonify({'message': 'Block added successfully'})

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction_data = request.get_json()
    # Load wallet
    filename = 'wallet.json'
    password = "password123"  #getpass.getpass('Enter password for your wallet: ')
    print("Before loading wallet")
    try:
        wallet, public_key = load_wallet(filename, password)
    except FileNotFoundError:
        return jsonify({'message': 'Wallet file not found. Create a wallet first.'}), 400
    except Exception as e:
        print(f'Error loading wallet: {e}')
        return jsonify({'message': f'Error loading wallet: {e}'}), 500

    # Create a Transaction object from the dictionary
    transaction = Transaction(public_key, transaction_data['recipient'], transaction_data['amount'])

    if blockchain.add_transaction(transaction):
        return jsonify({'message': 'Transaction added successfully'})
    else:
        return jsonify({'message': 'Transaction failed'})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
