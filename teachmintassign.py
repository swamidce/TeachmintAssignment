# Import necessary modules from Flask
from flask import Flask, request, jsonify

# Create a Flask application instance
app = Flask(__name__)

# Initialize a variable to hold the ExpenseManager instance
expense_manager = None

# Define a User class with attributes for user details
class User:
    def __init__(self, user_id, name, email, mobile):
        # Constructor for User class, initializes user attributes
        self.user_id = user_id
        self.name = name
        self.email = email
        self.mobile = mobile

# Define a Split class with attributes for splitting expenses
class Split:
    def __init__(self, user, amount=0):
        # Constructor for Split class, initializes split attributes
        self.user = user
        self.amount = amount

# Define subclasses for different types of splits
class EqualSplit(Split):
    # Subclass of Split for equal splits
    pass

class ExactSplit(Split):
    # Subclass of Split for exact splits
    pass

class PercentSplit(Split):
    def __init__(self, user, percent=0):
        # Constructor for PercentSplit class, initializes percent split attributes
        super().__init__(user)
        self.percent = percent

# Define a class for metadata associated with an expense
class ExpenseMetadata:
    def __init__(self, name, img_url, notes):
        # Constructor for ExpenseMetadata class, initializes metadata attributes
        self.name = name
        self.img_url = img_url
        self.notes = notes

# Define an Expense class with attributes for an expense
class Expense:
    def __init__(self, amount, paid_by, splits, metadata=None):
        # Constructor for Expense class, initializes expense attributes
        self.amount = amount
        self.paid_by = paid_by
        self.splits = splits
        self.metadata = metadata

    def validate(self):
        # Abstract method to be implemented by subclasses
        pass

# Define subclasses for different types of expenses
class EqualExpense(Expense):
    def validate(self):
        # Validates if all splits in the expense are of type EqualSplit
        return all(isinstance(split, EqualSplit) for split in self.splits)

class ExactExpense(Expense):
    def validate(self):
        # Validates if all splits in the expense are of type ExactSplit
        # and if the total amount matches the specified amount
        if not all(isinstance(split, ExactSplit) for split in self.splits):
            return False
        total_amount = sum(split.amount for split in self.splits)
        return total_amount == self.amount

class PercentExpense(Expense):
    def validate(self):
        # Validates if all splits in the expense are of type PercentSplit
        # and if the total percentage is 100
        if not all(isinstance(split, PercentSplit) for split in self.splits):
            return False
        total_percent = sum(split.percent for split in self.splits)
        return total_percent == 100

# Define an enumeration class for expense types
class ExpenseType:
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENT = "PERCENT"

# Define a class for handling expense-related operations
class ExpenseService:
    @staticmethod
    def create_expense(expense_type, amount, paid_by, splits, metadata=None):
        # Static method to create an expense based on the provided type
        if expense_type == ExpenseType.EXACT:
            return ExactExpense(amount, paid_by, splits, metadata)
        elif expense_type == ExpenseType.PERCENT:
            for percent_split in splits:
                percent_split.amount = (amount * percent_split.percent) / 100
            return PercentExpense(amount, paid_by, splits, metadata)
        elif expense_type == ExpenseType.EQUAL:
            total_splits = len(splits)
            split_amount = round(amount / total_splits, 2)
            for split in splits:
                split.amount = split_amount
            splits[0].amount += (amount - split_amount * total_splits)
            return EqualExpense(amount, paid_by, splits, metadata)
        else:
            return None

# Define a class for managing expenses, users and balances
class ExpenseManager:
    def __init__(self):
        # Constructor for ExpenseManager class, initializes manager attributes
        self.expenses = []
        self.user_map = {}
        self.balance_sheet = {}

    def add_user(self, user):
        # Adds a user to the user_map and initializes their balance sheet
        self.user_map[user.user_id] = user
        self.balance_sheet[user.user_id] = {}

    def add_expense(self, expense_type, amount, paid_by, splits, metadata=None):
        # Adds an expense, updates balance sheet and stores the expense
        expense = ExpenseService.create_expense(expense_type, amount, self.user_map[paid_by], splits, metadata)
        self.expenses.append(expense)

        for split in expense.splits:
            paid_to = split.user.user_id
            self.update_balance(paid_by, paid_to, split.amount)

    def update_balance(self, user1, user2, amount):
        # Updates the balance between two users
        if user2 not in self.balance_sheet[user1]:
            self.balance_sheet[user1][user2] = 0
        self.balance_sheet[user1][user2] += amount

        if user1 not in self.balance_sheet[user2]:
            self.balance_sheet[user2][user1] = 0
        self.balance_sheet[user2][user1] -= amount

    def show_balance(self, user_id):
        # Returns the balance for a specific user
        balances = set()
        for user, amount in self.balance_sheet[user_id].items():
            if amount != 0:
                user_name = self.user_map[user].name
                balance_info = f"owes {user_name}: {abs(amount)}" if amount < 0 else f"{user_name} owes {amount}"
                balances.add(balance_info)
        return list(balances)

    def show_balances(self):
        # Displays balances for all users
        balances = set()  # Use a set to store unique balances
        for user1, user2_balance in self.balance_sheet.items():
            for user2, amount in user2_balance.items():
                if amount != 0:
                    user1_name = self.user_map[user1].name
                    user2_name = self.user_map[user2].name
                    balance_info = f"{user1_name} owes {user2_name}: {abs(amount)}" if amount < 0 else f"{user2_name} owes {user1_name}: {amount}"
                    balances.add(balance_info)  # Add balance to set
        return list(balances)

    def print_balance(self, user1, user2, amount):
        # Prints the balance between two users
        user1_name = self.user_map[user1].name
        user2_name = self.user_map[user2].name
        if amount < 0:
            print(f"{user1_name} owes {user2_name}: {abs(amount)}")
        elif amount > 0:
            print(f"{user2_name} owes {user1_name}: {amount}")


# Define routes and request handling functions using Flask
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    user = User(data['user_id'], data['name'], data['email'], data['mobile'])
    expense_manager.add_user(user)
    return jsonify({"message": "User added successfully"}), 201

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    paid_by = data['paid_by']
    amount = float(data['amount'])
    expense_type = data['expense_type']
    splits = []

    for split_data in data['splits']:
        user_id = split_data['user_id']
        if expense_type == "EQUAL":
            splits.append(EqualSplit(expense_manager.user_map[user_id]))
        elif expense_type == "EXACT":
            splits.append(ExactSplit(expense_manager.user_map[user_id], float(split_data['amount'])))
        elif expense_type == "PERCENT":
            splits.append(PercentSplit(expense_manager.user_map[user_id], float(split_data['percent'])))

    expense_manager.add_expense(expense_type, amount, paid_by, splits)
    return jsonify({"message": "Expense added successfully"}), 201

@app.route('/show_balances', methods=['GET'])
def show_balances():
    user_id = request.args.get('user_id')
    if user_id:
        balances = expense_manager.show_balance(user_id)
    else:
        balances = expense_manager.show_balances()

    return jsonify({"balances": balances})


if __name__ == '__main__':
    # Create an instance of ExpenseManager
    expense_manager = ExpenseManager()
    app.run(debug=True)