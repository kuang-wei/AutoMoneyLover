import argparse


MAPPING = {
    "Television": "Utilities",
    "Fast Food": "Quick Food",
    "Pharmacy": "Medical",
    "Gift": "Shopping",
    "Rental Car & Taxi": "Uber",
    "Clothing": "Shopping",
    "Mobile Phone": "Phone Bill",
    "Doctor": "Medical",
    "Dentist": "Medical",
    "Food & Dining": "Food & Beverage",
    "Mortgage & Rent": "Housing",
    "Gas & Fuel": "Travel",  # Don't really buy gas under normal circustances
    "Rental Car & Taxi": "Travel",
    "Parking": "Transportation",
    "Hotel": "Travel",
    "Sporting Goods": "Shopping",
    "Movies & Dvds": "Entertainment",
    "Music": "Entertainment",
    "Books": "Education",
    "Bills & Utilities": "Utilities",
    "Auto & Transport": "Utilities",
    "Home": "Shopping",
    "Vacation": "Travel",
    "Laundry": "Utilities",
    "Federal Tax": "Taxes",
    "Personal Care": "Other",
    "Shopping": "Shopping",  # Start of default categories
    "Groceries": "Groceries",
    "Coffee Shops": "Coffee Shops",
    "Utilities": "Utilities",
    "Credit Card Payment": "Credit Card Payment",
    "Entertainment": "Entertainment",
    "Taxes": "Taxes",
    "Health & Fitness": "Health & Fitness",
    "Travel": "Travel",
    "Restaurants": "Restaurants",
    "Shipping": "Shipping",
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
    parser.add_argument('--end_date', default=None, type=str, help='Date filter to add all transactions up to this date')
    args = parser.parse_args()

    return args