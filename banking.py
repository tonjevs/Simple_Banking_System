from flask import Flask, request, jsonify
from threading import Lock
import sqlite3

app = Flask(__name__)
lock = Lock()

DATABASE_PATH = "bank_data.db"

def make_tables(): 
    """
    Create tables for accounts and transactions in the database if they don't exist.
    Inserting some sample accounts into the 'accounts' table.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                availableCash REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                registeredTime INTEGER,
                executedTime INTEGER,
                success INTEGER,
                cashAmount REAL,
                sourceAccountId INTEGER,
                destinationAccountId INTEGER,
                FOREIGN KEY (sourceAccountId) REFERENCES accounts (id),
                FOREIGN KEY (destinationAccountId) REFERENCES accounts (id)
            )
        """)
        sample_accounts = [
            ("Account1", 100.0),
            ("Account2", 52.0),
            ("Account3", 203.0),
            ("Account4", 604.0),
            ("Account5", 99.0),
            ("Account6", 204.0)
        ]

        for name, available_cash in sample_accounts:
            cursor.execute("SELECT * FROM accounts WHERE name = ?", (name,))
            existing_account = cursor.fetchone()

            if existing_account:
                # Update existing account
                cursor.execute("UPDATE accounts SET availableCash = ? WHERE id = ?", (available_cash, existing_account[0]))
            else:
                # Insert new account
                cursor.execute("INSERT INTO accounts (name, availableCash) VALUES (?, ?)", (name, available_cash))

        conn.commit()

def get_account_by_id(cursor, account_id):
    """
    Retrieve an account from the 'accounts' table based on the provided account ID.

    Parameters:
    - cursor: SQLite database cursor
    - account_id: ID of the account to retrieve

    Returns:
    - Account data (as a tuple) if found, otherwise None
    """
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    return cursor.fetchone()

def update_account_balance(cursor, account_id, balance): 
    """
    Update the available cash balance of an account in the 'accounts' table.

    Parameters:
    - cursor: SQLite database cursor
    - account_id: ID of the account to update
    - balance: New available cash balance
    """
    cursor.execute("UPDATE accounts SET availableCash = ? WHERE id = ?",(balance,account_id,))

def execute_transaction(transaction_data): 
    """
    Execute a financial transaction between two bank accounts.

    Parameters:
    - transaction_data (dict): Transaction details, including source and destination accounts.

    Returns:
    - tuple: Tuple containing a JSON response and an HTTP status code.
    """
    try: 
        with lock:
            with sqlite3.connect(DATABASE_PATH) as conn:
                cursor = conn.cursor()

                for transaction in transaction_data["transactions"]:
                    
                    if "sourceAccount" not in transaction or "destinationAccount" not in transaction:
                        return jsonify({"error": "Invalid transaction format"}), 400

                    source_account_id = get_account_by_id(cursor, transaction["sourceAccount"]["id"])
                    destination_account_id = get_account_by_id(cursor, transaction["destinationAccount"]["id"])

                    if source_account_id is None or destination_account_id is None:
                        return jsonify({"error": "Invalid account information"}), 400

                    if source_account_id[2] < transaction.get("cashAmount", 0) or transaction.get("cashAmount", 0) < 0:
                        return jsonify({"error": f"Insufficient fund for account {source_account_id[1]} to {destination_account_id[1]}"}), 400
                    
                    update_account_balance(cursor, transaction["sourceAccount"]["id"], source_account_id[2] - transaction.get("cashAmount", 0))
                    update_account_balance(cursor, transaction["destinationAccount"]["id"], destination_account_id[2] + transaction.get("cashAmount", 0))

                    cursor.execute("""
                        INSERT INTO transactions
                        (registeredTime, executedTime, success, cashAmount, sourceAccountId, destinationAccountId)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        transaction.get("registeredTime", 0),
                        transaction.get("executedTime", 0),
                        1,  
                        transaction.get("cashAmount", 0),
                        source_account_id[0],
                        destination_account_id[0]
                    ))
                    conn.commit()
                
        return jsonify({"success": True}), 200
    except Exception as e: 
        return jsonify({"error":"Internal server error"}),500

@app.route("/api/executeTransaction", methods=["POST"])
def write_to(): 
    """
    Handle HTTP POST requests to execute financial transactions.

    Returns:
    - tuple: Tuple containing a JSON response and an HTTP status code.
    """
    try: 
        transaction_data = request.json
        result, status_code = execute_transaction(transaction_data)
        return result, status_code
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    make_tables()
    app.run(debug=True, port=5001)
