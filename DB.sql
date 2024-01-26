-- User table to store user information
CREATE TABLE User (
    user_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mobile VARCHAR(15) NOT NULL
);

-- Split table to store information about splits
CREATE TABLE Split (
    split_id INT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- ExpenseMetadata table to store metadata associated with an expense
CREATE TABLE ExpenseMetadata (
    expense_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    img_url VARCHAR(255),
    notes TEXT
);

-- Expense table to store information about expenses
CREATE TABLE Expense (
    expense_id INT PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    paid_by INT,
    metadata_id INT,
    FOREIGN KEY (paid_by) REFERENCES User(user_id),
    FOREIGN KEY (metadata_id) REFERENCES ExpenseMetadata(expense_id)
);

-- ExpenseSplit table to link expenses with splits (many-to-many relationship)
CREATE TABLE ExpenseSplit (
    expense_id INT,
    split_id INT,
    PRIMARY KEY (expense_id, split_id),
    FOREIGN KEY (expense_id) REFERENCES Expense(expense_id),
    FOREIGN KEY (split_id) REFERENCES Split(split_id)
);

-- Enum table to store expense types
CREATE TABLE ExpenseType (
    type_id INT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL
);

-- ExpenseTypeMapping table to map expenses to their types
CREATE TABLE ExpenseTypeMapping (
    expense_id INT,
    type_id INT,
    PRIMARY KEY (expense_id, type_id),
    FOREIGN KEY (expense_id) REFERENCES Expense(expense_id),
    FOREIGN KEY (type_id) REFERENCES ExpenseType(type_id)
);

-- Balance table to store balance information between users
CREATE TABLE Balance (
    user1_id INT,
    user2_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (user1_id, user2_id),
    FOREIGN KEY (user1_id) REFERENCES User(user_id),
    FOREIGN KEY (user2_id) REFERENCES User(user_id)
);
