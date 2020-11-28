import os
import subprocess
from io import BytesIO as StringIO
import pandas as pd
import mintapi
import getpass
import keyring
from mintapi.api import assert_pd

from automoneylover.utils import map_category, parse_args


def get_transactions(mint):
    assert_pd()
    s = StringIO(mint.get_transactions_csv(
        include_investment=True))
    s.seek(0)
    df = pd.read_csv(s, parse_dates=['Date'])
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    df.category = (df.category.str.lower().replace('uncategorized', pd.NA))
    return df


def log_transaction(row, wallet):
    """
    row: pandas.core.series.Series
    """
    amount = row.amount
    category = map_category(row.category)
    date = row.date
    description = row.description
    raw_description = row.original_description
    transaction_type = row.transaction_type

    if "DIVVY" in raw_description:
        category = "Divvy"

    if "VANGUARD BUY INVESTMENT" in raw_description or "VANGUARD EDI" in raw_description:
       category = "Investment"

    if category == "Credit Card Payment":
        print("Not logging credit card payment to avoid double counting")
        return None
    elif description == "Target":
        category = "Groceries"
    elif category == "Income" and "Gusto" in description:  ## too personalized
        category = "Salary"
    elif category == "Transfer" and transaction_type == "credit" and "PAYPAL" in description:
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

    if transaction_type == "debit":
        subprocess.run(f"moneylover expense '{wallet}' {amount} -c '{category}' -d '{date}' -m '{description}'", shell=True)
        print()
    else:
        subprocess.run(f"moneylover income '{wallet}' {amount} -c '{category}' -d '{date}' -m '{description}'", shell=True)
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
        print(f"Filtering transactions before {args.start_date}")
        df = df[df["date"] >= args.start_date].copy()

    # Capitalize first character in category
    df["category"] = df["category"].str.title()

    # Log transactions in Money Lover
    print("Start logging transactions into Money Lover")
    for _, row in df.iterrows():
        log_transaction(row, args.wallet)


if __name__ == "__main__":
    main()
