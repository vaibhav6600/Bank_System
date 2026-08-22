import sys
sys.path.append(r"C:\Users\Admin\PycharmProjects\PythonProject")

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from bank.customer import Customer
from bank.account import Account
from bank.database import get_connection
from bank.transaction import save_transaction

# ══════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
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
#  DB HELPER FUNCTIONS  –  all data comes from MySQL
# ══════════════════════════════════════════════════════════

def db_get_stats():
    """Return (n_customers, n_accounts, total_balance) from DB."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customer")
        n_cust = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*), COALESCE(SUM(balance),0) FROM account")
        row = cur.fetchone()
        n_acc, total_bal = row[0], float(row[1])
        cur.close(); conn.close()
        return n_cust, n_acc, total_bal
    except Exception:
        return 0, 0, 0.0


def db_get_customers():
    """Return list of dicts from customer table."""
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM customer ORDER BY customer_id DESC")
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception:
        return []


def db_get_accounts():
    """Return list of dicts from account table joined with customer name."""
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.account_no, a.customer_id, c.name AS customer_name,
                   a.account_type, a.balance
            FROM account a
            LEFT JOIN customer c ON a.customer_id = c.customer_id
            ORDER BY a.account_no DESC
        """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception:
        return []


def db_get_transactions():
    """Return list of dicts from transaction_history table."""
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT th.id, th.account_no, c.name AS customer_name,
                   th.transaction_type, th.amount, th.created_at
            FROM transaction_history th
            LEFT JOIN account a ON th.account_no = a.account_no
            LEFT JOIN customer c ON a.customer_id = c.customer_id
            ORDER BY th.id DESC
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


# ══════════════════════════════════════════════════════════
#  SESSION STATE  –  only for navigation, not data
# ══════════════════════════════════════════════════════════
PAGES = [
    ("🏠", "Dashboard"),
    ("👤", "Create Customer"),
    ("🏧", "Create Account"),
    ("💰", "Deposit"),
    ("💸", "Withdraw"),
    ("🔄", "Transfer Money"),
    ("📊", "Display Balance"),
    ("🧾", "Transaction History"),
]

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    # ── Brand ──
    st.markdown("""
    <div style="padding:20px 18px 10px;">
        <div style="font-size:2rem;">🏦</div>
        <div style="font-size:1.15rem;font-weight:800;color:#ffffff;margin-top:4px;">BankPro</div>
        <div style="font-size:0.78rem;color:#9fa8da;margin-top:2px;">Management System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:4px 18px 10px;"></div>', unsafe_allow_html=True)

    # ── Navigation buttons ──
    st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)
    for icon, label in PAGES:
        active_cls = "active" if st.session_state.page == label else ""
        if st.button(f"{icon}  {label}", key=f"nav_{label}",
                     use_container_width=True):
            st.session_state.page = label
            st.rerun()

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:14px 18px 10px;"></div>', unsafe_allow_html=True)

    # ── Live stats from DB ──
    st.markdown('<div class="section-label">Live Stats</div>', unsafe_allow_html=True)
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


# ══════════════════════════════════════════════════════════
#  PAGE HEADER  –  always rendered at the top of the page
# ══════════════════════════════════════════════════════════
PAGE_META = {
    "Dashboard":         ("🏠", "Dashboard", "Overview of all banking operations"),
    "Create Customer":   ("👤", "Create Customer", "Register a new customer in the system"),
    "Create Account":    ("🏧", "Create Account", "Open a new bank account for a customer"),
    "Deposit":           ("💰", "Deposit Money", "Add funds to a customer account"),
    "Withdraw":          ("💸", "Withdraw Money", "Withdraw funds from a customer account"),
    "Transfer Money":    ("🔄", "Transfer Money", "Move funds between two accounts"),
    "Display Balance":   ("📊", "Account Balance", "View detailed balance and account info"),
    "Transaction History": ("🧾", "Transaction History", "Full audit log of all transactions"),
}

page = st.session_state.page
icon, title, subtitle = PAGE_META[page]
st.markdown(f"""
<div class="page-header">
    <div class="icon">{icon}</div>
    <div>
        <div class="title">{title}</div>
        <div class="subtitle">{subtitle}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE : Dashboard
# ══════════════════════════════════════════════════════════
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", n_cust)
    col2.metric("Total Accounts",  n_acc)
    col3.metric("Total Bank Balance", f"₹{total_bal:,.2f}")

    st.markdown("---")

    accounts_data = db_get_accounts()
    if accounts_data:
        st.markdown("### All Accounts")
        df = pd.DataFrame(accounts_data)
        df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No accounts yet. Create a customer and account to get started.")


# ══════════════════════════════════════════════════════════
#  PAGE : Create Customer
# ══════════════════════════════════════════════════════════
elif page == "Create Customer":
    with st.form("form_create_customer", clear_on_submit=True):
        st.markdown("#### Customer Details")
        col1, col2 = st.columns(2)
        with col1:
            name  = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            email = st.text_input("Email", placeholder="e.g. rahul@example.com")
        with col2:
            phone = st.text_input("Phone Number", placeholder="e.g. 9876543210")
        submitted = st.form_submit_button("➕  Create Customer", use_container_width=True)

    if submitted:
        if not all([name, email, phone]):
            st.error("All fields are required.")
        else:
            try:
                c = Customer(None, name, email, phone)
                c.save()
                st.success(f"✅ Customer **{name}** created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("#### Existing Customers")
    custs = db_get_customers()
    if custs:
        df = pd.DataFrame(custs)
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No customers found.")


# ══════════════════════════════════════════════════════════
#  PAGE : Create Account
# ══════════════════════════════════════════════════════════
elif page == "Create Account":
    custs = db_get_customers()
    if not custs:
        st.warning("No customers found. Please create a customer first.")
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
                st.success(f"✅ Account created successfully with ₹{balance:,.2f} initial deposit!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("---")
        st.markdown("#### Existing Accounts")
        accs = db_get_accounts()
        if accs:
            df = pd.DataFrame(accs)
            df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No accounts yet.")


# ══════════════════════════════════════════════════════════
#  PAGE : Deposit
# ══════════════════════════════════════════════════════════
elif page == "Deposit":
    accs = db_get_accounts()
    if not accs:
        st.warning("No accounts found. Please create an account first.")
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
                col2.metric("New Balance", f"₹{new_bal:,.2f}")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("---")
        st.markdown("#### Current Account Balances")
        df = pd.DataFrame(accs)
        df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════
#  PAGE : Withdraw
# ══════════════════════════════════════════════════════════
elif page == "Withdraw":
    accs = db_get_accounts()
    if not accs:
        st.warning("No accounts found. Please create an account first.")
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
                    col2.metric("New Balance", f"₹{new_bal:,.2f}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown("---")
        st.markdown("#### Current Account Balances")
        df = pd.DataFrame(accs)
        df["balance"] = df["balance"].apply(lambda x: f"₹{float(x):,.2f}")
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════
#  PAGE : Transfer Money
# ══════════════════════════════════════════════════════════
elif page == "Transfer Money":
    accs = db_get_accounts()
    if len(accs) < 2:
        st.warning("You need at least 2 accounts to transfer money.")
    else:
        acc_map = {f"{a['account_no']} – {a['customer_name']}": a['account_no'] for a in accs}
        acc_labels = list(acc_map.keys())
        with st.form("form_transfer", clear_on_submit=True):
            st.markdown("#### Transfer Details")
            col1, col2 = st.columns(2)
            with col1:
                from_label = st.selectbox("From Account", acc_labels, key="from_acc")
            with col2:
                to_options = [l for l in acc_labels if l != from_label]
                to_label   = st.selectbox("To Account", to_options, key="to_acc")
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
    accs = db_get_accounts()
    if not accs:
        st.warning("No accounts found.")
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
                <p style="font-size:1rem;font-weight:700;color:#1a237e;margin-bottom:14px;">🏧 Account Information</p>
                <p><b>Account No :</b> {acc['account_no']}</p>
                <p><b>Account Type :</b> {acc['account_type']}</p>
                <p><b>Customer ID :</b> {acc['customer_id']}</p>
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
                    <p style="font-size:1rem;font-weight:700;color:#1a237e;margin-bottom:14px;">👤 Customer Details</p>
                    <p><b>Name  :</b> {cust['name']}</p>
                    <p><b>Email :</b> {cust['email']}</p>
                    <p><b>Phone :</b> {cust['phone']}</p>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE : Transaction History
# ══════════════════════════════════════════════════════════
elif page == "Transaction History":
    txns = db_get_transactions()
    if not txns:
        st.info("No transactions recorded yet.")
    else:
        df = pd.DataFrame(txns)

        # Summary metrics from DB
        deps  = df[df["transaction_type"] == "Deposit"]["amount"].sum()
        wdrs  = df[df["transaction_type"] == "Withdrawal"]["amount"].sum()
        trfs  = df[df["transaction_type"] == "Transfer Out"]["amount"].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Transactions", len(df))
        col2.metric("Total Deposited",    f"₹{float(deps):,.2f}")
        col3.metric("Total Withdrawn",    f"₹{float(wdrs):,.2f}")
        col4.metric("Total Transferred",  f"₹{float(trfs):,.2f}")

        st.markdown("---")
        st.markdown("#### All Transactions")

        # Format for display
        df["amount"] = df["amount"].apply(lambda x: f"₹{float(x):,.2f}")
        if "created_at" in df.columns:
            df["created_at"] = df["created_at"].astype(str)
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
