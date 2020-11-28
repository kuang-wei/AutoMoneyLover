import argparse


MAPPING = {
    "Television": "Utilities",
    "Fast Food": "Quick Food",
    "Pharmacy": "Medical",
    "Gift": "Shopping",
    "Rental Car & Taxi": "Uber",
    "Clothing": "Shopping",
    "Mobile Phone": "Utilities",
    "Doctor": "Medical",
    "Food & Dining": "Food & Beverage",
    "Mortgage & Rent": "Housing",
}


def map_category(category):
    if category in MAPPING:
        return MAPPING[category]
    else:
        return category


def parse_args():
    parser = argparse.ArgumentParser(description='Handles necessary arguments to run AutoMoneyLover')
    parser.add_argument('username', type=str, help='Username for Mint log-in')
    parser.add_argument("wallet", type=str, help='The name of the wallet to which to log transactions')
    parser.add_argument('--start_date', default=None, type=str, help='Date filter to add all transactions since this date')
    args = parser.parse_args()

    return args