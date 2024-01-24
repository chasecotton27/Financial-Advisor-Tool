import os
import csv


class TransactionRecord:

    def __init__(self, transaction, bank_name, account_type, transaction_date, transaction_type, transaction_category, transaction_description, transaction_amount):

        self.transactions = transaction
        self.bank_name = bank_name
        self.account_type = account_type
        self.transaction_date = transaction_date
        self.transaction_type = transaction_type
        self.transaction_category = transaction_category
        self.transaction_description = transaction_description
        self.transaction_amount = transaction_amount


def upload_file():

    file_name = input("Please move your CSV file into the dedicated folder called 'csv_files', then type the name of the file (including the .csv): ")
    file_path = os.path.join('.', 'csv_files', file_name)

    if not os.path.exists(file_path):
        print("File not found. Please check the file path.")
        return

    bank_name = input("Which financial institution is associated with this file? (Charles Schwab, Chase Bank, E-Trade, or Wells Fargo): ")
    account_type = input("What kind of account is associated with this file? (Checking Account, Credit Card Account, Investment Account, or Retirement Account): ")

    try:
        starting_row_index = int(input("In this CSV file, in which row does the transaction data begin? (Starting with 1 at the top, and not including headers): ")) - 1
        date_index = int(input("In this CSV file, which column contains the date of the transaction? (Starting with 1 on the left, and if there is no date, then type None): ")) - 1
        type_index = int(input("In this CSV file, which column contains the type of the transaction? (Starting with 1 on the left, and if there is no type, then type None): ")) - 1
        category_index = int(input("In this CSV file, which column contains the category of the transaction? (Starting with 1 on the left, and if there is no category, then type None): ")) - 1
        description_index = int(input("In this CSV file, which column contains the description of the transaction? (Starting with 1 on the left, and if there is no description, then type None): ")) - 1
        amount_index = int(input("In this CSV file, which column contains the amount of the transaction? (Starting with 1 on the left, and if there is no amount, then type None): ")) - 1
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return

    transactions = []

    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        i = 0
        for row in csv_reader:
            if i < starting_row_index or not row:
                pass
            elif len(row) <= max(date_index, type_index, category_index, description_index, amount_index):
                print("Error: Some specified indices are out of bounds for a row. Please check your input.")
                break
            else:
                transaction = TransactionRecord(row, bank_name, account_type, row[date_index], row[type_index], row[category_index], row[description_index], row[amount_index])
                transactions.append(transaction)
            i += 1

    return transactions


# Start of Version 2


"""def create_transactions(transactions_file):

  transactions = []

  with open(transactions_file, mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    if 'wells' in transactions_file or 'fargo' in transactions_file:
      organization = 'Wells Fargo'
    elif 'chase' in transactions_file:
      organization = 'Chase Bank'
    elif 'etrade' in transactions_file:
      organization = 'E-Trade'
    elif 'charles' in transactions_file or 'schwab' in transactions_file:
      organization = 'Charles Schwab'
    else:
      raise Exception('Unrecognized transactions file format.')

    if organization == 'Wells Fargo':
      for row in csv_reader:
        if len(row) == 0:
          pass
        else:
          row[1], row[4] = row[4], row[1]
          row[1], row[3] = row[3], row[1]
          row[1], row[2] = row[2], row[1]
          transactions.append(row)
    elif organization == 'Chase Bank':
      i = 0
      for row in csv_reader:
        if i == 0 or len(row) == 0:
          pass
        else:
          del row[1]
          del row[5]
          row[1], row[3] = row[3], row[1]
          transactions.append(row)
        i += 1
    elif organization == 'E-Trade':
      i = 0
      for row in csv_reader:
        if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or len(row) == 0:
          pass
        else:
          del row[3]
          del row[3]
          del row[4]
          del row[4]
          row[3], row[4] = row[4], row[3]
          transactions.append(row)
        i += 1
    elif organization == 'Charles Schwab':
      i = 0
      for row in csv_reader:
        if i == 0 or len(row) == 0:
          pass
        else:
          del row[2]
          del row[4]
          del row[4]
          del row[5]
          row[1], row[3] = row[3], row[1]
          transactions.append(row)
        i += 1

  return transactions


def incoming_or_outgoing(transactions):

  incoming_transactions = []
  outgoing_transactions = []

  for row in transactions:
    if float(row[4]) > 0:
      incoming_transactions.append(row)
    elif float(row[4]) < 0:
      outgoing_transactions.append(row)
    elif float(row[4]) == 0:
      pass
    else:
      raise Exception('Unrecognized transaction amount.')

  return incoming_transactions, outgoing_transactions


def categorize_incoming(incoming_transactions):

  adjustments = []
  contributions = []
  dividends = []
  employer_contributions = []
  interest = []
  payments = []
  payroll = []
  redemptions = []
  reorganizations = []
  returns = []
  stock_sales = []
  transfers = []
  tax_refunds = []
  miscellaneous = []

  for row in incoming_transactions:
    if row[1] == 'Adjustment':
      adjustments.append(row)
    elif row[2] == 'Contributions - Employee':
      contributions.append(row)
    elif row[1] == 'Dividend' or row[2] == 'Dividends/Capital Gains':
      dividends.append(row)
    elif row[2] == 'Contributions - Employer':
      employer_contributions.append(row)
    elif row[1] == 'Interest' or row[2] == 'Interest Earned':
      interest.append(row)
    elif row[1] == 'Payment':
      payments.append(row)
    elif 'NATIONAL INSTRUM PAYROLL' in row[3]:
      payroll.append(row)
    elif 'DISCOVER CASH AWARD' in row[3]:
      redemptions.append(row)
    elif row[1] == 'Reorganization':
      reorganizations.append(row)
    elif 'PURCHASE RETURN' in row[3] or row[1] == 'Return':
      returns.append(row)
    elif row[1] == 'Sold':
      stock_sales.append(row)
    elif  'APPLE CASH BANK XFER' in row[3] or 'MOBILE DEPOSIT' in row[3] or 'MSPBNA ACH TRNSFR' in row[3] or 'ONLINE TRANSFER FROM' in row[3] or 'VENMO CASHOUT' in row[3] or 'ZELLE FROM' in row[3] or row[1] == 'Transfer':
      transfers.append(row)
    elif 'IRS TREAS 310 TAX REF' in row[3]:
      tax_refunds.append(row)
    else:
      miscellaneous.append(row)

  return adjustments, contributions, dividends, employer_contributions, interest, payments, payroll, redemptions, reorganizations, returns, stock_sales, transfers, tax_refunds, miscellaneous"""


# Version 1


"""def create_and_structure_transaction_lists(credit_card_file, checking_account_file, retirement_account_file, investment_account_file):

  credit_purchases = []
  with open(credit_card_file, mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      if float(row[5]) < 0:
        credit_purchases.append(row)

  debit_purchases = []
  with open(checking_account_file, mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      if float(row[1]) < 0 and 'CHASE CREDIT CRD' not in row[4] and 'DISCOVER E-PAYMENT' not in row[4] and 'MSPBNA ACH' not in row[4]:
        debit_purchases.append(row)

  income = []
  with open(checking_account_file, mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      if float(row[1]) > 0 and 'MSPBNA ACH' not in row[4] and 'DISCOVER CASH' not in row[4]:
        income.append(row)

  retirement = []
  with open(retirement_account_file, mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      if row[4] != 'Purchase' and row[4] != 'Cash Disbursement' and row[3] != 'Dividends/Capital Gains' and row[3] != 'Interest Earned' and row[3] != 'Transfers In/Out':
        retirement.append(row)

  investments = []
  with open(investment_account_file, mode = 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      if 'Misc Trade' in row[1] or 'Reorganization' in row[1] or 'Transfer' in row[1]:
        investments.append(row)

  for row in credit_purchases:
    del row[1]
    del row[3]

  for row in debit_purchases:
    del row[2]
    row[1], row[3] = row[3], row[1]

  for row in income:
    del row[2]
    row[1], row[3] = row[3], row[1]

  for row in retirement:
    row[0] = row[0][:-5]
    del row[1]
    del row[1]
    del row[3]
    del row[3]

  for row in investments:
    del row[2]
    del row[2]
    del row[2]
    del row[3]
    del row[3]
    row[1], row[3] = row[3], row[1]
    row[2], row[3] = row[3], row[2]

  return credit_purchases, debit_purchases, income, retirement, investments


def sort_transactions(transactions):

  sorted_transactions = sorted(transactions, key=lambda x: datetime.strptime(x[0], "%m/%d/%Y"))

  return sorted_transactions


def only_include_month_and_year(transactions, month, year):

  transactions_during_month_and_year = []
  alternate_month = '0' + month
  alternate_year = '20' + year

  for row in transactions:
    month_letters = []
    year_letters = []
    date = row[0]
    for letter in date:
      if letter == '/':
        break
      else:
        month_letters.append(letter)
    for letter in date[::-1]:
      if letter == '/':
        break
      else:
        year_letters.append(letter)
    combined_month_letters = ''.join(month_letters)
    combined_year_letters = ''.join(year_letters)
    reversed_year_letters = combined_year_letters[::-1]
    if (combined_month_letters == month or combined_month_letters == alternate_month) and (reversed_year_letters == year or reversed_year_letters == alternate_year):
      transactions_during_month_and_year.append(row)

  return transactions_during_month_and_year


def categorize_purchases(purchases):

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

  return contributions, employer_contributions, withdrawals, fees, reorganizations


class TransactionCategories:

  def __init__(self, transactions):

    self.transactions = transactions

  def calculate_sum(self):

    sum = 0
    for row in self.transactions:
      sum += float(row[3])

    return sum


def display_wants_needs_savings(total_purchases, total_income, total_savings):

  salary = abs(total_income[0].calculate_sum() + total_savings[0].calculate_sum() + total_savings[1].calculate_sum())

  wants = abs(total_purchases[1].calculate_sum() + total_purchases[5].calculate_sum() + total_purchases[6].calculate_sum() + total_purchases[9].calculate_sum() + total_purchases[10].calculate_sum() + total_income[1].calculate_sum())
  needs = abs(total_purchases[0].calculate_sum() + total_purchases[2].calculate_sum() + total_purchases[3].calculate_sum() + total_purchases[4].calculate_sum() + total_purchases[7].calculate_sum() + total_purchases[8].calculate_sum() + total_income[2].calculate_sum() + total_savings[2].calculate_sum() + total_savings[3].calculate_sum())
  savings = abs(total_savings[0].calculate_sum() + total_savings[1].calculate_sum() + total_savings[4].calculate_sum())
  left_over = abs(salary - wants - needs - savings)

  percentage_wants = (wants/salary)*100
  percentage_needs = (needs/salary)*100
  percentage_savings = (savings/salary)*100
  percentage_left_over = (left_over/salary)*100

  print(f'\nIncome:  ${salary: .2f}\n------------------------------------')
  print(f'Salary:  ${abs(total_income[0].calculate_sum()): .2f}\nInvestment Contributions:  ${abs(total_savings[0].calculate_sum()): .2f}\nEmployer Contributions:  ${abs(total_savings[1].calculate_sum()): .2f}\n')
  print(f'\nWants:  ${wants: .2f}  ({percentage_wants: .2f}% )\n------------------------------------')
  print(f'Entertainment:  ${abs(total_purchases[1].calculate_sum()): .2f}\nMiscellaneous:  ${abs(total_purchases[5].calculate_sum()): .2f}\nPersonal:  ${abs(total_purchases[6].calculate_sum()): .2f}\nShopping:  ${abs(total_purchases[9].calculate_sum()): .2f}\nTravel:  ${abs(total_purchases[10].calculate_sum()): .2f}\nWants Reimbursement:  ${abs(total_income[1].calculate_sum()): .2f}\n')
  print(f'\nNeeds:  ${needs: .2f}  ({percentage_needs: .2f}% )\n------------------------------------')
  print(f'Automotive:  ${abs(total_purchases[0].calculate_sum()): .2f}\nGas Stations:  ${abs(total_purchases[2].calculate_sum()): .2f}\nGroceries:  ${abs(total_purchases[3].calculate_sum()): .2f}\nHealth:  ${abs(total_purchases[4].calculate_sum()): .2f}\nRent and Utilities:  ${abs(total_purchases[7].calculate_sum()): .2f}\nRestaurants:  ${abs(total_purchases[8].calculate_sum()): .2f}\nNeeds Reimbursement:  ${abs(total_income[2].calculate_sum()): .2f}\nSavings Withdrawals:  ${abs(total_savings[2].calculate_sum()): .2f}\nSavings Fees:  ${abs(total_savings[3].calculate_sum()): .2f}\n')
  print(f'\nSavings:  ${savings: .2f}  ({percentage_savings: .2f}% )\n------------------------------------')
  print(f'Investment Contributions:  ${abs(total_savings[0].calculate_sum()): .2f}\nEmployer Contributions:  ${abs(total_savings[1].calculate_sum()): .2f}\nReorganizations:  ${abs(total_savings[4].calculate_sum()): .2f}\n')
  print(f'\nLeft Over:  ${left_over: .2f}  ({percentage_left_over: .2f}% )\n------------------------------------\n')"""