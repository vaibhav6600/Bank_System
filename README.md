# 🏦 BankPro – Bank Management System

A full-featured **Bank Management System** built with Python and a modern **Streamlit** web interface.
It supports two user roles — **Admin** and **Customer** — with separate dashboards, access control, and a clean dark-themed UI.

---

## ✨ Features

### Admin Features
- **Create Customer** – Register a new customer (name, email, phone). A login account is automatically created with the default password `1234`.
- **Manage Customers** – View all customers, edit their details, or deactivate them. Inactive customers are shown with a **light red background**.
- **Create Account** – Open a bank account for any active customer with an initial deposit.
- **Manage Accounts** – View all accounts, edit account type or balance, or deactivate an account. Inactive accounts are shown with a **light red background**.
- **Deposit / Withdraw / Transfer** – Perform banking operations on any active account.
- **Display Balance** – View live balance and customer details for any account.
- **Transaction History** – See every deposit, withdrawal, and transfer across all accounts.
- **Live Dashboard** – Real-time stats: total active customers, accounts, and bank balance.

### Customer Features
- **Self-Registration** – Customers can register themselves from the login page. They set their own password during registration.
- **Dashboard** – See their own accounts and total balance only.
- **Create Account** – Open a new account linked to their profile.
- **Deposit / Withdraw / Transfer** – Perform banking operations on their own accounts only.
- **Display Balance** – View their own account and personal details.
- **Transaction History** – See their own transactions only.

### Security
- Inactive customers **cannot log in**.
- Customers **cannot see** other customers' accounts or data.
- Deactivating a customer automatically deactivates all their accounts and blocks their login.
- Passwords are stored as **bcrypt hashes** (if `bcrypt` is installed) or plain text as a fallback.

---

## 📁 Project Structure

```
PythonProject/
│
├── app.py                  # Main Streamlit web application
├── login.py                # Login and self-registration page
├── main.py                 # CLI-based interface (optional)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .env                    # Database connection settings (not committed to git)
│
└── bank/                   # Core banking logic
    ├── __init__.py
    ├── auth.py             # Login, registration, and password helpers
    ├── customer.py         # Customer class (save to DB)
    ├── account.py          # Account class (deposit, withdraw)
    ├── transaction.py      # Transaction read/write helpers
    ├── bank.py             # Bank-level operations
    └── database.py         # MySQL connection helper
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web Framework | Streamlit 1.62.0 |
| Database | MySQL (via mysql-connector-python) |
| Data Processing | Pandas |
| Password Hashing | bcrypt |
| Styling | Custom CSS (dark glassmorphism, gradients, animations) |
| Fonts | Inter (Google Fonts) |

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- MySQL server running locally (or remotely)
- `pip` package manager

### 2. Set Up the Database

Run the following SQL in your MySQL client to create the database and tables:

```sql
CREATE DATABASE IF NOT EXISTS bank_management_system;
USE bank_management_system;

-- Customers table
CREATE TABLE IF NOT EXISTS customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    phone       VARCHAR(20),
    is_active   TINYINT NOT NULL DEFAULT 1
);

-- Accounts table
CREATE TABLE IF NOT EXISTS account (
    account_no   INT AUTO_INCREMENT PRIMARY KEY,
    customer_id  INT NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    balance      DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    is_active    TINYINT NOT NULL DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

-- Transaction history table
CREATE TABLE IF NOT EXISTS transaction_history (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    account_no       INT NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    amount           DECIMAL(15,2) NOT NULL,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Users table (for login)
CREATE TABLE IF NOT EXISTS users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(150) UNIQUE NOT NULL,
    email         VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('ADMIN', 'CUSTOMER') NOT NULL DEFAULT 'CUSTOMER',
    is_active     TINYINT NOT NULL DEFAULT 1
);

-- Create your first admin user (change the password after first login)
INSERT INTO users (username, email, password_hash, role, is_active)
VALUES ('admin', 'admin@bankpro.com', '1234', 'ADMIN', 1);
```

> **Note:** The app automatically adds `is_active` columns to `customer` and `account` tables at startup if they are missing (safe migration).

### 3. Configure the .env File

Create a `.env` file in the project root with your MySQL connection details:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=bank_management_system
```

### 4. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the App

```bash
streamlit run app.py
```

Then open your browser at: **http://localhost:8501**

---

## 🔐 Login Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| Admin | `admin` | `1234` | Created manually in the DB setup step |
| Customer (admin-created) | their email address | `1234` | Default password — customer should change it |
| Customer (self-registered) | their email address | password they chose | Set during registration |

---

## 📖 Usage Guide

### For Admin

Use the **sidebar** to navigate between pages:

| Page | What You Can Do |
|---|---|
| 🏠 Dashboard | See live stats and all active accounts |
| 👤 Create Customer | Register a new customer (auto-creates login with password `1234`) |
| 👥 Manage Customers | Edit customer details or deactivate a customer |
| 🏧 Create Account | Open an account for any active customer |
| 🏦 Manage Accounts | Edit account type/balance or deactivate an account |
| 💰 Deposit | Deposit money into any active account |
| 💸 Withdraw | Withdraw from any active account |
| 🔄 Transfer Money | Transfer funds between any two active accounts |
| 📊 Display Balance | View balance and customer info for any account |
| 🧾 Transaction History | See all transactions across all accounts |

### For Customer

Customers only see their own data:

| Page | What You Can Do |
|---|---|
| 🏠 Dashboard | See your own accounts and total balance |
| 🏧 Create Account | Open a new account linked to your profile |
| 💰 Deposit | Deposit into your own accounts |
| 💸 Withdraw | Withdraw from your own accounts |
| 🔄 Transfer Money | Transfer between your own accounts |
| 📊 Display Balance | View your account balance and personal details |
| 🧾 Transaction History | See your own transactions |

### Self-Registration

New customers can register directly from the login page:
1. Click the **Register** tab on the login screen.
2. Fill in your name, email, phone, and choose a password.
3. After registration, sign in using your **email** as the username.

### Soft Delete (Deactivate)

When a customer is deactivated:
- Their record is **not deleted** from the database — `is_active` is set to `0`.
- All their accounts are also deactivated (`is_active = 0`).
- Their login is blocked.
- Inactive rows are shown with a **light red background** in the admin manage pages.

When an account is deactivated:
- The account is excluded from all transactions (deposit, withdraw, transfer).
- It is shown with a **light red background** on the Manage Accounts page.

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add: description"`
4. Push and open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

> ⭐ If you found this project helpful, consider giving it a star!
