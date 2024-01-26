import personal_finances_module_v2


transactions_by_account = []
uploading_files = True

while uploading_files:
  transactions = personal_finances_module_v2.upload_file()
  transactions_by_account.append(transactions)

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
unrecognized_transactions = []

for account in transactions_by_account:
  incoming_transactions = personal_finances_module_v2.incoming_or_outgoing(account)[0]
  outgoing_transactions = personal_finances_module_v2.incoming_or_outgoing(account)[1]
  null_transactions = personal_finances_module_v2.incoming_or_outgoing(account)[2]
  transactions_by_account_and_type.append([incoming_transactions, outgoing_transactions])
  unrecognized_transactions.append(null_transactions)

credit_payments_by_account = []
credit_returns_by_account = []

for account in transactions_by_account_and_type:
  for type in account:
    if type[0].account_type == 'credit card' and type[0].transaction_amount > 0:
      credit_payments = personal_finances_module_v2.identify_credit_payments(type)
      credit_returns = personal_finances_module_v2.identify_credit_returns(type)
      credit_payments_by_account.append(credit_payments)
      credit_returns_by_account.append(credit_returns)

total_credit_payments = [credit_payment for credit_payments in credit_payments_by_account for credit_payment in credit_payments]
total_credit_returns = [credit_return for credit_returns in credit_returns_by_account for credit_return in credit_returns]


# Consider having inputs that ask about checking accounts and credit card accounts separately
# That way the accounts can be referenced separately and credit card payments can be identified and canceled
# Might want to move incoming_or_outgoing to after separate_and_sort_by_month
# At the end of the script (after categorization), present transactions that could not be automatically categorized and ask user to categorize them
# ... to do this, likely will need to pass uncategorized/unrecognized transactions from each function in a tuple


"""monthly_sorted_transactions_dictionary = personal_finances_module_v2.separate_and_sort_by_month(transactions_by_account_and_type)

for month_year, transactions in monthly_sorted_transactions_dictionary.items():
  if month_year == '11/2023':
    for transaction in transactions:
      print(f'\nDate: {transaction.transaction_date}\nCategory: {transaction.transaction_category}\nDescription: {transaction.transaction_description}\nAmount: {transaction.transaction_amount}')
print()"""