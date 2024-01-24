import personal_finances_module_v2


uploading_files = True
total_transactions = []

while uploading_files:
  transactions = personal_finances_module_v2.upload_file()
  total_transactions.append(transactions)
  still_uploading = input('Would you like to upload another CSV file? (Yes or No): ')

  if still_uploading == 'Yes':
    pass
  elif still_uploading == 'No':
    uploading_files = False
  else:
    print('Invalid input. Please enter Yes or No.')
    break

print(total_transactions)


# Need to figure out how to handle cases where user types None for column numbers


# Start of Version 2


"""checking_transactions_file = '.\csv_files\wells_fargo_checking_account_transactions.csv'
credit_card_transactions_file = '.\csv_files\chase_credit_card_account_transactions.csv'
brokerage_transactions_file = '.\csv_files\etrade_brokerage_account_transactions.csv'
retirement_transactions_file = '.\csv_files\charles_schwab_retirement_account_transactions.csv'

checking_transactions = personal_finances_module_v2.create_transactions(checking_transactions_file)
credit_card_transactions = personal_finances_module_v2.create_transactions(credit_card_transactions_file)
brokerage_transactions = personal_finances_module_v2.create_transactions(brokerage_transactions_file)
retirement_transactions = personal_finances_module_v2.create_transactions(retirement_transactions_file)

incoming_checking = personal_finances_module_v2.incoming_or_outgoing(checking_transactions)[0]
outgoing_checking = personal_finances_module_v2.incoming_or_outgoing(checking_transactions)[1]
incoming_credit_card = personal_finances_module_v2.incoming_or_outgoing(credit_card_transactions)[0]
outgoing_credit_card = personal_finances_module_v2.incoming_or_outgoing(credit_card_transactions)[1]
incoming_brokerage = personal_finances_module_v2.incoming_or_outgoing(brokerage_transactions)[0]
outgoing_brokerage = personal_finances_module_v2.incoming_or_outgoing(brokerage_transactions)[1]
incoming_retirement = personal_finances_module_v2.incoming_or_outgoing(retirement_transactions)[0]
outgoing_retirement = personal_finances_module_v2.incoming_or_outgoing(retirement_transactions)[1]

categorized_incoming_checking = personal_finances_module_v2.categorize_incoming(incoming_checking)
categorized_incoming_credit_card = personal_finances_module_v2.categorize_incoming(incoming_credit_card)
categorized_incoming_brokerage = personal_finances_module_v2.categorize_incoming(incoming_brokerage)
categorized_incoming_retirement = personal_finances_module_v2.categorize_incoming(incoming_retirement)

adjustments = categorized_incoming_checking[0] + categorized_incoming_credit_card[0] + categorized_incoming_brokerage[0] + categorized_incoming_retirement[0]
contributions = categorized_incoming_checking[1] + categorized_incoming_credit_card[1] + categorized_incoming_brokerage[1] + categorized_incoming_retirement[1]
dividends = categorized_incoming_checking[2] + categorized_incoming_credit_card[2] + categorized_incoming_brokerage[2] + categorized_incoming_retirement[2]
employer_contributions = categorized_incoming_checking[3] + categorized_incoming_credit_card[3] + categorized_incoming_brokerage[3] + categorized_incoming_retirement[3]
interest = categorized_incoming_checking[4] + categorized_incoming_credit_card[4] + categorized_incoming_brokerage[4] + categorized_incoming_retirement[4]
payments = categorized_incoming_checking[5] + categorized_incoming_credit_card[5] + categorized_incoming_brokerage[5] + categorized_incoming_retirement[5]
payroll = categorized_incoming_checking[6] + categorized_incoming_credit_card[6] + categorized_incoming_brokerage[6] + categorized_incoming_retirement[6]
redemptions = categorized_incoming_checking[7] + categorized_incoming_credit_card[7] + categorized_incoming_brokerage[7] + categorized_incoming_retirement[7]
reorganizations = categorized_incoming_checking[8] + categorized_incoming_credit_card[8] + categorized_incoming_brokerage[8] + categorized_incoming_retirement[8]
returns = categorized_incoming_checking[9] + categorized_incoming_credit_card[9] + categorized_incoming_brokerage[9] + categorized_incoming_retirement[9]
stock_sales = categorized_incoming_checking[10] + categorized_incoming_credit_card[10] + categorized_incoming_brokerage[10] + categorized_incoming_retirement[10]
transfers = categorized_incoming_checking[11] + categorized_incoming_credit_card[11] + categorized_incoming_brokerage[11] + categorized_incoming_retirement[11]
tax_refunds = categorized_incoming_checking[12] + categorized_incoming_credit_card[12] + categorized_incoming_brokerage[12] + categorized_incoming_retirement[12]
miscellaneous = categorized_incoming_checking[13] + categorized_incoming_credit_card[13] + categorized_incoming_brokerage[13] + categorized_incoming_retirement[13]"""


# Version 1


"""transaction_lists = personal_finances_module_v2.create_and_structure_transaction_lists(credit_card_transactions, checking_account_transactions, retirement_account_transactions, investment_account_transactions)

credit_purchases = transaction_lists[0]
debit_purchases = transaction_lists[1]
purchases = credit_purchases + debit_purchases
income = transaction_lists[2]
retirement = transaction_lists[3]
investments = transaction_lists[4]
savings = retirement + investments

sorted_purchases = personal_finances_module_v2.sort_transactions(purchases)
sorted_income = personal_finances_module_v2.sort_transactions(income)
sorted_savings = personal_finances_module_v2.sort_transactions(savings)

purchases_by_month = personal_finances_module_v2.only_include_month_and_year(sorted_purchases, month, year)
income_by_month = personal_finances_module_v2.only_include_month_and_year(sorted_income, month, year)
savings_by_month = personal_finances_module_v2.only_include_month_and_year(sorted_savings, month, year)

categorized_purchases = personal_finances_module_v2.categorize_purchases(purchases_by_month)
categorized_income = personal_finances_module_v2.categorize_income(income_by_month)
categorized_savings = personal_finances_module_v2.categorize_savings(savings_by_month)

purchases_automotive = personal_finances_module_v2.TransactionCategories(categorized_purchases[0])
purchases_entertainment = personal_finances_module_v2.TransactionCategories(categorized_purchases[1])
purchases_gas_stations = personal_finances_module_v2.TransactionCategories(categorized_purchases[2])
purchases_groceries = personal_finances_module_v2.TransactionCategories(categorized_purchases[3])
purchases_health = personal_finances_module_v2.TransactionCategories(categorized_purchases[4])
purchases_miscellaneous = personal_finances_module_v2.TransactionCategories(categorized_purchases[5])
purchases_personal = personal_finances_module_v2.TransactionCategories(categorized_purchases[6])
purchases_rent_and_utilities = personal_finances_module_v2.TransactionCategories(categorized_purchases[7])
purchases_restaurants = personal_finances_module_v2.TransactionCategories(categorized_purchases[8])
purchases_shopping = personal_finances_module_v2.TransactionCategories(categorized_purchases[9])
purchases_travel = personal_finances_module_v2.TransactionCategories(categorized_purchases[10])

income_salary = personal_finances_module_v2.TransactionCategories(categorized_income[0])
income_wants_reimbursement = personal_finances_module_v2.TransactionCategories(categorized_income[1])
income_needs_reimbursement = personal_finances_module_v2.TransactionCategories(categorized_income[2])

savings_contributions = personal_finances_module_v2.TransactionCategories(categorized_savings[0])
savings_employer_contributions =personal_finances_module_v2.TransactionCategories(categorized_savings[1])
savings_withdrawals = personal_finances_module_v2.TransactionCategories(categorized_savings[2])
savings_fees = personal_finances_module_v2.TransactionCategories(categorized_savings[3])
savings_reorganizations = personal_finances_module_v2.TransactionCategories(categorized_savings[4])

purchases_with_category_classes = [purchases_automotive, purchases_entertainment, purchases_gas_stations, purchases_groceries, purchases_health, purchases_miscellaneous, purchases_personal, purchases_rent_and_utilities, purchases_restaurants, purchases_shopping, purchases_travel]
income_with_category_classes = [income_salary, income_wants_reimbursement, income_needs_reimbursement]
savings_with_category_classes = [savings_contributions, savings_employer_contributions, savings_withdrawals, savings_fees, savings_reorganizations]

personal_finances_module_v2.display_wants_needs_savings(purchases_with_category_classes, income_with_category_classes, savings_with_category_classes)"""