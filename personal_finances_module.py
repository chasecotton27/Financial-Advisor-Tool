import csv
from datetime import datetime


def create_and_structure_transaction_lists(credit_card_file, checking_account_file, retirement_account_file, investment_account_file):

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

  print(f'\nIncome:  ${salary: .2f}\n--------------------------------')
  print(f'Salary:  ${abs(total_income[0].calculate_sum()): .2f}\nInvestments Witthheld:  ${abs(total_savings[0].calculate_sum()): .2f}\nEmployer Contributions:  ${abs(total_savings[1].calculate_sum()): .2f}\n')
  print(f'\nWants:  ${wants: .2f}  ({percentage_wants: .2f}% )\n--------------------------------')
  print(f'Entertainment:  ${abs(total_purchases[1].calculate_sum()): .2f}\nMiscellaneous:  ${abs(total_purchases[5].calculate_sum()): .2f}\nPersonal:  ${abs(total_purchases[6].calculate_sum()): .2f}\nShopping:  ${abs(total_purchases[9].calculate_sum()): .2f}\nTravel:  ${abs(total_purchases[10].calculate_sum()): .2f}\nWants Reimbursement:  ${abs(total_income[1].calculate_sum()): .2f}\n')
  print(f'\nNeeds:  ${needs: .2f}  ({percentage_needs: .2f}% )\n--------------------------------')
  print(f'Automotive:  ${abs(total_purchases[0].calculate_sum()): .2f}\nGas Stations:  ${abs(total_purchases[2].calculate_sum()): .2f}\nGroceries:  ${abs(total_purchases[3].calculate_sum()): .2f}\nHealth:  ${abs(total_purchases[4].calculate_sum()): .2f}\nRent and Utilities:  ${abs(total_purchases[7].calculate_sum()): .2f}\nRestaurants:  ${abs(total_purchases[8].calculate_sum()): .2f}\nNeeds Reimbursement:  ${abs(total_income[2].calculate_sum()): .2f}\nSavings Withdrawals:  ${abs(total_savings[2].calculate_sum()): .2f}\nSavings Fees:  ${abs(total_savings[3].calculate_sum()): .2f}\n')
  print(f'\nSavings:  ${savings: .2f}  ({percentage_savings: .2f}% )\n--------------------------------')
  print(f'Contributions:  ${abs(total_savings[0].calculate_sum()): .2f}\nEmployer Contributions:  ${abs(total_savings[1].calculate_sum()): .2f}\nReorganizations:  ${abs(total_savings[4].calculate_sum()): .2f}\n')
  print(f'\nLeft Over:  ${left_over: .2f}  ({percentage_left_over: .2f}% )\n--------------------------------\n')