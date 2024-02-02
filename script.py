import functions


first_name = input('What is your first name?\n').lower()
last_name = input('What is your last name?\n').lower()

uploading_checking_files = True
checking_accounts_transactions = []

while True:
  first_upload = input('Would you like to upload a checking account CSV file? (yes or no)\n').lower()
  if first_upload == 'yes':
    break
  elif first_upload == 'no':
    uploading_checking_files = False
    break
  else:
    print('Invalid input. Please enter yes or no.')

while uploading_checking_files:
  checking_account_data = functions.upload_file('checking account')
  checking_account_transactions = functions.create_transactions(checking_account_data)
  checking_accounts_transactions.append(checking_account_transactions)

  while True:
    still_uploading = input('Would you like to upload another checking account CSV file? (yes or no)\n').lower()
    if still_uploading == 'yes':
      break
    elif still_uploading == 'no':
      uploading_checking_files = False
      break
    else:
      print('Invalid input. Please enter yes or no.')

checking_transactions = [checking_account_transaction for checking_account_transactions in checking_accounts_transactions for checking_account_transaction in checking_account_transactions]

uploading_credit_card_files = True
credit_card_accounts_transactions = []

while True:
  first_upload = input('Would you like to upload a credit card account CSV file? (yes or no)\n').lower()
  if first_upload == 'yes':
    break
  elif first_upload == 'no':
    uploading_credit_card_files = False
    break
  else:
    print('Invalid input. Please enter yes or no.')

while uploading_credit_card_files:
  credit_card_account_data = functions.upload_file('credit card account')
  credit_card_account_transactions = functions.create_transactions(credit_card_account_data)
  credit_card_accounts_transactions.append(credit_card_account_transactions)

  while True:
    still_uploading = input('Would you like to upload another credit card account CSV file? (yes or no)\n').lower()
    if still_uploading == 'yes':
      break
    elif still_uploading == 'no':
      uploading_credit_card_files = False
      break
    else:
      print('Invalid input. Please enter yes or no.')

credit_card_transactions = [credit_card_account_transaction for credit_card_account_transactions in credit_card_accounts_transactions for credit_card_account_transaction in credit_card_account_transactions]

for checking_account_transactions in checking_accounts_transactions:
  checking_account_transactions = functions.format_transaction_dates(checking_account_transactions)
  checking_account_transactions = functions.sort_transactions(checking_account_transactions)

for credit_card_account_transactions in credit_card_accounts_transactions:
  credit_card_account_transactions = functions.format_transaction_dates(credit_card_account_transactions)
  credit_card_account_transactions = functions.sort_transactions(credit_card_account_transactions)

transactions = checking_transactions + credit_card_transactions
transactions = functions.format_transaction_dates(transactions)
transactions = functions.sort_transactions(transactions)
transactions = functions.clean_transaction_descriptions(transactions, first_name, last_name)


# For machine learning:

training_data = functions.format_training_data()
transaction_descriptions = training_data[0]
transaction_categories = training_data[1]

categories_model = functions.train_categories_model(transaction_descriptions, transaction_categories)
tfidf_vectorizer = categories_model[0]
classifier = categories_model[1]
model_accuracy = categories_model[2]

transactions = functions.predict_categories(transactions, tfidf_vectorizer, classifier)


# For testing:

for transaction in transactions:
  print()
  print(f'Description: {transaction.transaction_description}')
  print(f'Category: {transaction.transaction_category}')

print()
print(f'Model Accuracy: {(model_accuracy*100): .2f}%')
print()


# From Chase and Discover formats:

'''Category Options:

services
merchandise
travel
gifts & donations
education
home improvement
food & drink
gasoline
fees & adjustments
groceries
travel/ entertainment
automotive
gas
professional services
department stores
payments and credits
personal
none
supermarkets
shopping
restaurants
health & wellness
awards and rebate credits
entertainment

Type Options:

none
sale
payment
return
fee'''


# The goal is to adjust the transaction attributes for each transaction so that they follow a uniform structure
# These attributes should be the main determinator of the classification/operation of a transaction
# Then, account/transaction records can be created to analyze the transactions as a whole
# Keep the functions very modular, where each function completes a very specific task
# AccountRecord might need to be changed to TransactionRecord, depending on the requirements that become visible later
# Assigning and updating transaction attributes might involve some machine learning, that way there's no dependency on keywords specific to my account
# These attributes can be updated one step at a time, since a complete transactions list already exists