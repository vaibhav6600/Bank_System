# 🏦 Bank Management System

A full-featured **Bank Management System** built with Python and a modern **Streamlit** web interface. Manage customers, accounts, deposits, withdrawals, transfers, and transaction history — all from a clean browser-based dashboard.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Usage Guide](#usage-guide)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Bank Management System provides two ways to interact with banking operations:

| Mode | File | Description |
|---|---|---|
| **Web UI** | `app.py` | Streamlit-powered browser dashboard |
| **CLI** | `main.py` | Terminal-based interactive menu |

All core banking logic lives in the `bank/` package and is shared between both interfaces.

---

## ✨ Features

- **Customer Management** — Create and store customer profiles (ID, name, email, phone)
- **Account Management** — Open bank accounts linked to customers with an initial deposit
- **Deposit** — Add funds to any account with instant balance update
- **Withdraw** — Withdraw funds with insufficient-balance protection
- **Transfer Money** — Move funds between two accounts safely
- **Display Balance** — View detailed account and customer information at a glance
- **Transaction History** — Full audit log of every deposit, withdrawal, and transfer
- **Live Dashboard** — Real-time stats: total customers, total accounts, total bank balance
- **Dark Glassmorphism UI** — Premium dark-mode design with smooth animations

---

## 📁 Project Structure

```
PythonProject/
│
├── app.py                  # Streamlit web application (main entry point)
├── main.py                 # CLI-based interface
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── bank/                   # Core banking logic package
│   ├── __init__.py
│   ├── customer.py         # Customer class
│   ├── account.py          # Account class (deposit, withdraw)
│   ├── bank.py             # Bank-level operations (extendable)
│   └── transaction.py      # Transaction model (extendable)
│
├── tests/                  # Unit tests
└── utils/                  # Utility helpers
```

---

## 🛠 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.14.6 |
| Web Framework | Streamlit | 1.62.0 |
| Data Processing | Pandas | 3.0.5 |
| Styling | CSS (Glassmorphism, Gradients) | — |
| Font | Inter (Google Fonts) | — |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed on your machine:

- [Python 3.10+](https://www.python.org/downloads/)
- `pip` (comes bundled with Python)
- A terminal or PowerShell

---

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/bank-management-system.git
cd bank-management-system
```

**2. Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is out of date, install manually:
> ```bash
> pip install streamlit pandas
> ```

---

### Running the App

#### ▶ Web UI (Recommended)

```bash
streamlit run app.py
```

Then open your browser and go to: **http://localhost:8501**

#### ▶ CLI Mode

```bash
python main.py
```

Follow the on-screen menu to perform banking operations in the terminal.

---

## 📖 Usage Guide

Once the Streamlit app is open, use the **sidebar** to navigate:

| Page | What You Can Do |
|---|---|
| 🏠 Dashboard | See live stats and a full accounts overview |
| 👤 Create Customer | Register a new customer with ID, name, email, and phone |
| 🏧 Create Account | Link an account to a customer and set an opening balance |
| 💰 Deposit | Select an account and deposit an amount |
| 💸 Withdraw | Withdraw from an account (balance-protected) |
| 🔄 Transfer Money | Transfer funds between two accounts |
| 📊 Display Balance | View account balance and full customer details |
| 🧾 Transaction History | See every transaction with summary totals |

> **Note:** All data is stored in the current session. Refreshing the browser will reset the state. For persistence, integrate a database (e.g., SQLite, PostgreSQL).

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repository
2. **Create** a new branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "Add: your feature description"`
4. **Push** to the branch: `git push origin feature/your-feature-name`
5. **Open** a Pull Request

Please make sure your code follows the existing style and includes relevant tests.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.

---

## 👤 Author

Built with ❤️ using Python & Streamlit.

---

> ⭐ If you found this project helpful, please consider giving it a star!
