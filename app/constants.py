# app/constants.py

ACCOUNT_TYPE_LABELS = {
    "checking": "Checking",
    "savings": "Savings",
    "cd": "Certificate of Deposit",
    "brokerage": "Brokerage",
    "ira": "IRA",
}

TAX_TREATMENT_LABELS = {
    "taxable": "Taxable",
    "traditional_ira": "Traditional IRA",
    "roth_ira": "Roth IRA",
}

ENTRY_TYPE_LABELS = {
    "opening": "Opening Balance",
    "deposit": "Deposit",
    "withdrawal": "Withdrawal",
    "transfer_in": "Transfer In",
    "transfer_out": "Transfer Out",
    "interest": "Interest",
    "fee": "Fee",
}


# For now: cash-style register entry types
CASH_ENTRY_TYPES = [
    "opening", "deposit", "withdrawal", "transfer_in", "transfer_out", "interest", "fee"
]