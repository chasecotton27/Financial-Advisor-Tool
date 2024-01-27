import os
import csv
from datetime import datetime
from classes import Bank
from classes import Account
from classes import Transaction


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
    bank = Bank(input('Which financial institution is associated with this file? (wells fargo or chase bank): ').lower())
    if bank.bank_name in valid_bank_names:
      break
    else:
      print('Invalid input. Please enter a valid financial institution.')
  while True:
    account = Account(bank.bank_name, input('What kind of account is associated with this file? (checking account or credit card): ').lower())
    if account.account_type in valid_account_types:
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
          transaction = Transaction(account.bank_name, account.account_type, transaction_date, transaction_description, 'none', transaction_type, transaction_amount)
          transactions.append(transaction)
        elif category_column != 0 and type_column == 0:
          transaction = Transaction(account.bank_name, account.account_type, transaction_date, transaction_description, transaction_category, 'none', transaction_amount)
          transactions.append(transaction)
        elif category_column == 0 and type_column == 0:
          transaction = Transaction(account.bank_name, account.account_type, transaction_date, transaction_description, 'none', 'none', transaction_amount)
          transactions.append(transaction)
        else:
          transaction = Transaction(account.bank_name, account.account_type, transaction_date, transaction_description, transaction_category, transaction_type, transaction_amount)
          transactions.append(transaction)

        row_number += 1

    if transactions:
      break

  return bank, account, transactions


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