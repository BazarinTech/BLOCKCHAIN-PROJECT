# Blockchain Project

This is a basic blockchain project implemented in Python. It includes functionalities for proof of work, transaction validation, wallet management, and peer-to-peer synchronization.

## Project Structure

The project is structured as follows:

-   `blockchain/`: Contains the core blockchain logic.
    -   `blockchain.py`: Implements the `Blockchain` class.
    -   `block_module.py`: Defines the `Block` class.
    -   `proof_of_work.py`: Implements the proof-of-work algorithm.
-   `transactions/`: Contains transaction-related logic.
    -   `transaction.py`: Defines the `Transaction` class.
    -   `transaction_validation.py`: Implements transaction validation logic.
-   `wallet/`: Contains wallet management logic.
    -   `wallet.py`: Defines the `Wallet` class.
-   `p2p/`: Contains peer-to-peer synchronization logic.
    -   `p2p_node.py`: Implements the P2P node using Flask.
-   `cli/`: Contains the command-line interface.
    -   `cli.py`: Implements the CLI using `argparse`.
-   `tests/`: Contains tests for the project.
-   `requirements.txt`: Lists the project dependencies.
-   `LICENSE`: Contains the license information (MIT License).
-   `README.md`: This file.

## Features

-   **Proof of Work:** Implemented using a simple difficulty adjustment.
-   **Transaction Validation:** Checks for sufficient balance and valid signatures.
-   **Wallet Management:** Allows creating new wallets.
-   **Peer-to-Peer Sync:** Basic structure with API endpoints for chain and block exchange.

## Dependencies

The project depends on the following Python libraries:

-   `cryptography`
-   `Flask`
-   `requests`

You can install these dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Getting Started

1.  **Clone the repository:**

```bash
git clone [repository_url]
cd [project_directory]
```

2.  **Create a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3.  **Install dependencies:**

```bash
pip install -r requirements.txt
```

4.  **Run the P2P nodes:**

Open three separate terminal windows. In each terminal, activate the virtual environment and run the following commands:

```bash
# Terminal 1 (Port 5000)
PORT=5000 python p2p/p2p_node.py

# Terminal 2 (Port 5001)
PORT=5001 python p2p/p2p_node.py

# Terminal 3 (Port 5002)
PORT=5002 python p2p/p2p_node.py
```

## Usage

### CLI

The `cli.py` file provides a command-line interface for interacting with the blockchain.

-   **Create a wallet:**

```bash
python cli/cli.py --create_wallet
```

-   **Send a transaction:**

```bash
python cli/cli.py --send_transaction <sender_public_key> <recipient_public_key> <amount>
```

-   **Mine a block:**

```bash
python cli/cli.py --mine_block
```

-   **View the blockchain:**

```bash
python cli/cli.py --view_blockchain
```

### API Endpoints

The P2P nodes expose the following API endpoints:

-   `/get_chain`: Returns the current node's blockchain.
-   `/add_block`: Adds a new block to the current node's blockchain.
-   `/add_transaction`: Adds a transaction to the transaction pool.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
