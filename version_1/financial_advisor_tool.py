import personal_finances_module

month = '12'
year = '23'
credit_card_transactions = 'credit_card_transactions.csv'
checking_account_transactions = 'checking_account_transactions.csv'
retirement_account_transactions = 'retirement_account_transactions.csv'
investment_account_transactions = 'investment_account_transactions.csv'

transaction_lists = personal_finances_module.create_and_structure_transaction_lists(credit_card_transactions, checking_account_transactions, retirement_account_transactions, investment_account_transactions)

credit_purchases = transaction_lists[0]
debit_purchases = transaction_lists[1]
purchases = credit_purchases + debit_purchases
income = transaction_lists[2]
retirement = transaction_lists[3]
investments = transaction_lists[4]
savings = retirement + investments

sorted_purchases = personal_finances_module.sort_transactions(purchases)
sorted_income = personal_finances_module.sort_transactions(income)
sorted_savings = personal_finances_module.sort_transactions(savings)

purchases_by_month = personal_finances_module.only_include_month_and_year(sorted_purchases, month, year)
income_by_month = personal_finances_module.only_include_month_and_year(sorted_income, month, year)
savings_by_month = personal_finances_module.only_include_month_and_year(sorted_savings, month, year)

categorized_purchases = personal_finances_module.categorize_purchases(purchases_by_month)
categorized_income = personal_finances_module.categorize_income(income_by_month)
categorized_savings = personal_finances_module.categorize_savings(savings_by_month)

purchases_automotive = personal_finances_module.TransactionCategories(categorized_purchases[0])
purchases_entertainment = personal_finances_module.TransactionCategories(categorized_purchases[1])
purchases_gas_stations = personal_finances_module.TransactionCategories(categorized_purchases[2])
purchases_groceries = personal_finances_module.TransactionCategories(categorized_purchases[3])
purchases_health = personal_finances_module.TransactionCategories(categorized_purchases[4])
purchases_miscellaneous = personal_finances_module.TransactionCategories(categorized_purchases[5])
purchases_personal = personal_finances_module.TransactionCategories(categorized_purchases[6])
purchases_rent_and_utilities = personal_finances_module.TransactionCategories(categorized_purchases[7])
purchases_restaurants = personal_finances_module.TransactionCategories(categorized_purchases[8])
purchases_shopping = personal_finances_module.TransactionCategories(categorized_purchases[9])
purchases_travel = personal_finances_module.TransactionCategories(categorized_purchases[10])

income_salary = personal_finances_module.TransactionCategories(categorized_income[0])
income_wants_reimbursement = personal_finances_module.TransactionCategories(categorized_income[1])
income_needs_reimbursement = personal_finances_module.TransactionCategories(categorized_income[2])

savings_contributions = personal_finances_module.TransactionCategories(categorized_savings[0])
savings_employer_contributions =personal_finances_module.TransactionCategories(categorized_savings[1])
savings_withdrawals = personal_finances_module.TransactionCategories(categorized_savings[2])
savings_fees = personal_finances_module.TransactionCategories(categorized_savings[3])
savings_reorganizations = personal_finances_module.TransactionCategories(categorized_savings[4])

purchases_with_category_classes = [purchases_automotive, purchases_entertainment, purchases_gas_stations, purchases_groceries, purchases_health, purchases_miscellaneous, purchases_personal, purchases_rent_and_utilities, purchases_restaurants, purchases_shopping, purchases_travel]
income_with_category_classes = [income_salary, income_wants_reimbursement, income_needs_reimbursement]
savings_with_category_classes = [savings_contributions, savings_employer_contributions, savings_withdrawals, savings_fees, savings_reorganizations]

personal_finances_module.display_wants_needs_savings(purchases_with_category_classes, income_with_category_classes, savings_with_category_classes)

# Next, combine the categorize functions into a single function
# Ideally, each function would only have one parameter, that way the application is not dependent on how many accounts the user has
# Then, work towards eliminating hard-coded values, increasing the range of the functions for general cases, and improving error handling for general cases