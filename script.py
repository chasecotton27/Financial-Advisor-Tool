import functions


uploading_checking_files = True
checking_files_data = []

while True:
  first_upload = input('Would you like to upload a checking account CSV file? (yes or no): ').lower()
  if first_upload == 'yes':
    break
  elif first_upload == 'no':
    uploading_checking_files = False
    break
  else:
    print('Invalid input. Please enter yes or no.')

while uploading_checking_files:
  checking_file_data = functions.upload_file()
  account_type = 'checking account'
  checking_transactions_data = checking_file_data[0]
  checking_date_index = checking_file_data[1]
  checking_description_index = checking_file_data[2]
  checking_amount_index = checking_file_data[3]
  checking_category_index = checking_file_data[4]
  checking_type_index = checking_file_data[5]
  checking_files_data.append([account_type, checking_transactions_data, checking_date_index, checking_description_index, checking_amount_index, checking_category_index, checking_type_index])

  while True:
    still_uploading = input('Would you like to upload another checking account CSV file? (yes or no): ').lower()
    if still_uploading == 'yes':
      break
    elif still_uploading == 'no':
      uploading_checking_files = False
      break
    else:
      print('Invalid input. Please enter yes or no.')

uploading_credit_card_files = True
credit_card_files_data = []

while True:
  first_upload = input('Would you like to upload a credit card account CSV file? (yes or no): ').lower()
  if first_upload == 'yes':
    break
  elif first_upload == 'no':
    uploading_credit_card_files = False
    break
  else:
    print('Invalid input. Please enter yes or no.')

while uploading_credit_card_files:
  credit_card_file_data = functions.upload_file()
  account_type = 'credit card account'
  credit_card_transactions_data = credit_card_file_data[0]
  credit_card_date_index = credit_card_file_data[1]
  credit_card_description_index = credit_card_file_data[2]
  credit_card_amount_index = credit_card_file_data[3]
  credit_card_category_index = credit_card_file_data[4]
  credit_card_type_index = credit_card_file_data[5]
  credit_card_files_data.append([account_type, credit_card_transactions_data, credit_card_date_index, credit_card_description_index, credit_card_amount_index, credit_card_category_index, credit_card_type_index])

  while True:
    still_uploading = input('Would you like to upload another credit card account CSV file? (yes or no): ').lower()
    if still_uploading == 'yes':
      break
    elif still_uploading == 'no':
      uploading_credit_card_files = False
      break
    else:
      print('Invalid input. Please enter yes or no.')

files_data = checking_files_data + credit_card_files_data
files_transactions = []

for file_data in files_data:
  transactions = functions.create_transactions(file_data)
  files_transactions.append(transactions)

transactions = [transaction for file_transactions in files_transactions for transaction in file_transactions]

# Account records will be created after the transactions list is sorted and transaction attributes are formatted for each transaction

for file_transactions in files_transactions:
  pass

# For testing:

print()
print('First 5 Transactions:')
print()

for i in range(5):
  print(f'Account Type: {transactions[i].account_type}')
  print(f'Transaction Date: {transactions[i].transaction_date}')
  print(f'Transaction Description: {transactions[i].transaction_description}')
  print(f'Transaction Amount: {transactions[i].transaction_amount}')
  print(f'Transaction Category: {transactions[i].transaction_category}')
  print(f'Transaction Type: {transactions[i].transaction_type}')
  print()

print('Last 5 Transactions:')
print()

for i in range(-1, -6, -1):
  print(f'Account Type: {transactions[i].account_type}')
  print(f'Transaction Date: {transactions[i].transaction_date}')
  print(f'Transaction Description: {transactions[i].transaction_description}')
  print(f'Transaction Amount: {transactions[i].transaction_amount}')
  print(f'Transaction Category: {transactions[i].transaction_category}')
  print(f'Transaction Type: {transactions[i].transaction_type}')
  print()