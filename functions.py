import os
import csv
import re
from classes import Transaction
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


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


def remove_dates(transaction):

  dates = [
    r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', r'\b\d{1,2}-\d{1,2}-\d{2,4}\b', r'\b\d{1,2}.\d{1,2}.\d{2,4}\b', r'\b\d{1,2}\s\d{1,2}\s\d{2,4}\b',
    r'\b\d{1,2}/\d{1,2}\b', r'\b\d{1,2}-\d{1,2}\b', r'\b\d{1,2}.\d{1,2}\b', r'\b\d{1,2}\s\d{1,2}\b',
    r'\b\d{1,2}/\d{2,4}\b', r'\b\d{1,2}-\d{2,4}\b', r'\b\d{1,2}.\d{2,4}\b', r'\b\d{1,2}\s\d{2,4}\b',
    r'\b\d{2,4}/\d{1,2}\b', r'\b\d{2,4}-\d{1,2}\b', r'\b\d{2,4}.\d{1,2}\b', r'\b\d{2,4}\s\d{1,2}\b'
  ]

  combined_dates = '|'.join(dates)
  transaction.transaction_description = re.sub(combined_dates, ' ', transaction.transaction_description, count = 0)

  return transaction


def remove_phone_numbers(transaction):

  phone_numbers = [
    r'\b\d{3}-\d{3}-\d{4}\b', r'\b\d{3}.\d{3}.\d{4}\b', r'\b\d{3}\s\d{3}\s\d{4}\b',
    r'\b\(\d{3}\)-\d{3}-\d{4}\b', r'\b\(\d{3}\).\d{3}.\d{4}\b', r'\b\(\d{3}\)\s\d{3}\s\d{4}\b',
    r'\b\(\d{3}\)\s\d{3}-\d{4}\b', r'\b\(\d{3}\)\s\d{3}.\d{4}\b'
  ]

  combined_phone_numbers = '|'.join(phone_numbers)
  transaction.transaction_description = re.sub(combined_phone_numbers, ' ', transaction.transaction_description, count = 0)

  return transaction


def remove_url_components(transaction):

  transaction.transaction_description = re.sub(r'\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)(?:\.[a-zA-Z]{2,4})(?:/\S+)?\b', r'\1', transaction.transaction_description, count = 0)

  return transaction


def remove_id_numbers(transaction):

  id_numbers = [
    r'\b\d+\w+\b', r'\b\d+\w+\d+\b', r'\b\d+\w+\d+\w+\b', r'\b\d+\w+\d+\w+\d+\b', r'\b\d+\w+\d+\w+\d+\w+\b', r'\b\d+\w+\d+\w+\d+\w+\d+\b',
    r'\b\d+\w+\d+\w+\d+\w+\d+\w+\b', r'\b\d+\w+\d+\w+\d+\w+\d+\w+\d+\b', r'\b\d+\w+\d+\w+\d+\w+\d+\w+\d+\w+\b',
    r'\b\w+\d+\b', r'\b\w+\d+\w+\b', r'\b\w+\d+\w+\d+\b', r'\b\w+\d+\w+\d+\w+\b', r'\b\w+\d+\w+\d+\w+\d+\b', r'\b\w+\d+\w+\d+\w+\d+\w+\b',
    r'\b\w+\d+\w+\d+\w+\d+\w+\d+\b', r'\b\w+\d+\w+\d+\w+\d+\w+\d+\w+\b', r'\b\w+\d+\w+\d+\w+\d+\w+\d+\w+\d+\b'
  ]

  combined_id_numbers = '|'.join(id_numbers)
  transaction.transaction_description = re.sub(combined_id_numbers, ' ', transaction.transaction_description, count = 0)

  return transaction


def remove_symbols(transaction):

  symbols = [
    r'`', r'~', r'!', r'@', r'#', r'\$', r'%', r'\^', r'\*', r'\(', r'\)', r'_', r'=', r'\+', r'\[',
    r'\{', r'\]', r'\}', r'\\', r'\|', r';', r':', r'"', r'<', r',', r'\.', r'>', r'\?', r'/'
  ]

  combined_symbols = '|'.join(symbols)
  transaction.transaction_description = re.sub(combined_symbols, ' ', transaction.transaction_description, count = 0)

  return transaction


def remove_users_name(transaction, first_name, last_name):

  name = r'\b{}\s{}\b'.format(re.escape(first_name), re.escape(last_name))
  reversed_name = r'\b{}\s{}\b'.format(re.escape(last_name), re.escape(first_name))
  name_no_space = r'\b{}{}\b'.format(re.escape(first_name), re.escape(last_name))
  reversed_name_no_space = r'\b{}{}\b'.format(re.escape(last_name), re.escape(first_name))

  transaction.transaction_description = re.sub(name, ' ', transaction.transaction_description, count = 0)
  transaction.transaction_description = re.sub(reversed_name, ' ', transaction.transaction_description, count = 0)
  transaction.transaction_description = re.sub(name_no_space, ' ', transaction.transaction_description, count = 0)
  transaction.transaction_description = re.sub(reversed_name_no_space, ' ', transaction.transaction_description, count = 0)

  return transaction


def remove_standalone_numbers(transaction):

  transaction.transaction_description = re.sub(r'(?<![\w\d&\'-])\d+(?![\w\d&\'-])', ' ', transaction.transaction_description, count = 0)

  return transaction


def remove_standalone_valuable_symbols(transaction):

  transaction.transaction_description = re.sub(r'(?<![\w\d&\'-])&+(?![\w\d&\'-])', ' ', transaction.transaction_description, count = 0)
  transaction.transaction_description = re.sub(r'(?<![\w\d&\'-])\'+(?![\w\d&\'-])', ' ', transaction.transaction_description, count = 0)
  transaction.transaction_description = re.sub(r'(?<![\w\d&\'-])-+(?![\w\d&\'-])', ' ', transaction.transaction_description, count = 0)

  return transaction


def remove_extra_spaces(transaction):

  transaction.transaction_description = re.sub(r'\s+', ' ', transaction.transaction_description, count = 0)
  transaction.transaction_description = re.sub(r'^\s|\s$', '', transaction.transaction_description, count = 0)

  return transaction


def clean_transaction_descriptions(transactions, first_name, last_name):

  for transaction in transactions:
    transaction = remove_dates(transaction)
    transaction = remove_phone_numbers(transaction)
    transaction = remove_url_components(transaction)
    transaction = remove_id_numbers(transaction)
    transaction = remove_symbols(transaction)
    transaction = remove_users_name(transaction, first_name, last_name)
    transaction = remove_standalone_numbers(transaction)
    transaction = remove_standalone_valuable_symbols(transaction)
    transaction = remove_extra_spaces(transaction)

  return transactions


def format_training_data(first_name, last_name):

  transactions = []
  transaction_descriptions = []
  transaction_categories = []

  training_files_folder = 'training_files'
  folder_path = os.path.join(os.path.dirname(__file__), training_files_folder)

  if os.path.exists(folder_path) and os.path.isdir(folder_path):
    files = os.listdir(folder_path)

    for file in files:
      file_path = os.path.join(folder_path, file)

      with open(file_path, mode = 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        row_count = 1
        starting_row = 2

        for row in csv_reader:
          if row_count < starting_row:
            pass
          elif not row:
            pass
          else:
            transaction_description = row[0].lower()
            transaction_category = row[1].lower()
            transaction = Transaction('none', 'none', transaction_description, 'none', transaction_category, 'none')
            transactions.append(transaction)
          row_count += 1

  else:
    print('Error: The training_files folder does not exist.')

  transactions = clean_transaction_descriptions(transactions, first_name, last_name)

  for transaction in transactions:
    transaction_descriptions.append(transaction.transaction_description)
    transaction_categories.append(transaction.transaction_category)

  return transaction_descriptions, transaction_categories


def train_categories_model(transaction_descriptions, transaction_categories):

  description_train, description_test, category_train, category_test = train_test_split(transaction_descriptions, transaction_categories, test_size=0.2, random_state=42)

  tfidf_vectorizer = TfidfVectorizer()
  description_train_tfidf = tfidf_vectorizer.fit_transform(description_train)
  description_test_tfidf = tfidf_vectorizer.transform(description_test)

  classifier = MultinomialNB()
  classifier.fit(description_train_tfidf, category_train)

  y_pred = classifier.predict(description_test_tfidf)
  accuracy = accuracy_score(category_test, y_pred)

  return tfidf_vectorizer, classifier, accuracy


def predict_categories(transactions, tfidf_vectorizer, classifier):

  for transaction in transactions:
    if transaction.transaction_category == 'none':
      transaction_vector = tfidf_vectorizer.transform([transaction.transaction_description])
      predicted_category = classifier.predict(transaction_vector)
      transaction.transaction_category = predicted_category[0]
    else:
      pass

  return transactions