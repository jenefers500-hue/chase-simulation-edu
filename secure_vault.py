import sqlite3
import pandas as pd
from datetime import datetime
import theme_config as cfg

class SimulatedChaseEngine:
    def __init__(self):
        self.db_path = "chase_simulation.db"
        self._bootstrap_vault()

    def _execute(self, query, params=(), is_select=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if is_select:
                data = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]
                return pd.DataFrame(data, columns=cols)
            conn.commit()

    def _bootstrap_vault(self):
        self._execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY,
                account_name TEXT NOT NULL,
                balance REAL NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        self._execute('''
            CREATE TABLE IF NOT EXISTS ledger (
                transaction_id TEXT PRIMARY KEY,
                date TEXT NOT NULL,
                account_id TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                running_balance REAL NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts (account_id)
            )
        ''')

        check_empty = self._execute("SELECT COUNT(*) as count FROM accounts", is_select=True)
        if check_empty.empty or check_empty.iloc[0]['count'] == 0:
            for acc in cfg.DEFAULT_ACCOUNTS:
                self._execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", (acc['id'], acc['name'], acc['balance'], acc['type']))

            for tx in cfg.DEFAULT_HISTORY:
                self._execute(
                    """INSERT INTO ledger (transaction_id, date, account_id, description, category, amount, status, running_balance) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (tx['transaction_id'], tx['date'], "CHASE-CHKP-4321", tx['description'], tx['category'], tx['amount'], tx['status'], tx['running_balance'])
                )

    def get_accounts_summary(self):
        return self._execute("SELECT * FROM accounts", is_select=True)

    def get_transaction_ledger(self):
        q = """
            SELECT l.transaction_id, l.date, a.account_name, l.description, l.category, l.amount, l.status, l.running_balance 
            FROM ledger l
            JOIN accounts a ON l.account_id = a.account_id
            ORDER BY l.date DESC
        """
        return self._execute(q, is_select=True)

    def record_transaction(self, account_id, description, category, amount, tx_type):
        now_str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        txn_id = f"TXN-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        acc_info = self._execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,), is_select=True)
        current_bal = acc_info.iloc[0]['balance'] if not acc_info.empty else 0.0

        final_amount = amount if tx_type == "Income" else -amount
        new_running = current_bal + final_amount
        status = "Completed"

        self._execute(
            """INSERT INTO ledger (transaction_id, date, account_id, description, category, amount, status, running_balance) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (txn_id, now_str, account_id, description, category, final_amount, status, new_running)
        )
        self._execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (new_running, account_id))
