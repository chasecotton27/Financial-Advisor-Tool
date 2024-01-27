class Bank:

  def __init__(self, bank_name):

    self.bank_name = bank_name


class Account(Bank):

  def __init__(self, bank_name, account_type):

    super().__init__(bank_name)
    self.account_type = account_type


class Transaction(Account):

  def __init__(self, bank_name, account_type, transaction_date, transaction_description, transaction_category, transaction_type, transaction_amount):

    super().__init__(bank_name, account_type)
    self.transaction_date = transaction_date
    self.transaction_description = transaction_description
    self.transaction_category = transaction_category
    self.transaction_type = transaction_type
    self.transaction_amount = float(transaction_amount)