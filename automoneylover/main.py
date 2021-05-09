import os
import subprocess
from io import BytesIO as StringIO
import pandas as pd
import mintapi
import getpass
import keyring
from mintapi.api import assert_pd

from automoneylover.utils import map_category, parse_args, check_duplicate, MAPPING, ANSI_ESCAPE
from automoneylover.transaction import MoneyLoverTransaction


def get_transactions(mint):
    assert_pd()
    s = StringIO(mint.get_transactions_csv(
        include_investment=True))
    s.seek(0)
    df = pd.read_csv(s, parse_dates=['Date'])
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    df.category = (df.category.str.lower().replace('uncategorized', pd.NA))
    return df


def get_moneylover_log(start_date, end_date, wallet="Kuang Wei"):
    output = subprocess.run(
        f"moneylover transactions '{wallet}' --startDate {start_date} --endDate {end_date}",
        shell=True,
        capture_output=True,
        text=True,
    )
    result = ANSI_ESCAPE.sub('', output.stdout)
    transaction_strs = result.split("\n")[2:-2]
    transactions = [MoneyLoverTransaction(transaction_str) for transaction_str in transaction_strs]
    return transactions


def log_transaction(row, wallet, transactions):
    """
    row: pandas.core.series.Series
    transactions: list(automoneylover.transaction.MoneyLoverTransaction)
        already logged transactions
    """
    amount = row.amount
    category = map_category(row.category)
    date = row.date
    description = row.description
    raw_description = row.original_description
    transaction_type = row.transaction_type

    if (
        "DIVVY" in raw_description or
        "Lyft" in description
    ):
        category = "Divvy"

    if (
        "VANGUARD BUY INVESTMENT" in raw_description or
        "VANGUARD EDI" in raw_description
    ) or (
        "VANGUARD BUY INVESTMENT" in description or
        "VANGUARD EDI" in description
    ):
       # category = "Investment"
       print(f"Detected Vanguard investment transaction. Skip as we do not log investment in MoneyLover.")
       return None

    if category == "Credit Card Payment":
        print("Not logging credit card payment to avoid double counting\n")
        return None
    elif description == "Target":
        category = "Groceries"
    elif description == "Wal-Mart":
        category = "Groceries"
    elif category == "Income" and "Gusto" in description:  ## too personalized
        category = "Salary"
    elif category == "Transfer" and transaction_type == "credit" and "PAYPAL" in description:
        category = "Resell"
    elif category == "Transfer" and transaction_type == "credit" and "Venmo Cashout" in description:
        category = "Resell"
    elif category == "Transfer" and transaction_type == "credit" and "EBAY EDI" in description:
        category = "Resell"
    elif category == "Transfer" and ("payment" in raw_description.lower() or "chase" in raw_description.lower()) and transaction_type == "credit":
        print("Not logging credit card payment to avoid double counting")
        return None
    elif category == "Transfer" and ("kith" in description.lower() or "ssense" in description.lower() or "soylent" in description.lower()):
        category = "Shopping"
    elif category == "Check" and amount == 925.0:
        category == "Housing"
    elif category == "Kids" and "DANCE" in description:
        category == "Dance"
    elif category == "Service Fee" and "annual membership fee" in description.lower():
        category == "Credit Card Fees"
    elif category == "Business Services" and "USPS" in description or "UPS" in description:
        category == "Shipping"

    duplicate = check_duplicate(date, category, amount, description, transactions)
    if not duplicate:
        if transaction_type == "debit":
            subprocess.run(f"moneylover expense '{wallet}' {amount} -c '{category}' -d '{date}' -m '{description}'", shell=True)

        else:
            subprocess.run(f"moneylover income '{wallet}' {amount} -c '{category}' -d '{date}' -m '{description}'", shell=True)

    else:
        print(f"Transaction {duplicate.date} | {duplicate.description:^20s} | {duplicate.amount:>4.2f} | has already been logged")
    print()

def main():
    args = parse_args()
    home = os.path.expanduser("~")
    default_session_path = os.path.join(home, '.mintapi', 'session')

    try:
        password = keyring.get_password('mintapi', args.username)
    except:
        print("keyring couldn't get saved password, please manually enter the password")
        password = getpass.getpass("Mint password: ")
        print("Saving the password to keyring")
        keyring.set_password('mintapi', args.username, password)


    # init Mint
    print("Logging into Mint")
    mint = mintapi.Mint(
        args.username,
        password,
        mfa_method='sms',
        headless=False,
        session_path=default_session_path,  # saved session to avoid multiple MFA requests
        wait_for_sync=True,
        wait_for_sync_timeout=300,  # number of seconds to wait for sync
        use_chromedriver_on_path=True,  # Use chromedriver on PATH since Debian Chromium is behind the latest release
    )

    # Get Transactions
    print("Obtaining transactions")
    df = get_transactions(mint)

    # Filter by date, if applicable
    if args.start_date:
        print(f"Filtering transactions that occured before {args.start_date}")
        df = df[df["date"] >= args.start_date].copy()
    if args.end_date:
        print(f"Fitering transactions that occured after   {args.end_date}")
        df = df[df["date"] <= args.end_date].copy()

    # Capitalize first character in category
    df["category"] = df["category"].str.title()

    # Check unmapped categories
    unmapped = []
    for category in pd.unique(df.category):
        if category not in MAPPING:
            unmapped.append(category)
            print(f"{category:>25s} is unmapped")
    print(f"Found a total of {len(unmapped)} unmapped categories")
    proceed = input("Proceed with logging? (y/n/print) ")  # TODO: make more user friendly

    if proceed == "print":
        for category in unmapped:
            sample_df = df.query(f"category == '{category}'")[
                ["date", "description", "original_description", "category", "transaction_type"]
            ]
            sample_df = sample_df.sample(n=min(5, len(sample_df)))
            print(f"Category: {category:<25}")
            print(sample_df.to_markdown())
            _ = input("Press ENTER for next category ")
            print("\n---\n")
        proceed = input("Proceed with logging? (y/n/CTRL-C) ")

    if proceed == "y":
        # Get logged transactions
        print("Obtaining already logged transactions to avoid repeating transactions")
        start_date = df.date.min()
        end_date = df.date.max()
        transactions = get_moneylover_log(start_date, end_date, wallet=args.wallet)
        # Log transactions in Money Lover
        print("Start logging transactions into Money Lover")
        for _, row in df.iterrows():
            log_transaction(row, args.wallet, transactions)
    else:
        print("Ending program")


if __name__ == "__main__":
    main()
