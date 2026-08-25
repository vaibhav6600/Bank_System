import sys
sys.path.append(r"C:\Users\Admin\PycharmProjects\PythonProject")

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from bank.customer import Customer
from bank.account import Account
from bank.database import get_connection
from bank.transaction import save_transaction, get_transactions
from bank.auth import create_customer_with_default_user

# ══════════════════════════════════════════════════════════
#  PAGE CONFIG  – must be the FIRST Streamlit call
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="BankPro – Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
#  AUTH GATE  – show login page until authenticated
# ══════════════════════════════════════════════════════════
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    from login import render_login
    render_login()          # calls st.stop() internally


# ══════════════════════════════════════════════════════════
#  GLOBAL CSS  –  Classic Professional Banking Theme
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ══════════════════════════════════════════
   COLOR PALETTE
   Background : #0d1117  (deep charcoal)
   Sidebar    : #0a0f1e  (midnight navy)
   Accent     : #00c9a7  (vivid teal/emerald)
   Accent2    : #845ef7  (soft violet)
   Gold       : #ffd43b  (warm gold)
   Surface    : #161b2e  (dark card)
   Border     : rgba(0,201,167,0.18)
   Text       : #e2e8f0  (soft white)
   Muted      : #8892a4  (slate grey)
══════════════════════════════════════════ */

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App canvas ── */
.stApp {
    background: radial-gradient(ellipse at top left, #0d1f3c 0%, #0a0f1e 50%, #050810 100%);
    color: #e2e8f0;
    min-height: 100vh;
}

/* ── Hide default Streamlit top decoration ── */
header[data-testid="stHeader"] {
    background: transparent !important;
    box-shadow: none !important;
}

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #0d1635 100%) !important;
    border-right: 1px solid rgba(0,201,167,0.12) !important;
}
section[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}
/* Force all sidebar text to inherit theme color */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: #c8d6e5 !important;
}

/* ── Sidebar nav buttons ── */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #8892a4 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    text-align: left !important;
    justify-content: flex-start !important;
    letter-spacing: 0.2px !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    margin: 2px 0 !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,201,167,0.10) !important;
    color: #00c9a7 !important;
    transform: translateX(4px) !important;
    box-shadow: none !important;
}

/* ── Logout button in sidebar ── */
.logout-btn > button {
    background: rgba(255,87,87,0.10) !important;
    color: #ff5757 !important;
    border: 1px solid rgba(255,87,87,0.25) !important;
    border-radius: 10px !important;
    padding: 9px 16px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}
.logout-btn > button:hover {
    background: rgba(255,87,87,0.22) !important;
    border-color: #ff5757 !important;
    transform: none !important;
}

/* ── Sidebar stat pills ── */
.stat-pill {
    background: rgba(0,201,167,0.07);
    border: 1px solid rgba(0,201,167,0.15);
    border-radius: 12px;
    padding: 11px 16px;
    margin: 5px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.2s;
}
.stat-pill:hover { background: rgba(0,201,167,0.13); }
.stat-pill .stat-label { font-size: 0.81rem; color: #8892a4 !important; font-weight: 500; }
.stat-pill .stat-value { font-size: 0.97rem; font-weight: 800; color: #00c9a7 !important; }

/* ── Sidebar section label ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #8892a4 !important;
    padding: 16px 18px 6px;
}

/* ── Sidebar divider ── */
.sidebar-divider {
    height: 1px;
    background: rgba(0,201,167,0.12);
    margin: 8px 18px;
}

/* ══════════════════════════════════════════
   PAGE HEADER BANNER
══════════════════════════════════════════ */
.page-header {
    background: linear-gradient(135deg, #00c9a7 0%, #0096c7 40%, #845ef7 100%);
    color: white;
    padding: 24px 36px;
    border-radius: 18px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 8px 32px rgba(0,201,167,0.25), 0 2px 8px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -50px; right: 80px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.page-header .icon {
    font-size: 2.6rem;
    line-height: 1;
    filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));
    z-index: 1;
}
.page-header .title {
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    z-index: 1;
}
.page-header .subtitle {
    font-size: 0.87rem;
    opacity: 0.85;
    margin-top: 3px;
    z-index: 1;
}
.page-header .user-badge {
    margin-left: auto;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.82rem;
    font-weight: 600;
    z-index: 1;
    white-space: nowrap;
}

/* ══════════════════════════════════════════
   METRIC CARDS
══════════════════════════════════════════ */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #161b2e 0%, #1a2035 100%);
    border: 1px solid rgba(0,201,167,0.18);
    border-radius: 16px;
    padding: 22px 26px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s;
    position: relative;
    overflow: hidden;
}
div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #00c9a7, #845ef7);
    border-radius: 16px 0 0 16px;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    border-color: rgba(0,201,167,0.38);
    box-shadow: 0 12px 36px rgba(0,201,167,0.15), 0 4px 12px rgba(0,0,0,0.4);
}
div[data-testid="metric-container"] label {
    color: #8892a4 !important;
    font-weight: 600;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #ffd43b !important;
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}

/* ══════════════════════════════════════════
   BUTTONS  (main content area)
══════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #00c9a7 0%, #0096c7 100%);
    color: #0a0f1e !important;
    border: none;
    border-radius: 12px;
    padding: 12px 32px;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
    transition: all 0.22s ease;
    box-shadow: 0 4px 16px rgba(0,201,167,0.35);
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(0,201,167,0.5);
    filter: brightness(1.06);
}
.stButton > button:active {
    transform: translateY(-1px);
}

/* ══════════════════════════════════════════
   FORMS & INPUTS
══════════════════════════════════════════ */
div[data-testid="stForm"] {
    background: linear-gradient(135deg, #161b2e 0%, #1a2035 100%);
    border: 1px solid rgba(0,201,167,0.15);
    border-radius: 18px;
    padding: 28px 32px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}
div[data-testid="stForm"] h4 {
    color: #e2e8f0 !important;
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(0,201,167,0.12);
}
input, textarea {
    background: #0d1117 !important;
    border: 1.5px solid rgba(0,201,167,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.94rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input:focus, textarea:focus {
    border-color: #00c9a7 !important;
    box-shadow: 0 0 0 3px rgba(0,201,167,0.15) !important;
}
/* Selectbox */
div[data-baseweb="select"] > div {
    background: #0d1117 !important;
    border: 1.5px solid rgba(0,201,167,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #00c9a7 !important;
    box-shadow: 0 0 0 3px rgba(0,201,167,0.15) !important;
}
/* Selectbox dropdown option list */
div[data-baseweb="popover"] {
    background: #161b2e !important;
    border: 1px solid rgba(0,201,167,0.2) !important;
    border-radius: 12px !important;
}
/* Input labels */
label[data-testid="stWidgetLabel"] p {
    color: #8892a4 !important;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.3px;
}

/* ══════════════════════════════════════════
   ALERTS
══════════════════════════════════════════ */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-weight: 500 !important;
    font-size: 0.93rem !important;
}
/* Success */
div[data-testid="stAlert"][data-baseweb="notification"][kind="positive"] {
    background: rgba(0,201,167,0.12) !important;
    border-left: 4px solid #00c9a7 !important;
    color: #a8ffef !important;
}
/* Error */
div[data-testid="stAlert"][data-baseweb="notification"][kind="negative"] {
    background: rgba(255,87,87,0.10) !important;
    border-left: 4px solid #ff5757 !important;
}
/* Warning */
div[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
    background: rgba(255,212,59,0.10) !important;
    border-left: 4px solid #ffd43b !important;
}

/* ══════════════════════════════════════════
   DATAFRAMES / TABLES
══════════════════════════════════════════ */
.stDataFrame {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid rgba(0,201,167,0.14) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25) !important;
}
div[data-testid="stDataFrame"] > div {
    background: #161b2e !important;
}

/* ══════════════════════════════════════════
   DETAIL CARDS  (Display Balance page)
══════════════════════════════════════════ */
.detail-card {
    background: linear-gradient(135deg, #161b2e 0%, #1a2035 100%);
    border: 1px solid rgba(0,201,167,0.18);
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.detail-card p {
    margin: 10px 0;
    font-size: 0.95rem;
    color: #c8d6e5 !important;
    line-height: 1.6;
}
.detail-card b { color: #00c9a7 !important; font-weight: 600; }

/* ══════════════════════════════════════════
   CARD (generic white surface override)
══════════════════════════════════════════ */
.card {
    background: linear-gradient(135deg, #161b2e 0%, #1a2035 100%);
    border: 1px solid rgba(0,201,167,0.15);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

/* ══════════════════════════════════════════
   MANAGE TABLE  (inactive rows = light red)
══════════════════════════════════════════ */
.manage-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}
.manage-table th {
    background: rgba(0,201,167,0.12);
    color: #00c9a7;
    font-weight: 700;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 2px solid rgba(0,201,167,0.2);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.manage-table td {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: #c8d6e5;
}
.manage-table tr.active-row {
    background: rgba(22,27,46,0.8);
}
.manage-table tr.active-row:hover {
    background: rgba(0,201,167,0.05);
}
.manage-table tr.inactive-row {
    background: rgba(255, 80, 80, 0.10);
}
.manage-table tr.inactive-row td {
    color: #f0a0a0;
}
.inactive-badge {
    background: rgba(255,80,80,0.2);
    color: #ff7070;
    border: 1px solid rgba(255,80,80,0.35);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-weight: 700;
}
.active-badge {
    background: rgba(0,201,167,0.15);
    color: #00c9a7;
    border: 1px solid rgba(0,201,167,0.3);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-weight: 700;
}

/* ══════════════════════════════════════════
   MARKDOWN  –  headings, hr, text
══════════════════════════════════════════ */
h1, h2, h3, h4, h5 { color: #e2e8f0 !important; }
h4 { color: #b0bec5 !important; font-weight: 700; }
hr {
    border: none;
    border-top: 1px solid rgba(0,201,167,0.15);
    margin: 20px 0;
}
p { color: #c8d6e5; }

/* ══════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb {
    background: rgba(0,201,167,0.35);
    border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover { background: #00c9a7; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  ROLE & USER INFO from session state
# ══════════════════════════════════════════════════════════
_role        = st.session_state.get("role", "CUSTOMER")   # 'ADMIN' or 'CUSTOMER'
_customer_id = st.session_state.get("customer_id")         # int or None
_username    = st.session_state.get("display_name", "User")
_is_admin    = (_role == "ADMIN")


# ══════════════════════════════════════════════════════════
#  ENSURE is_active COLUMNS EXIST IN DB
# ══════════════════════════════════════════════════════════
def db_ensure_columns():
    """
    Safely add is_active column to customer and account tables if missing,
    then back-fill any NULL values to 1 (rows inserted before the column existed).
    Runs once per session.
    """
    if st.session_state.get("_columns_checked"):
        return
    try:
        conn = get_connection()
        cur  = conn.cursor()

        # ── customer.is_active ──
        cur.execute("""
            SELECT COUNT(*) FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name   = 'customer'
              AND column_name  = 'is_active'
        """)
        if cur.fetchone()[0] == 0:
            cur.execute("ALTER TABLE customer ADD COLUMN is_active TINYINT DEFAULT 1")
        # Back-fill NULLs → 1  (existing rows inserted before the column was added)
        cur.execute("UPDATE customer SET is_active = 1 WHERE is_active IS NULL")
        conn.commit()

        # ── account.is_active ──
        cur.execute("""
            SELECT COUNT(*) FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name   = 'account'
              AND column_name  = 'is_active'
        """)
        if cur.fetchone()[0] == 0:
            cur.execute("ALTER TABLE account ADD COLUMN is_active TINYINT DEFAULT 1")
        # Back-fill NULLs → 1
        cur.execute("UPDATE account SET is_active = 1 WHERE is_active IS NULL")
        conn.commit()

        cur.close(); conn.close()
        st.session_state["_columns_checked"] = True
    except Exception as e:
        st.warning(f"DB migration warning: {e}")


db_ensure_columns()


# ══════════════════════════════════════════════════════════
#  DB HELPER FUNCTIONS  –  all data comes from MySQL
# ══════════════════════════════════════════════════════════

def db_get_stats():
    """Return (n_customers, n_accounts, total_balance) – ADMIN only. Counts only active rows."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customer WHERE COALESCE(is_active, 1) = 1")
        n_cust = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*), COALESCE(SUM(balance),0) FROM account WHERE COALESCE(is_active, 1) = 1")
        row = cur.fetchone()
        n_acc, total_bal = row[0], float(row[1])
        cur.close(); conn.close()
        return n_cust, n_acc, total_bal
    except Exception:
        return 0, 0, 0.0


def db_get_my_stats(customer_id):
    """Return (n_accounts, total_balance) for a single customer (active accounts only)."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "SELECT COUNT(*), COALESCE(SUM(balance),0) FROM account WHERE customer_id = %s AND COALESCE(is_active, 1) = 1",
            (customer_id,)
        )
        row = cur.fetchone()
        n_acc, total_bal = row[0], float(row[1])
        cur.close(); conn.close()
        return n_acc, total_bal
    except Exception:
        return 0, 0.0


def db_get_customers(active_only=True):
    """
    Return list of dicts from customer table.
    active_only=True  → only COALESCE(is_active,1)=1 rows (used for dropdowns, forms)
    active_only=False → all rows (used for Manage Customers admin page)
    """
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        if active_only:
            cur.execute("SELECT * FROM customer WHERE COALESCE(is_active, 1) = 1 ORDER BY customer_id DESC")
        else:
            cur.execute("SELECT * FROM customer ORDER BY customer_id DESC")
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception:
        return []


def db_get_accounts(customer_id=None, active_only=True):
    """
    Return list of dicts from account table joined with customer name.
    active_only=True  → only COALESCE(is_active,1)=1 rows (used for transactions, balance)
    active_only=False → all rows (used for Manage Accounts admin page)
    If customer_id is given, filter to that customer only.
    """
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        if customer_id is not None:
            where = "WHERE a.customer_id = %s" + (" AND COALESCE(a.is_active, 1) = 1" if active_only else "")
            cur.execute(f"""
                SELECT a.account_no, a.customer_id, c.name AS customer_name,
                       a.account_type, a.balance,
                       COALESCE(a.is_active, 1) AS is_active
                FROM account a
                LEFT JOIN customer c ON a.customer_id = c.customer_id
                {where}
                ORDER BY a.account_no DESC
            """, (customer_id,))
        else:
            where = ("WHERE COALESCE(a.is_active, 1) = 1" if active_only else "")
            cur.execute(f"""
                SELECT a.account_no, a.customer_id, c.name AS customer_name,
                       a.account_type, a.balance,
                       COALESCE(a.is_active, 1) AS is_active
                FROM account a
                LEFT JOIN customer c ON a.customer_id = c.customer_id
                {where}
                ORDER BY a.account_no DESC
            """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception:
        return []


def db_get_account_balance(account_no):
    """Fetch current balance for an account from DB."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT balance FROM account WHERE account_no = %s", (account_no,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return float(row[0]) if row else 0.0
    except Exception:
        return 0.0


def db_update_customer(customer_id, name, email, phone):
    """Update customer name, email, phone. Returns (ok, msg)."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "UPDATE customer SET name=%s, email=%s, phone=%s WHERE customer_id=%s",
            (name, email, phone, customer_id)
        )
        conn.commit()
        cur.close(); conn.close()
        return True, "Updated."
    except Exception as e:
        return False, str(e)


def db_delete_customer(customer_id):
    """
    Soft-delete a customer:
    - Sets customer.is_active = 0
    - Sets account.is_active = 0 for all that customer's accounts
    - Sets users.is_active = 0 for the linked user (matched by email)
    Returns (ok, msg).
    """
    try:
        conn = get_connection()
        cur  = conn.cursor()
        # Get customer email to find their user record
        cur.execute("SELECT email FROM customer WHERE customer_id = %s", (customer_id,))
        row = cur.fetchone()
        if row:
            email = row[0]
            cur.execute("UPDATE users SET is_active = 0 WHERE email = %s", (email,))
        # Deactivate all accounts for this customer
        cur.execute("UPDATE account SET is_active = 0 WHERE customer_id = %s", (customer_id,))
        # Deactivate the customer
        cur.execute("UPDATE customer SET is_active = 0 WHERE customer_id = %s", (customer_id,))
        conn.commit()
        cur.close(); conn.close()
        return True, "Customer deactivated."
    except Exception as e:
        return False, str(e)


def db_update_account(account_no, account_type, balance):
    """Update account type and balance. Returns (ok, msg)."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "UPDATE account SET account_type=%s, balance=%s WHERE account_no=%s",
            (account_type, balance, account_no)
        )
        conn.commit()
        cur.close(); conn.close()
        return True, "Updated."
    except Exception as e:
        return False, str(e)


def db_delete_account(account_no):
    """
    Soft-delete an account: sets account.is_active = 0.
    Returns (ok, msg).
    """
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("UPDATE account SET is_active = 0 WHERE account_no = %s", (account_no,))
        conn.commit()
        cur.close(); conn.close()
        return True, "Account deactivated."
    except Exception as e:
        return False, str(e)


# ══════════════════════════════════════════════════════════
#  SESSION STATE  –  navigation
# ══════════════════════════════════════════════════════════

# Page lists per role
ADMIN_PAGES = [
    ("🏠", "Dashboard"),
    ("👤", "Create Customer"),
    ("👥", "Manage Customers"),
    ("🏧", "Create Account"),
    ("🏦", "Manage Accounts"),
    ("💰", "Deposit"),
    ("💸", "Withdraw"),
    ("🔄", "Transfer Money"),
    ("📊", "Display Balance"),
    ("🧾", "Transaction History"),
]

CUSTOMER_PAGES = [
    ("🏠", "Dashboard"),
    ("🏧", "Create Account"),
    ("💰", "Deposit"),
    ("💸", "Withdraw"),
    ("🔄", "Transfer Money"),
    ("📊", "Display Balance"),
    ("🧾", "Transaction History"),
]

PAGES = ADMIN_PAGES if _is_admin else CUSTOMER_PAGES

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Make sure the current page is valid for this role
_valid_page_names = [label for _, label in PAGES]
if st.session_state.page not in _valid_page_names:
    st.session_state.page = "Dashboard"


# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    # ── Brand ──
    st.markdown(f"""
    <div style="padding:20px 18px 10px;">
        <div style="font-size:2rem;">🏦</div>
        <div style="font-size:1.15rem;font-weight:800;color:#ffffff;margin-top:4px;">BankPro</div>
        <div style="font-size:0.78rem;color:#9fa8da;margin-top:2px;">Management System</div>
    </div>
    <div style="background:rgba(0,201,167,0.12);border-radius:10px;padding:8px 14px;margin:4px 10px 10px;">
        <span style="font-size:0.75rem;color:#8892a4;">Signed in as</span><br>
        <span style="font-size:0.9rem;font-weight:700;color:#00c9a7;">{'👑 ' if _is_admin else '👤 '}{_username}</span>
        <span style="font-size:0.7rem;color:#5d7a8a;margin-left:6px;">{'ADMIN' if _is_admin else 'CUSTOMER'}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:4px 18px 10px;"></div>', unsafe_allow_html=True)

    # ── Navigation buttons ──
    st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)
    for icon, label in PAGES:
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:14px 18px 10px;"></div>', unsafe_allow_html=True)

    # ── Live stats from DB (role-filtered) ──
    st.markdown('<div class="section-label">Live Stats</div>', unsafe_allow_html=True)

    if _is_admin:
        n_cust, n_acc, total_bal = db_get_stats()
        st.markdown(f"""
        <div class="stat-pill">
            <span class="stat-label">👤 Customers</span>
            <span class="stat-value">{n_cust}</span>
        </div>
        <div class="stat-pill">
            <span class="stat-label">🏧 Accounts</span>
            <span class="stat-value">{n_acc}</span>
        </div>
        <div class="stat-pill">
            <span class="stat-label">💰 Total Balance</span>
            <span class="stat-value">₹{total_bal:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Customer: show only their own accounts + balance
        n_acc, total_bal = db_get_my_stats(_customer_id)
        st.markdown(f"""
        <div class="stat-pill">
            <span class="stat-label">🏧 My Accounts</span>
            <span class="stat-value">{n_acc}</span>
        </div>
        <div class="stat-pill">
            <span class="stat-label">💰 My Balance</span>
            <span class="stat-value">₹{total_bal:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:14px 18px 10px;"></div>', unsafe_allow_html=True)

    # ── Logout button ──
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪  Logout", key="logout_btn", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE HEADER  –  always rendered at the top of the page
# ══════════════════════════════════════════════════════════
PAGE_META = {
    "Dashboard":           ("🏠", "Dashboard",           "Overview of your banking operations"),
    "Create Customer":     ("👤", "Create Customer",     "Register a new customer in the system"),
    "Manage Customers":    ("👥", "Manage Customers",    "Edit or deactivate existing customers"),
    "Create Account":      ("🏧", "Create Account",      "Open a new bank account"),
    "Manage Accounts":     ("🏦", "Manage Accounts",     "Edit or deactivate existing accounts"),
    "Deposit":             ("💰", "Deposit Money",        "Add funds to an account"),
    "Withdraw":            ("💸", "Withdraw Money",       "Withdraw funds from an account"),
    "Transfer Money":      ("🔄", "Transfer Money",       "Move funds between two accounts"),
    "Display Balance":     ("📊", "Account Balance",      "View detailed balance and account info"),
    "Transaction History": ("🧾", "Transaction History", "Audit log of all transactions"),
}

page = st.session_state.page
icon, title, subtitle = PAGE_META[page]

# Role badge in header
_badge_color = "#ffd43b" if _is_admin else "#00c9a7"
_badge_label = "👑 Admin" if _is_admin else "👤 Customer"

st.markdown(f"""
<div class="page-header">
    <div class="icon">{icon}</div>
    <div>
        <div class="title">{title}</div>
        <div class="subtitle">{subtitle}</div>
    </div>
    <div class="user-badge" style="border-color:rgba(255,255,255,0.3);color:#fff;">
        {_badge_label}: {_username}
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE : Dashboard
# ══════════════════════════════════════════════════════════
if page == "Dashboard":
    if _is_admin:
        # Admin sees global aggregates (active only)
        n_cust, n_acc, total_bal = db_get_stats()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Customers",    n_cust)
        col2.metric("Total Accounts",     n_acc)
        col3.metric("Total Bank Balance", f"₹{total_bal:,.2f}")

        st.markdown("---")

        accounts_data = db_get_accounts(active_only=True)
        if accounts_data:
            st.markdown("### All Active Accounts")
            df = pd.DataFrame(accounts_data)
            df = df.drop(columns=["is_active"], errors="ignore")
            df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No active accounts yet. Create a customer and account to get started.")
    else:
        # Customer sees only their own data
        n_acc, total_bal = db_get_my_stats(_customer_id)
        col1, col2 = st.columns(2)
        col1.metric("My Accounts", n_acc)
        col2.metric("My Total Balance", f"₹{total_bal:,.2f}")

        st.markdown("---")

        accounts_data = db_get_accounts(customer_id=_customer_id, active_only=True)
        if accounts_data:
            st.markdown("### My Accounts")
            df = pd.DataFrame(accounts_data)
            df = df.drop(columns=["is_active"], errors="ignore")
            df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("You have no active accounts yet.")


# ══════════════════════════════════════════════════════════
#  PAGE : Create Customer  (ADMIN ONLY)
# ══════════════════════════════════════════════════════════
elif page == "Create Customer":
    if not _is_admin:
        st.error("🚫 Access denied. This page is for administrators only.")
        st.stop()

    with st.form("form_create_customer", clear_on_submit=True):
        st.markdown("#### Customer Details")
        col1, col2 = st.columns(2)
        with col1:
            name  = st.text_input("Full Name",   placeholder="e.g. Rahul Sharma")
            email = st.text_input("Email",        placeholder="e.g. rahul@example.com")
        with col2:
            phone = st.text_input("Phone Number", placeholder="e.g. 9876543210")
        submitted = st.form_submit_button("➕  Create Customer", use_container_width=True)

    if submitted:
        if not all([name, email, phone]):
            st.error("All fields are required.")
        else:
            # Use the helper that also creates a users row with default password "1234"
            ok, msg = create_customer_with_default_user(name.strip(), email.strip(), phone.strip())
            if ok:
                st.success(
                    f"✅ Customer **{name}** created successfully! "
                    f"Login username: **{email.strip()}** · Default password: **1234**"
                )
                st.rerun()
            else:
                st.error(f"Error: {msg}")

    st.markdown("---")
    st.markdown("#### Existing Customers")
    custs = db_get_customers(active_only=False)
    if custs:
        df = pd.DataFrame(custs)
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No customers found.")


# ══════════════════════════════════════════════════════════
#  PAGE : Manage Customers  (ADMIN ONLY)
# ══════════════════════════════════════════════════════════
elif page == "Manage Customers":
    if not _is_admin:
        st.error("🚫 Access denied. This page is for administrators only.")
        st.stop()

    st.markdown("#### All Customers")
    st.markdown(
        "<p style='font-size:0.85rem;color:#8892a4;'>"
        "🔴 Rows highlighted in red are <b>inactive</b> customers. "
        "Inactive customers cannot log in. Their accounts are also deactivated."
        "</p>",
        unsafe_allow_html=True
    )

    custs = db_get_customers(active_only=False)
    if not custs:
        st.info("No customers found.")
    else:
        # Render styled HTML table
        rows_html = ""
        for c in custs:
            row_class = "active-row" if c.get("is_active", 1) else "inactive-row"
            status_badge = (
                '<span class="active-badge">Active</span>'
                if c.get("is_active", 1)
                else '<span class="inactive-badge">Inactive</span>'
            )
            rows_html += f"""
            <tr class="{row_class}">
                <td>{c['customer_id']}</td>
                <td>{c['name']}</td>
                <td>{c['email']}</td>
                <td>{c.get('phone', '')}</td>
                <td>{status_badge}</td>
            </tr>"""

        st.markdown(f"""
        <table class="manage-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Edit or Deactivate a Customer")

        # Selectbox: only show active customers for actions
        active_custs = [c for c in custs if c.get("is_active", 1)]
        if not active_custs:
            st.info("No active customers to manage.")
        else:
            cust_labels = {f"{c['customer_id']} – {c['name']}": c for c in active_custs}
            selected_label = st.selectbox("Select Customer", list(cust_labels.keys()), key="manage_cust_select")
            sel_cust = cust_labels[selected_label]

            tab_edit, tab_delete = st.tabs(["✏️  Edit Details", "🗑️  Deactivate Customer"])

            with tab_edit:
                with st.form("form_edit_customer", clear_on_submit=False):
                    st.markdown("#### Update Customer Details")
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name  = st.text_input("Full Name",   value=sel_cust["name"],  key="edit_cust_name")
                        new_email = st.text_input("Email",        value=sel_cust["email"], key="edit_cust_email")
                    with col2:
                        new_phone = st.text_input("Phone Number", value=sel_cust.get("phone", ""), key="edit_cust_phone")
                    upd_submit = st.form_submit_button("💾  Save Changes", use_container_width=True)

                if upd_submit:
                    if not all([new_name, new_email, new_phone]):
                        st.error("All fields are required.")
                    else:
                        ok, msg = db_update_customer(sel_cust["customer_id"], new_name.strip(), new_email.strip(), new_phone.strip())
                        if ok:
                            st.success("✅ Customer updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error: {msg}")

            with tab_delete:
                st.warning(
                    f"⚠️ Deactivating **{sel_cust['name']}** will also deactivate all their accounts "
                    f"and block their login. This action does NOT permanently delete any data."
                )
                col_confirm, col_btn = st.columns([3, 1])
                with col_confirm:
                    confirm_text = st.text_input(
                        f"Type the customer name **{sel_cust['name']}** to confirm",
                        key="delete_cust_confirm"
                    )
                with col_btn:
                    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
                    if st.button("🗑️  Deactivate", key="btn_delete_cust"):
                        if confirm_text.strip() == sel_cust["name"]:
                            ok, msg = db_delete_customer(sel_cust["customer_id"])
                            if ok:
                                st.success(f"✅ Customer **{sel_cust['name']}** has been deactivated.")
                                st.rerun()
                            else:
                                st.error(f"Error: {msg}")
                        else:
                            st.error("Name does not match. Deactivation cancelled.")


# ══════════════════════════════════════════════════════════
#  PAGE : Create Account
# ══════════════════════════════════════════════════════════
elif page == "Create Account":
    if _is_admin:
        # Admin can create account for any active customer
        custs = db_get_customers(active_only=True)
        if not custs:
            st.warning("No active customers found. Please create a customer first.")
        else:
            cust_map = {f"{c['customer_id']} – {c['name']}": c['customer_id'] for c in custs}
            with st.form("form_create_account", clear_on_submit=True):
                st.markdown("#### Account Details")
                col1, col2 = st.columns(2)
                with col1:
                    selected_label = st.selectbox("Select Customer", list(cust_map.keys()))
                    acc_type = st.selectbox("Account Type", ["Savings", "Current", "Fixed Deposit"])
                with col2:
                    balance = st.number_input("Initial Deposit (₹)", min_value=0.0, step=100.0, format="%.2f")
                submitted = st.form_submit_button("➕  Create Account", use_container_width=True)

            if submitted:
                cust_id = cust_map[selected_label]
                try:
                    a = Account(None, cust_id, acc_type, balance)
                    a.save()
                    st.success(f"✅ Account created with ₹{balance:,.2f} initial deposit!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

            st.markdown("---")
            st.markdown("#### Existing Active Accounts")
            accs = db_get_accounts(active_only=True)
            if accs:
                df = pd.DataFrame(accs)
                df = df.drop(columns=["is_active"], errors="ignore")
                df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
                df.columns = [c.replace("_", " ").title() for c in df.columns]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No active accounts yet.")
    else:
        # Customer can only create account for themselves
        if _customer_id is None:
            st.warning("Your user account is not linked to a customer profile. Please contact an administrator.")
        else:
            with st.form("form_create_account_cust", clear_on_submit=True):
                st.markdown("#### New Account")
                acc_type = st.selectbox("Account Type", ["Savings", "Current", "Fixed Deposit"])
                balance  = st.number_input("Initial Deposit (₹)", min_value=0.0, step=100.0, format="%.2f")
                submitted = st.form_submit_button("➕  Create Account", use_container_width=True)

            if submitted:
                try:
                    a = Account(None, _customer_id, acc_type, balance)
                    a.save()
                    st.success(f"✅ Account created with ₹{balance:,.2f} initial deposit!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

            st.markdown("---")
            st.markdown("#### My Accounts")
            accs = db_get_accounts(customer_id=_customer_id, active_only=True)
            if accs:
                df = pd.DataFrame(accs)
                df = df.drop(columns=["is_active"], errors="ignore")
                df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
                df.columns = [c.replace("_", " ").title() for c in df.columns]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No accounts yet.")


# ══════════════════════════════════════════════════════════
#  PAGE : Manage Accounts  (ADMIN ONLY)
# ══════════════════════════════════════════════════════════
elif page == "Manage Accounts":
    if not _is_admin:
        st.error("🚫 Access denied. This page is for administrators only.")
        st.stop()

    st.markdown("#### All Accounts")
    st.markdown(
        "<p style='font-size:0.85rem;color:#8892a4;'>"
        "🔴 Rows highlighted in red are <b>inactive</b> accounts. "
        "Inactive accounts are excluded from transactions."
        "</p>",
        unsafe_allow_html=True
    )

    all_accs = db_get_accounts(active_only=False)
    if not all_accs:
        st.info("No accounts found.")
    else:
        # Render styled HTML table
        rows_html = ""
        for a in all_accs:
            row_class = "active-row" if a.get("is_active", 1) else "inactive-row"
            status_badge = (
                '<span class="active-badge">Active</span>'
                if a.get("is_active", 1)
                else '<span class="inactive-badge">Inactive</span>'
            )
            rows_html += f"""
            <tr class="{row_class}">
                <td>{a['account_no']}</td>
                <td>{a.get('customer_name', '')}</td>
                <td>{a['account_type']}</td>
                <td>₹{float(a['balance']):,.2f}</td>
                <td>{status_badge}</td>
            </tr>"""

        st.markdown(f"""
        <table class="manage-table">
            <thead>
                <tr>
                    <th>Account No</th>
                    <th>Customer Name</th>
                    <th>Type</th>
                    <th>Balance</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Edit or Deactivate an Account")

        active_accs = [a for a in all_accs if a.get("is_active", 1)]
        if not active_accs:
            st.info("No active accounts to manage.")
        else:
            acc_labels = {
                f"{a['account_no']} – {a.get('customer_name', 'N/A')} ({a['account_type']})": a
                for a in active_accs
            }
            selected_acc_label = st.selectbox("Select Account", list(acc_labels.keys()), key="manage_acc_select")
            sel_acc = acc_labels[selected_acc_label]

            tab_edit_acc, tab_del_acc = st.tabs(["✏️  Edit Account", "🗑️  Deactivate Account"])

            with tab_edit_acc:
                with st.form("form_edit_account", clear_on_submit=False):
                    st.markdown("#### Update Account Details")
                    col1, col2 = st.columns(2)
                    with col1:
                        new_acc_type = st.selectbox(
                            "Account Type",
                            ["Savings", "Current", "Fixed Deposit"],
                            index=["Savings", "Current", "Fixed Deposit"].index(sel_acc["account_type"])
                            if sel_acc["account_type"] in ["Savings", "Current", "Fixed Deposit"] else 0,
                            key="edit_acc_type"
                        )
                    with col2:
                        new_balance = st.number_input(
                            "Balance (₹)", min_value=0.0,
                            value=float(sel_acc["balance"]),
                            step=100.0, format="%.2f",
                            key="edit_acc_balance"
                        )
                    acc_upd_submit = st.form_submit_button("💾  Save Changes", use_container_width=True)

                if acc_upd_submit:
                    ok, msg = db_update_account(sel_acc["account_no"], new_acc_type, new_balance)
                    if ok:
                        st.success("✅ Account updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error: {msg}")

            with tab_del_acc:
                st.warning(
                    f"⚠️ Deactivating account **{sel_acc['account_no']}** will exclude it from all transactions. "
                    f"This does NOT permanently delete any data."
                )
                if st.button("🗑️  Deactivate This Account", key="btn_delete_acc"):
                    ok, msg = db_delete_account(sel_acc["account_no"])
                    if ok:
                        st.success(f"✅ Account **{sel_acc['account_no']}** has been deactivated.")
                        st.rerun()
                    else:
                        st.error(f"Error: {msg}")


# ══════════════════════════════════════════════════════════
#  PAGE : Deposit
# ══════════════════════════════════════════════════════════
elif page == "Deposit":
    accs = db_get_accounts(customer_id=None if _is_admin else _customer_id, active_only=True)
    if not accs:
        st.warning("No active accounts found.")
    else:
        acc_map = {f"{a['account_no']} – {a['customer_name']}": a['account_no'] for a in accs}
        with st.form("form_deposit", clear_on_submit=True):
            st.markdown("#### Deposit Details")
            selected_label = st.selectbox("Select Account", list(acc_map.keys()))
            amount = st.number_input("Deposit Amount (₹)", min_value=1.0, step=100.0, format="%.2f")
            submitted = st.form_submit_button("💰  Deposit", use_container_width=True)

        if submitted:
            acc_no = acc_map[selected_label]
            try:
                acc = Account(acc_no, None, None, None)
                acc.deposit(amount)
                save_transaction(acc_no, "Deposit", amount)
                new_bal = db_get_account_balance(acc_no)
                st.success(f"✅ ₹{amount:,.2f} deposited into account **{acc_no}**.")
                col1, col2 = st.columns(2)
                col1.metric("Amount Deposited", f"₹{amount:,.2f}")
                col2.metric("New Balance",       f"₹{new_bal:,.2f}")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("---")
        st.markdown("#### Current Account Balances")
        df = pd.DataFrame(accs)
        df = df.drop(columns=["is_active"], errors="ignore")
        df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════
#  PAGE : Withdraw
# ══════════════════════════════════════════════════════════
elif page == "Withdraw":
    accs = db_get_accounts(customer_id=None if _is_admin else _customer_id, active_only=True)
    if not accs:
        st.warning("No active accounts found.")
    else:
        acc_map = {f"{a['account_no']} – {a['customer_name']}": a['account_no'] for a in accs}
        with st.form("form_withdraw", clear_on_submit=True):
            st.markdown("#### Withdrawal Details")
            selected_label = st.selectbox("Select Account", list(acc_map.keys()))
            amount = st.number_input("Withdrawal Amount (₹)", min_value=1.0, step=100.0, format="%.2f")
            submitted = st.form_submit_button("💸  Withdraw", use_container_width=True)

        if submitted:
            acc_no  = acc_map[selected_label]
            cur_bal = db_get_account_balance(acc_no)
            if amount > cur_bal:
                st.error(f"❌ Insufficient funds! Available balance: ₹{cur_bal:,.2f}")
            else:
                try:
                    acc = Account(acc_no, None, None, None)
                    acc.withdraw(amount)
                    save_transaction(acc_no, "Withdrawal", amount)
                    new_bal = db_get_account_balance(acc_no)
                    st.success(f"✅ ₹{amount:,.2f} withdrawn from account **{acc_no}**.")
                    col1, col2 = st.columns(2)
                    col1.metric("Amount Withdrawn", f"₹{amount:,.2f}")
                    col2.metric("New Balance",       f"₹{new_bal:,.2f}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown("---")
        st.markdown("#### Current Account Balances")
        df = pd.DataFrame(accs)
        df = df.drop(columns=["is_active"], errors="ignore")
        df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════
#  PAGE : Transfer Money
# ══════════════════════════════════════════════════════════
elif page == "Transfer Money":
    accs = db_get_accounts(customer_id=None if _is_admin else _customer_id, active_only=True)
    if len(accs) < 2:
        if _is_admin:
            st.warning("You need at least 2 active accounts to transfer money.")
        else:
            st.warning("You need at least 2 active accounts to transfer money. Please create another account first.")
    else:
        acc_map    = {f"{a['account_no']} – {a['customer_name']}": a['account_no'] for a in accs}
        acc_labels = list(acc_map.keys())
        with st.form("form_transfer", clear_on_submit=True):
            st.markdown("#### Transfer Details")
            col1, col2 = st.columns(2)
            with col1:
                from_label = st.selectbox("From Account", acc_labels, key="from_acc")
            with col2:
                to_options = [l for l in acc_labels if l != from_label]
                to_label   = st.selectbox("To Account",   to_options, key="to_acc")
            amount    = st.number_input("Transfer Amount (₹)", min_value=1.0, step=100.0, format="%.2f")
            submitted = st.form_submit_button("🔄  Transfer", use_container_width=True)

        if submitted:
            from_acc = acc_map[from_label]
            to_acc   = acc_map[to_label]
            src_bal  = db_get_account_balance(from_acc)
            if amount > src_bal:
                st.error(f"❌ Insufficient funds in account {from_acc}! Available: ₹{src_bal:,.2f}")
            else:
                try:
                    src = Account(from_acc, None, None, None)
                    dst = Account(to_acc,   None, None, None)
                    src.withdraw(amount)
                    dst.deposit(amount)
                    save_transaction(from_acc, "Transfer Out", amount)
                    save_transaction(to_acc,   "Transfer In",  amount)
                    new_src = db_get_account_balance(from_acc)
                    new_dst = db_get_account_balance(to_acc)
                    st.success(f"✅ ₹{amount:,.2f} transferred from **{from_acc}** → **{to_acc}** successfully!")
                    col1, col2 = st.columns(2)
                    col1.metric(f"{from_acc} New Balance", f"₹{new_src:,.2f}")
                    col2.metric(f"{to_acc} New Balance",   f"₹{new_dst:,.2f}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════
#  PAGE : Display Balance
# ══════════════════════════════════════════════════════════
elif page == "Display Balance":
    accs = db_get_accounts(customer_id=None if _is_admin else _customer_id, active_only=True)
    if not accs:
        st.warning("No active accounts found.")
    else:
        acc_map = {f"{a['account_no']} – {a['customer_name']}": a for a in accs}
        selected_label = st.selectbox("Select Account", list(acc_map.keys()))
        acc = acc_map[selected_label]

        # Live balance from DB
        live_bal = db_get_account_balance(acc["account_no"])

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"""
            <div class="detail-card">
                <p style="font-size:1rem;font-weight:700;color:#00c9a7;margin-bottom:14px;">🏧 Account Information</p>
                <p><b>Account No :</b> {acc['account_no']}</p>
                <p><b>Account Type :</b> {acc['account_type']}</p>
                <p><b>Customer Name :</b> {acc['customer_name']}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.metric("💰 Live Balance", f"₹{live_bal:,.2f}")

            # Fetch customer details
            try:
                conn = get_connection()
                cur  = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM customer WHERE customer_id = %s", (acc["customer_id"],))
                cust = cur.fetchone()
                cur.close(); conn.close()
            except Exception:
                cust = None

            if cust:
                st.markdown(f"""
                <div class="detail-card" style="margin-top:16px;">
                    <p style="font-size:1rem;font-weight:700;color:#00c9a7;margin-bottom:14px;">👤 Customer Details</p>
                    <p><b>Name  :</b> {cust['name']}</p>
                    <p><b>Email :</b> {cust['email']}</p>
                    <p><b>Phone :</b> {cust['phone']}</p>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE : Transaction History
# ══════════════════════════════════════════════════════════
elif page == "Transaction History":
    # Admins see all transactions; customers see only theirs
    txns = get_transactions(user_id=None if _is_admin else _customer_id)

    if not txns:
        st.info("No transactions recorded yet.")
    else:
        df = pd.DataFrame(txns)

        # Summary metrics
        deps = df[df["transaction_type"] == "Deposit"]["amount"].sum()
        wdrs = df[df["transaction_type"] == "Withdrawal"]["amount"].sum()
        trfs = df[df["transaction_type"] == "Transfer Out"]["amount"].sum()

        if _is_admin:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Transactions", len(df))
            col2.metric("Total Deposited",    f"₹{float(deps):,.2f}")
            col3.metric("Total Withdrawn",    f"₹{float(wdrs):,.2f}")
            col4.metric("Total Transferred",  f"₹{float(trfs):,.2f}")
        else:
            # Customer: show their own transaction summary only
            col1, col2, col3 = st.columns(3)
            col1.metric("My Transactions", len(df))
            col2.metric("Deposited",       f"₹{float(deps):,.2f}")
            col3.metric("Withdrawn",       f"₹{float(wdrs):,.2f}")

        st.markdown("---")
        st.markdown("#### All Transactions" if _is_admin else "#### My Transactions")

        # Format for display
        df["amount"] = df["amount"].apply(lambda x: f"₹{float(x):,.2f}")
        if "created_at" in df.columns:
            df["created_at"] = df["created_at"].astype(str)
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
