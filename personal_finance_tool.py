import functions


banks = []
accounts = []
transactions_by_account = []
uploading_files = True

while uploading_files:
  file_data = functions.upload_file()
  banks.append(file_data[0])
  accounts.append(file_data[1])
  transactions_by_account.append(file_data[2])

  while True:
    still_uploading = input('Would you like to upload another CSV file? (yes or no): ').lower()

    if still_uploading == 'yes':
      break
    elif still_uploading == 'no':
      uploading_files = False
      break
    else:
      print('Invalid input. Please enter yes or no.')

transactions_by_account_and_type = []
unrecognized_transactions_by_account = []

for account in transactions_by_account:
  incoming_transactions = functions.incoming_or_outgoing(account)[0]
  outgoing_transactions = functions.incoming_or_outgoing(account)[1]
  null_transactions = functions.incoming_or_outgoing(account)[2]
  transactions_by_account_and_type.append([incoming_transactions, outgoing_transactions])
  unrecognized_transactions_by_account.append(null_transactions)

credit_payments_by_account = []
credit_returns_by_account = []

for account in transactions_by_account_and_type:
  for type in account:
    if type[0].account_type == 'credit card' and type[0].transaction_amount > 0:
      credit_payments = functions.identify_credit_payments(type)
      credit_returns = functions.identify_credit_returns(type)
      credit_payments_by_account.append(credit_payments)
      credit_returns_by_account.append(credit_returns)

credit_payments = [credit_payment for credit_payments in credit_payments_by_account for credit_payment in credit_payments]
credit_returns = [credit_return for credit_returns in credit_returns_by_account for credit_return in credit_returns]

print()
print('transactions_by_account_and_type:')
print()
print('type:')
print(type(transactions_by_account_and_type))
print(type(transactions_by_account_and_type[0]))
print(type(transactions_by_account_and_type[0][0]))
print(type(transactions_by_account_and_type[0][0][0]))
print()
print('example:')
print(transactions_by_account_and_type[0][0][0].bank_name)
print(transactions_by_account_and_type[0][0][0].account_type)
print(transactions_by_account_and_type[0][0][0].transaction_date)
print(transactions_by_account_and_type[0][0][0].transaction_description)
print(transactions_by_account_and_type[0][0][0].transaction_category)
print(transactions_by_account_and_type[0][0][0].transaction_type)
print(transactions_by_account_and_type[0][0][0].transaction_amount)
print()
print('unrecognized_transactions_by_account')
print()
print('type:')
print(type(unrecognized_transactions_by_account))
print(type(unrecognized_transactions_by_account[0]))
print(type(unrecognized_transactions_by_account[0][0]))
print()
print('example:')
print(unrecognized_transactions_by_account[0][0].bank_name)
print(unrecognized_transactions_by_account[0][0].account_type)
print(unrecognized_transactions_by_account[0][0].transaction_date)
print(unrecognized_transactions_by_account[0][0].transaction_description)
print(unrecognized_transactions_by_account[0][0].transaction_category)
print(unrecognized_transactions_by_account[0][0].transaction_type)
print(unrecognized_transactions_by_account[0][0].transaction_amount)
print()
print('credit_payments')
print()
print('type:')
print(type(credit_payments))
print(type(credit_payments[0]))
print()
print('example:')
print(credit_payments[0].bank_name)
print(credit_payments[0].account_type)
print(credit_payments[0].transaction_date)
print(credit_payments[0].transaction_description)
print(credit_payments[0].transaction_category)
print(credit_payments[0].transaction_type)
print(credit_payments[0].transaction_amount)
print()
print('credit_returns')
print()
print('type:')
print(type(credit_returns))
print(type(credit_returns[0]))
print()
print('example:')
print(credit_returns[0].bank_name)
print(credit_returns[0].account_type)
print(credit_returns[0].transaction_date)
print(credit_returns[0].transaction_description)
print(credit_returns[0].transaction_category)
print(credit_returns[0].transaction_type)
print(credit_returns[0].transaction_amount)
print()


# Need to add unrecognized transaction parameters to functions that lack them
# Then, need to add print statements for testing all the variables on this script

# Consider having inputs that ask about checking accounts and credit card accounts separately
# That way the accounts can be referenced separately and credit card payments can be identified and canceled

# Need to find a way to not rely on a set of valid banks and accounts, that way the application is more encompassing
# So, need to identify descriptions, categories, and types that apply to any bank and account

# At the end of the script (after categorization), present transactions that could not be automatically categorized and ask user to categorize them
# To do this, likely will need to pass uncategorized/unrecognized transactions from each function in a tuple


"""monthly_sorted_transactions_dictionary = personal_finances_module_v2.separate_and_sort_by_month(transactions_by_account_and_type)

for month_year, transactions in monthly_sorted_transactions_dictionary.items():
  if month_year == '11/2023':
    for transaction in transactions:
      print(f'\nDate: {transaction.transaction_date}\nCategory: {transaction.transaction_category}\nDescription: {transaction.transaction_description}\nAmount: {transaction.transaction_amount}')
print()"""


# To design a more robust and generalizable solution for categorizing transactions without relying solely on keywords, you can explore using machine learning techniques. Here are some steps and suggestions to help you approach this problem:

# Data Collection:
# Gather a diverse dataset of labeled transactions. You may need to manually label some transactions with their corresponding categories to create a training set.

# Feature Extraction:
# Identify relevant features in the transaction data that can be used for categorization. These features might include transaction amount, date, merchant name, and any other relevant information.

# Preprocessing:
# Clean and preprocess the data. This may involve handling missing values, normalizing numerical values, and converting categorical variables into a suitable format for machine learning algorithms.

# Model Selection:
# Choose a machine learning model that is suitable for your problem. Some common models for text-based categorization tasks are natural language processing (NLP) models, such as bag-of-words, TF-IDF, or word embeddings.

# Training the Model:
# Train your model on the labeled dataset using the chosen features. Ensure you split your dataset into training and testing sets to evaluate the model's performance.

# Evaluation:
# Evaluate the model's performance on the testing set. Use metrics such as accuracy, precision, recall, and F1 score to assess how well the model is categorizing transactions.

# Iterative Improvement:
# Based on the evaluation results, iterate on your model by tweaking hyperparameters, adding more features, or trying different algorithms to improve its performance.

# Deployment:
# Once satisfied with the model's performance, deploy it as part of your application. Make sure it's designed to handle transactions from various banks, accounts, and purchase types.

# User Feedback and Refinement:
# Collect user feedback and continually refine your model based on real-world usage and user suggestions. This could involve periodically retraining the model with new data.

# Consider External APIs:
# Some third-party APIs, like Plaid or Yodlee, provide access to transaction data from various banks. You might integrate such APIs into your application to obtain standardized and enriched transaction data.