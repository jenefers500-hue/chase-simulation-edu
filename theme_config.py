CHASE_BLUE = "#0060a3"
CHASE_DARK = "#112e51"
BG_LIGHT   = "#f4f6f9"

DEFAULT_ACCOUNTS = [
    {"id": "CHASE-CHKP-4321", "name": "Chase Total Checking (...4321)", "balance": 38563.60, "type": "Checking"},
    {"id": "CHASE-SAV-8765", "name": "Chase Premier Savings (...8765)", "balance": 24910.45, "type": "Savings"},
    {"id": "CHASE-CC-0912", "name": "Chase Sapphire Card (...0912)", "balance": -412.30, "type": "Credit Card"}
]

DEFAULT_HISTORY = [
    {
        "transaction_id": "TXN-2026-0616-001",
        "date": "2026-06-16T08:30:00Z",
        "description": "ATM Withdrawal - Shared Account",
        "category": "Cash",
        "amount": -8500.00,
        "status": "Completed",
        "running_balance": 52563.60
    },
    {
        "transaction_id": "TXN-2026-0616-002",
        "date": "2026-06-16T10:15:00Z",
        "description": "Online Transfer Out to Savings",
        "category": "Transfer",
        "amount": -10000.00,
        "status": "Completed",
        "running_balance": 42563.60
    },
    {
        "transaction_id": "TXN-2026-0616-003",
        "date": "2026-06-16T12:00:00Z",
        "description": "ATM Withdrawal - Owner Verified",
        "category": "Cash",
        "amount": -4000.00,
        "status": "Completed",
        "running_balance": 38563.60
    },
    {
        "transaction_id": "TXN-2026-0616-004",
        "date": "2026-06-16T14:45:00Z",
        "description": "Unauthorized External Transfer",
        "category": "Uncategorized",
        "amount": -5000.00,
        "status": "Failed - Flagged Fraudulent / Account Frozen",
        "running_balance": 38563.60
    }
]
