import personal_finances_module

transaction_lists = personal_finances_module.create_and_structure_transaction_lists('credit_card_transactions.csv', 'checking_account_transactions.csv', 'retirement_account_transactions.csv', 'investment_account_transactions.csv')

credit_purchases = transaction_lists[0]
debit_purchases = transaction_lists[1]
purchases = credit_purchases + debit_purchases
sorted_purchases = personal_finances_module.sort_transactions(purchases)
purchases_by_month = personal_finances_module.only_include_month_and_year(sorted_purchases, '12', '23')
categorized_purchases = personal_finances_module.categorize_purchases(purchases_by_month)

automotive = personal_finances_module.TransactionCategories(categorized_purchases[0])
entertainment = personal_finances_module.TransactionCategories(categorized_purchases[1])
gas_stations = personal_finances_module.TransactionCategories(categorized_purchases[2])
groceries = personal_finances_module.TransactionCategories(categorized_purchases[3])
health = personal_finances_module.TransactionCategories(categorized_purchases[4])
miscellaneous = personal_finances_module.TransactionCategories(categorized_purchases[5])
personal = personal_finances_module.TransactionCategories(categorized_purchases[6])
rent_and_utilities = personal_finances_module.TransactionCategories(categorized_purchases[7])
restaurants = personal_finances_module.TransactionCategories(categorized_purchases[8])
shopping = personal_finances_module.TransactionCategories(categorized_purchases[9])
travel = personal_finances_module.TransactionCategories(categorized_purchases[10])

purchases_with_category_classes = [automotive, entertainment, gas_stations, groceries, health, miscellaneous, personal, rent_and_utilities, restaurants, shopping, travel]

income = transaction_lists[2]
sorted_income = personal_finances_module.sort_transactions(income)
income_by_month = personal_finances_module.only_include_month_and_year(sorted_income, '12', '23')
differentiated_income = personal_finances_module.differentiate_income(income_by_month)

salary_income = personal_finances_module.TransactionCategories(differentiated_income[0])
wants_reimbursement = personal_finances_module.TransactionCategories(differentiated_income[1])
needs_reimbursement = personal_finances_module.TransactionCategories(differentiated_income[2])

income_with_category_classes = [salary_income, wants_reimbursement, needs_reimbursement]

retirement = transaction_lists[3]
investments = transaction_lists[4]
savings = retirement + investments
sorted_savings = personal_finances_module.sort_transactions(savings)
savings_by_month = personal_finances_module.only_include_month_and_year(sorted_savings, '12', '23')
differentiated_savings = personal_finances_module.differentiate_savings(savings_by_month)

savings_contributions = personal_finances_module.TransactionCategories(differentiated_savings[0])
savings_employer_contributions =personal_finances_module.TransactionCategories(differentiated_savings[1])
savings_withdrawals = personal_finances_module.TransactionCategories(differentiated_savings[2])
savings_fees = personal_finances_module.TransactionCategories(differentiated_savings[3])

savings_with_category_classes = [savings_contributions, savings_employer_contributions, savings_withdrawals, savings_fees]

personal_finances_module.display_wants_needs_savings(purchases_with_category_classes, income_with_category_classes, savings_with_category_classes)