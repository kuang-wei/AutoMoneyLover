import datetime

class MoneyLoverTransaction:
    def __init__(self, transaction_str, day_change=1):
        """
        transaction_str: str
            a specific string obtained from moneylover-cli
            example: '│ Thu Nov 26 2020 │ Kuang Wei │ Whole Foods          │ Expense │ Groceries    │ 68.88  │'
        """
        details = transaction_str.split("│ ")
        self.date = ' '.join(details[1].split())
        self.date = (
            datetime.datetime.strptime(self.date, "%a %b %d %Y") + datetime.timedelta(days=day_change)
        ).strftime("%Y-%m-%d")  # fix parsed transaction date dealy
        self.description = ' '.join(details[3].split())
        self.transaction_type = ' '.join(details[4].split())
        if self.transaction_type == "Expense":
            self.transaction_type = "debit"
        else:
            self.transaction_type = "credit"
        self.category = ' '.join(details[5].split())
        self.amount = float(details[6][:-1])