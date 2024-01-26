# Expense sharing application

## Overview
This application is designed to manage expenses among a group of users. Used Flask to provide a RESTful API for user and expense management. The core components include the User, Split, Expense and ExpenseManager classes which collectively handle user information, expense details and balance calculations.

### Architecture Diagram
      +------------------+
      |    Flask App     |
      +------------------+
               |
      +------------------+
      | ExpenseManager   |
      |   - Users        |
      |   - Expenses     |
      |   - Balance Sheet|
      +------------------+
           |          |
      +----------+ +----------+
      | User    | | Expense   |
      | - ID    | | - Amount  |
      | - Name  | | - Paid By |
      | - Email | | - Splits  |
      | - Mobile| | - Metadata|
      +---------+ +-------+
      | Split   | | +-----+
      | - User  | | Equal  |
      | - Amount| | Exact  |
      +---------+ | Percent|

### Class Structure
- User: Represents a user in the system with attributes user_id, name, email and mobile.

- Split: Abstract class representing a general split with attributes user and amount.

- EqualSplit: Subclass of Split for equal splits.

- ExactSplit: Subclass of Split for exact splits.

- PercentSplit: Subclass of Split for percentage-based splits.

- ExpenseMetadata: Represents metadata associated with an expense, including name, img_url and notes.

- Expense: Abstract class representing an expense with attributes amount, paid_by, splits and optional metadata.

- EqualExpense: Subclass of Expense for equal splits.

- ExactExpense: Subclass of Expense for exact splits.

- PercentExpense: Subclass of Expense for percentage-based splits.

- ExpenseType: Enumeration class defining expense types: EQUAL, EXACT, PERCENT.

- ExpenseService: Provides a static method create_expense for creating expense objects based on the provided type.

- ExpenseManager: Manages users, expenses, and balances with methods for adding users, adding expenses, updating balances and retrieving balance information.

## API endpoints

### Add User

#### Endpoint: /add_user
#### Method: POST
#### Request
```json
{
  "user_id": "string",
  "name": "string",
  "email": "string",
  "mobile": "string"
}
```

#### Response
```json
{
  "message": "User added successfully"
}
```

### Add Expense

#### Endpoint: /add_expense
#### Method: POST
#### Request
```json
{
  "paid_by": "string",
  "amount": "float",
  "expense_type": "string (EQUAL, EXACT, or PERCENT)",
  "splits": [
    {
      "user_id": "string",
      "amount": "float (for EXACT expense_type)",
      "percent": "float (for PERCENT expense_type)"
    },
    ...
  ]
}
```
#### Response
```json
{
  "message": "Expense added successfully"
}
```

### Show Balances

#### Endpoint: /show_balances
#### Method: GET
#### Query Parameter: user_id (optional)
#### Response
```json
{
  "balances": ["string", ...]
}
```

## Getting Started
- Clone the repository
- Install required dependencies: pip install flask
- Run the application: python teachmintassign.py
- Use the provided APIs to manage users and expenses
