class Transaction:

  def __init__(self, account_type, transaction_date, transaction_description, transaction_amount, transaction_category, transaction_type):

    self.account_type = account_type
    self.transaction_date = transaction_date
    self.transaction_description = transaction_description
    self.transaction_amount = transaction_amount
    self.transaction_category = transaction_category
    self.transaction_type = transaction_type


class AccountRecord:

  def __init__(self, account_type, transactions, transaction_months, transaction_categories, transaction_types):

    self.account_type = account_type
    self.transactions = transactions
    self.transaction_months = transaction_months
    self.transaction_categories = transaction_categories
    self.transaction_types = transaction_types