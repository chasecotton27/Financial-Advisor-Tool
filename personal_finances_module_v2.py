import os
import csv
from datetime import datetime


class Transaction:

  def __init__(self, bank_name, account_type, transaction_date, transaction_description, transaction_category, transaction_type, transaction_amount):

    self.bank_name = bank_name
    self.account_type = account_type
    self.transaction_date = transaction_date
    self.transaction_description = transaction_description
    self.transaction_category = transaction_category
    self.transaction_type = transaction_type
    self.transaction_amount = float(transaction_amount)


def upload_file():

  csv_files_folder = 'csv_files'
  valid_bank_names = ['wells fargo', 'chase bank']
  valid_account_types = ['checking account', 'credit card']

  while True:
    file_name = input(f'Please move your CSV file into the dedicated folder called {csv_files_folder}, then type the name of the file (including the .csv): ')
    file_path = os.path.join('.', csv_files_folder, file_name)
    if os.path.exists(file_path):
      break
    else:
      print('Invalid input. Please enter a valid file name.')
  while True:
    bank_name = input('Which financial institution is associated with this file? (wells fargo or chase bank): ').lower()
    if bank_name in valid_bank_names:
      break
    else:
      print('Invalid input. Please enter a valid financial institution.')
  while True:
    account_type = input('What kind of account is associated with this file? (checking account or credit card): ').lower()
    if account_type in valid_account_types:
      break
    else:
      print('Invalid input. Please enter a valid account.')

  while True:
    with open(file_path, mode = 'r') as csv_file:
      csv_reader = csv.reader(csv_file)

      while True:
        try:
          starting_row = int(input("In this CSV file, in which row does the transaction data begin? (Starting with 1 at the top, and do not include headers): "))
          break
        except:
          print("Invalid input. Please enter a valid integer.")
      while True:
        try:
          date_column = int(input("In this CSV file, which column contains the date of the transaction? (Starting with 1 on the left): "))
          break
        except:
          print("Invalid input. Please enter a valid integer.")
      while True:
        try:
          description_column = int(input("In this CSV file, which column contains the description of the transaction? (Starting with 1 on the left): "))
          break
        except:
          print("Invalid input. Please enter a valid integer.")
      while True:
        try:
          category_column = int(input("In this CSV file, which column contains the category of the transaction? (Starting with 1 on the left, and if there is no category, then type 0): "))
          break
        except:
          print("Invalid input. Please enter a valid integer.")
      while True:
        try:
          type_column = int(input("In this CSV file, which column contains the type of the transaction? (Starting with 1 on the left, and if there is no type, then type 0): "))
          break
        except:
          print("Invalid input. Please enter a valid integer.")
      while True:
        try:
          amount_column = int(input("In this CSV file, which column contains the amount of the transaction? (Starting with 1 on the left): "))
          break
        except:
          print("Invalid input. Please enter a valid integer.")

      transactions = []
      row_number = 1

      for row in csv_reader:
        if row[date_column - 1]:
          transaction_date = row[date_column - 1]
        else:
          transaction_date = 'none'
        if row[description_column - 1]:
          transaction_description = row[description_column - 1].lower()
        else:
          transaction_description = 'none'
        if row[category_column - 1]:
          transaction_category = row[category_column - 1].lower()
        else:
          transaction_category = 'none'
        if row[type_column - 1]:
          transaction_type = row[type_column - 1].lower()
        else:
          transaction_type = 'none'
        if row[amount_column - 1]:
          transaction_amount = row[amount_column - 1]
        else:
          transaction_amount = 'none'

        if row_number < starting_row or not row:
          pass
        elif len(row) < max(date_column, description_column, category_column, type_column, amount_column):
          print("Error: Some specified column numbers are out of bounds for a row. Please check your input.")
          break
        elif category_column == 0 and type_column != 0:
          transaction = Transaction(bank_name, account_type, transaction_date, transaction_description, 'none', transaction_type, transaction_amount)
          transactions.append(transaction)
        elif category_column != 0 and type_column == 0:
          transaction = Transaction(bank_name, account_type, transaction_date, transaction_description, transaction_category, 'none', transaction_amount)
          transactions.append(transaction)
        elif category_column == 0 and type_column == 0:
          transaction = Transaction(bank_name, account_type, transaction_date, transaction_description, 'none', 'none', transaction_amount)
          transactions.append(transaction)
        else:
          transaction = Transaction(bank_name, account_type, transaction_date, transaction_description, transaction_category, transaction_type, transaction_amount)
          transactions.append(transaction)

        row_number += 1

    if transactions:
      break

  return transactions


def incoming_or_outgoing(transactions):

  incoming_transactions = []
  outgoing_transactions = []
  null_transactions = []

  for transaction in transactions:
    if transaction.transaction_amount > 0:
      incoming_transactions.append(transaction)
    elif transaction.transaction_amount < 0:
      outgoing_transactions.append(transaction)
    else:
      null_transactions.append(transaction)

  return incoming_transactions, outgoing_transactions, null_transactions


def identify_credit_payments(transactions):

  credit_payments = []

  for transaction in transactions:
    if transaction.transaction_type == 'payment':
      credit_payments.append(transaction)

  return credit_payments


def identify_credit_returns(transactions):

  credit_returns = []

  for transaction in transactions:
    if transaction.transaction_type == 'return':
      credit_returns.append(transaction)

  return credit_returns


# Need to find a way to identify descriptions, categories, and types that applies to any bank_name and account_type
# Also need to find a way to add unrecognized transactions to identify_credit_payments() and identify_credit_returns()
# Need to offset credit card payments and other transactions before separate_and_sort_by_month()


"""def separate_and_sort_by_month(transactions_by_account_and_type):

  monthly_transactions_dictionary = {}

  for accounts_and_types in transactions_by_account_and_type:
    for transaction in accounts_and_types:
      month = datetime.strptime(transaction.transaction_date, '%m/%d/%Y').month
      year = datetime.strptime(transaction.transaction_date, '%m/%d/%Y').year
      month_year = str(month) + '/' + str(year)

      if month_year not in monthly_transactions_dictionary:
        monthly_transactions_dictionary[month_year] = []

      monthly_transactions_dictionary[month_year].append(transaction)

  monthly_sorted_transactions = {}

  for month_year, transactions in monthly_transactions_dictionary.items():
    sorted_transactions = sorted(transactions, key=lambda transaction: datetime.strptime(transaction.transaction_date, '%m/%d/%Y'))
    monthly_sorted_transactions[month_year] = sorted_transactions

  return monthly_sorted_transactions"""


"""def categorize_purchases(purchases):

  automotive = []
  entertainment = []
  gas_stations = []
  groceries = []
  health = []
  miscellaneous = []
  personal = []
  rent_and_utilities = []
  restaurants = []
  shopping = []
  travel = []

  for row in purchases:
    if row[2] == 'Automotive' or 'TOYOTA ACH' in row[1]:
      automotive.append(row)
    elif row[2] == 'Entertainment' or 'PlayStation' in row[1] or 'PlaystationNetwork' in row[1] or 'SPOTIFY' in row[1] or 'APPLE.COM/BILL' in row[1]:
      entertainment.append(row)
    elif row[2] == 'Gas':
      gas_stations.append(row)
    elif row[2] == 'Groceries':
      groceries.append(row)
    elif row[2] == 'Health & Wellness' or 'GOLDS GYM' in row[1]:
      health.append(row)
    elif row[2] == 'Miscellaneous' or row[2] == 'Fees & Adjustments':
      miscellaneous.append(row)
    elif row[2] == 'Personal' or row[2] == 'Education' or row[2] == 'Gifts & Donations' or row[2] == 'Home' or row[2] == 'Professional Services' or 'ATM' in row[1] or 'VENMO' in row[1] or 'PAYPAL' in row[1] or 'NORTHWEST HILLS' in row[1]:
      personal.append(row)
    elif row[2] == 'Bills & Utilities' or 'ZELLE' in row[1] or 'ClickPay' in row[1] or 'City of Austin' in row[1] or 'ONE GAS TEXAS' in row[1] or 'AT''&''T' in row[1]:
      rent_and_utilities.append(row)
    elif row[2] == 'Food & Drink':
      restaurants.append(row)
    elif row[2] == 'Shopping' or 'PURCHASE AUTHORIZED' in row[1]:
      shopping.append(row)
    elif row[2] == 'Travel':
      travel.append(row)
    else:
      raise Exception('Unrecognized purchase category.')

  categorized_purchases = [automotive, entertainment, gas_stations, groceries, health, miscellaneous, personal, rent_and_utilities, restaurants, shopping, travel]

  return categorized_purchases


def categorize_income(income):

  salary_income = []
  wants_reimbursement = []
  needs_reimbursement = []

  for row in income:
    if 'APPLE CASH' in row[1] or 'PURCHASE RETURN' in row[1] or 'MOBILE DEPOSIT' in row[1]:
      wants_reimbursement.append(row)
    elif 'VENMO CASHOUT' in row[1] or 'ONLINE TRANSFER' in row[1] or 'ZELLE' in row[1]:
      needs_reimbursement.append(row)
    elif 'NATIONAL INSTRUM' in row[1] or 'TAX REF' in row[1]:
      salary_income.append(row)
    else:
      raise Exception('Unrecognized income category.')

  return salary_income, wants_reimbursement, needs_reimbursement


def categorize_savings(savings):

  contributions = []
  employer_contributions = []
  withdrawals = []
  fees = []
  reorganizations = []

  for row in savings:
    if 'Fee' in row[1] or 'FEE' in row[1]:
      fees.append(row)
    elif 'ACH WITHDRAWL' in row[1]:
      withdrawals.append(row)
    elif 'Employer' in row[1]:
      employer_contributions.append(row)
    elif row[2] == 'Reorganization':
      reorganizations.append(row)
    elif 'DEPOSIT' in row[1] or 'Employee' in row[1]:
      contributions.append(row)
    else:
      raise Exception('Unrecognized savings category.')

  return contributions, employer_contributions, withdrawals, fees, reorganizations"""