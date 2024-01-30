import os
import csv
from classes import Transaction
from datetime import datetime


def upload_file(account_type):

  csv_files_folder = 'csv_files'

  while True:
    file_name = input(f'Please move your CSV file into the folder called {csv_files_folder}, then type the name of the file. (include the .csv)\n')
    file_path = os.path.join('.', csv_files_folder, file_name)
    if os.path.exists(file_path):
      break
    else:
      print('Invalid input. Please enter a valid file name.')

  while True:
    with open(file_path, mode = 'r') as csv_file:
      csv_reader = csv.reader(csv_file)

      while True:
        try:
          starting_row = int(input('In this CSV file, in which row does the transaction data begin? (start with 1 at the top)\n'))
          break
        except:
          print('Invalid input. Please enter a valid integer.')

      while True:
        try:
          date_column = int(input('In this CSV file, which column contains the date of the transaction? (start with 1 on the left)\n'))
          break
        except:
          print('Invalid input. Please enter a valid integer.')

      while True:
        try:
          description_column = int(input('In this CSV file, which column contains the description of the transaction? (start with 1 on the left)\n'))
          break
        except:
          print('Invalid input. Please enter a valid integer.')

      amount_column = ''
      incoming_amount_column = ''
      outgoing_amount_column = ''

      while True:
        amount_format = input('In this CSV file, is the amount of the transaction represented in a single column with positive and negative values for the direction of the transaction, or is the amount of the transaction represented in separate columns for incoming and outgoing transactions? (single or separate)\n').lower()
        if amount_format == 'single':
          while True:
            try:
              amount_column = int(input('In this CSV file, which column contains the amount of the transaction? (Start with 1 on the left)\n'))
              break
            except:
              print('Invalid input. Please enter a valid integer.')
          while True:
            incoming_amount_sign = input('Is the amount of the transaction positive or negative for incoming transactions? (for checking transactions, this includes income, refunds, etc, and for credit card transactions, this includes rewards, payments towards credit card debt, etc)\n').lower()
            if incoming_amount_sign == 'positive':
              break
            elif incoming_amount_sign == 'negative':
              break
            else:
              print('Invalid input. Please enter positive or negative.')
          while True:
            outgoing_amount_sign = input('Is the amount of the transaction positive or negative for outgoing transactions? (for checking transactions, this includes purchases, payments towards credit card debt, etc, and for credit card transactions, this includes credit purchases, fees, etc)\n').lower()
            if outgoing_amount_sign == 'positive':
              break
            elif outgoing_amount_sign == 'negative':
              break
            else:
              print('Invalid input. Please enter positive or negative.')
          break
        elif amount_format == 'separate':
          while True:
            try:
              incoming_amount_column = int(input('In this CSV file, which column contains the amount of the incoming transaction? (start with 1 on the left... for checking transactions, this includes income, refunds, etc, and for credit card transactions, this includes rewards, payments towards credit card debt, etc)\n'))
              break
            except:
              print('Invalid input. Please enter a valid integer.')
          while True:
            try:
              outgoing_amount_column = int(input('In this CSV file, which column contains the amount of the outgoing transaction? (start with 1 on the left... for checking transactions, this includes purchases, payments towards credit card debt, etc, and for credit card transactions, this includes credit purchases, fees, etc)\n'))
              break
            except:
              print('Invalid input. Please enter a valid integer.')
          break
        else:
          print('Invalid input. Please enter single or separate.')

      while True:
        try:
          category_column = int(input('In this CSV file, which column contains the category of the transaction? (start with 1 on the left... if there is no category, then type 0)\n'))
          break
        except:
          print('Invalid input. Please enter a valid integer.')

      while True:
        try:
          type_column = int(input('In this CSV file, which column contains the type of the transaction? (start with 1 on the left... if there is no type, then type 0)\n'))
          break
        except:
          print('Invalid input. Please enter a valid integer.')

      transactions_data = []
      row_number = 1

      if amount_column:
        if (incoming_amount_sign == 'positive' and outgoing_amount_sign == 'negative') or (incoming_amount_sign == 'negative' and outgoing_amount_sign == 'positive'):
          for row in csv_reader:
            if row_number < starting_row or not row:
              pass
            elif len(row) < max(date_column, description_column, amount_column, category_column, type_column):
              print('Error: Some specified column numbers are out of bounds for a row. Please check your input.')
              transactions_data = []
              break
            else:
              transactions_data.append(row)
            row_number += 1
        else:
          print('Error: Incoming and outgoing transactions cannout both be positive or negative. Please check your input.')
          transactions_data = []
          break

      elif incoming_amount_column and outgoing_amount_column:
        for row in csv_reader:
          if row_number < starting_row or not row:
            pass
          elif len(row) < max(date_column, description_column, incoming_amount_column, outgoing_amount_column, category_column, type_column):
            print('Error: Some specified column numbers are out of bounds for a row. Please check your input.')
            transactions_data = []
            break
          else:
            transactions_data.append(row)
          row_number += 1

    if amount_column:
      date_index = date_column - 1
      description_index = description_column - 1
      amount_index = amount_column - 1
      category_index = category_column - 1
      type_index = type_column - 1

    elif incoming_amount_column and outgoing_amount_column:
      date_index = date_column - 1
      description_index = description_column - 1
      incoming_amount_index = incoming_amount_column - 1
      outgoing_amount_index = outgoing_amount_column - 1
      category_index = category_column - 1
      type_index = type_column - 1

    if transactions_data:
      break

  if amount_column:
    return account_type, transactions_data, date_index, description_index, amount_index, incoming_amount_sign, outgoing_amount_sign, category_index, type_index
  elif incoming_amount_column and outgoing_amount_column:
    return account_type, transactions_data, date_index, description_index, incoming_amount_index, outgoing_amount_index, category_index, type_index


def create_transactions(account_data):

  if len(account_data) == 9:
    account_type = account_data[0]
    transactions_data = account_data[1]
    date_index = account_data[2]
    description_index = account_data[3]
    amount_index = account_data[4]
    incoming_amount_sign = account_data[5]
    outgoing_amount_sign = account_data[6]
    category_index = account_data[7]
    type_index = account_data[8]

    transactions = []

    for transaction_data in transactions_data:
      if transaction_data[date_index]:
        transaction_date = transaction_data[date_index]
      else:
        transaction_date = 'none'

      if transaction_data[description_index]:
        transaction_description = transaction_data[description_index].lower()
      else:
        transaction_description = 'none'

      if float(transaction_data[amount_index]):
        if incoming_amount_sign == 'positive' and outgoing_amount_sign == 'negative':
          transaction_amount = transaction_data[amount_index]
        elif incoming_amount_sign == 'negative' and outgoing_amount_sign == 'positive':
          if '-' in transaction_data[amount_index]:
            updated_transaction_data = [character for character in transaction_data[amount_index] if character != '-']
            transaction_amount = ''.join(updated_transaction_data)
          elif '-' not in transaction_data[amount_index]:
            transaction_amount = '-' + transaction_data[amount_index]
      else:
        transaction_amount = 'none'

      if transaction_data[category_index]:
        transaction_category = transaction_data[category_index].lower()
      else:
        transaction_category = 'none'

      if transaction_data[type_index]:
        transaction_type = transaction_data[type_index].lower()
      else:
        transaction_type = 'none'

      if category_index < 0 and type_index >= 0:
        transaction = Transaction(account_type, transaction_date, transaction_description, transaction_amount, 'none', transaction_type)
        transactions.append(transaction)
      elif category_index >= 0 and type_index < 0:
        transaction = Transaction(account_type, transaction_date, transaction_description, transaction_amount, transaction_category, 'none')
        transactions.append(transaction)
      elif category_index < 0 and type_index < 0:
        transaction = Transaction(account_type, transaction_date, transaction_description, transaction_amount, 'none', 'none')
        transactions.append(transaction)
      else:
        transaction = Transaction(account_type, transaction_date, transaction_description, transaction_amount, transaction_category, transaction_type)
        transactions.append(transaction)

  elif len(account_data) == 8:
    account_type = account_data[0]
    transactions_data = account_data[1]
    date_index = account_data[2]
    description_index = account_data[3]
    incoming_amount_index = account_data[4]
    outgoing_amount_index = account_data[5]
    category_index = account_data[6]
    type_index = account_data[7]

    transactions = []

    for transaction_data in transactions_data:
      if transaction_data[date_index]:
        transaction_date = transaction_data[date_index]
      else:
        transaction_date = 'none'

      if transaction_data[description_index]:
        transaction_description = transaction_data[description_index].lower()
      else:
        transaction_description = 'none'

      if float(transaction_data[incoming_amount_index]):
        if '-' in transaction_data[incoming_amount_index]:
          updated_transaction_data = [character for character in transaction_data[incoming_amount_index] if character != '-']
          transaction_amount = ''.join(updated_transaction_data)
        elif '-' not in transaction_data[incoming_amount_index]:
          transaction_amount = transaction_data[incoming_amount_index]
      elif float(transaction_data[outgoing_amount_index]):
        if '-' in transaction_data[outgoing_amount_index]:
          transaction_amount = transaction_data[outgoing_amount_index]
        elif '-' not in transaction_data[outgoing_amount_index]:
          transaction_amount = '-' + transaction_data[outgoing_amount_index]
      else:
        transaction_amount = 'none'

      if transaction_data[category_index]:
        transaction_category = transaction_data[category_index].lower()
      else:
        transaction_category = 'none'

      if transaction_data[type_index]:
        transaction_type = transaction_data[type_index].lower()
      else:
        transaction_type = 'none'

      if category_index < 0 and type_index >= 0:
        transaction = Transaction(account_type, transaction_date, transaction_description, transaction_amount, 'none', transaction_type)
        transactions.append(transaction)
      elif category_index >= 0 and type_index < 0:
        transaction = Transaction(account_type, transaction_date, transaction_description, transaction_amount, transaction_category, 'none')
        transactions.append(transaction)
      elif category_index < 0 and type_index < 0:
        transaction = Transaction(account_type, transaction_date, transaction_description, transaction_amount, 'none', 'none')
        transactions.append(transaction)
      else:
        transaction = Transaction(account_type, transaction_date, transaction_description, transaction_amount, transaction_category, transaction_type)
        transactions.append(transaction)

  return transactions


def format_transaction_dates(transactions):

  for transaction in transactions:
    month = datetime.strptime(transaction.transaction_date, '%m/%d/%Y').month
    day = datetime.strptime(transaction.transaction_date, '%m/%d/%Y').day
    year = datetime.strptime(transaction.transaction_date, '%m/%d/%Y').year
    date = str(month) + '/' + str(day) + '/' + str(year)
    transaction.transaction_date = date

  return transactions


def sort_transactions(transactions):

  transactions = sorted(transactions, key = lambda transaction: datetime.strptime(transaction.transaction_date, '%m/%d/%Y'))

  return transactions


# From version 1:

'''def categorize_purchases(purchases):

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

  return contributions, employer_contributions, withdrawals, fees, reorganizations'''