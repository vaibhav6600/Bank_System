"""
login.py
Attractive, dark-teal themed login page for BankPro.
Imported by app.py at the very start; renders only when the user
is not authenticated.
"""

import sys
sys.path.append(r"C:\Users\Admin\PycharmProjects\PythonProject")

# pyrefly: ignore [missing-import]
import streamlit as st
from bank.auth import authenticate


# ──────────────────────────────────────────────────────────
#  LOGIN PAGE CSS  (applied only on the login screen)
# ──────────────────────────────────────────────────────────
_LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Dark background */
.stApp {
    background: radial-gradient(ellipse at top left, #0d1f3c 0%, #0a0f1e 55%, #050810 100%);
    min-height: 100vh;
}

/* Hide default Streamlit chrome */
header[data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
#MainMenu, footer { visibility: hidden; }

/* ── Login card ── */
.login-wrapper {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 60px;
}
.login-card {
    background: linear-gradient(145deg, #10172a 0%, #161d30 100%);
    border: 1px solid rgba(0,201,167,0.22);
    border-radius: 24px;
    padding: 44px 48px 36px;
    width: 100%;
    max-width: 440px;
    box-shadow:
        0 0 0 1px rgba(0,201,167,0.06),
        0 8px 40px rgba(0,0,0,0.55),
        0 0 60px rgba(0,201,167,0.07);
    text-align: center;
}
.login-logo {
    font-size: 3.2rem;
    margin-bottom: 6px;
    filter: drop-shadow(0 0 12px rgba(0,201,167,0.6));
}
.login-brand {
    font-size: 1.7rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #00c9a7 0%, #0096c7 60%, #845ef7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.login-sub {
    font-size: 0.83rem;
    color: #5d7a8a;
    margin-bottom: 32px;
    letter-spacing: 0.3px;
}
.login-divider {
    height: 1px;
    background: rgba(0,201,167,0.12);
    margin: 24px 0;
}

/* Input overrides */
input {
    background: #0d1117 !important;
    border: 1.5px solid rgba(0,201,167,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.94rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input:focus {
    border-color: #00c9a7 !important;
    box-shadow: 0 0 0 3px rgba(0,201,167,0.15) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #8892a4 !important;
    font-weight: 600;
    font-size: 0.85rem;
    text-align: left;
}

/* Login button */
.stButton > button {
    background: linear-gradient(135deg, #00c9a7 0%, #0096c7 100%) !important;
    color: #0a0f1e !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 13px 32px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.4px !important;
    width: 100% !important;
    margin-top: 8px !important;
    box-shadow: 0 4px 20px rgba(0,201,167,0.4) !important;
    transition: all 0.22s ease !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 32px rgba(0,201,167,0.55) !important;
    filter: brightness(1.06) !important;
}

/* Alert tweaks */
div[data-testid="stAlert"] { border-radius: 10px !important; font-size: 0.9rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: rgba(0,201,167,0.3); border-radius: 6px; }
</style>
"""


def render_login():
    """
    Display the BankPro login card.
    Blocks execution until the user successfully authenticates.
    """
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)

    # Centre the card with Streamlit columns
    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        # Brand header
        st.markdown(
            """
            <div style="text-align:center;padding-bottom:4px;">
                <div class="login-logo">🏦</div>
                <div class="login-brand">BankPro</div>
                <div class="login-sub">Secure Banking Management System</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="login-divider"></div>',
            unsafe_allow_html=True,
        )

        # ── Credentials form ──
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
            )
            submitted = st.form_submit_button("🔐  Sign In", use_container_width=True)

        if submitted:
            user = authenticate(username.strip(), password)
            if user:
                st.session_state["authenticated"] = True
                st.session_state["user"]          = user
                st.session_state["role"]          = user["role"]          # 'ADMIN' or 'CUSTOMER'
                st.session_state["customer_id"]   = user.get("customer_id")
                st.session_state["display_name"]  = user["username"]
                st.rerun()
            else:
                st.error("❌  Invalid username or password. Please try again.")

        # Footer note
        st.markdown(
            """
            <div style="text-align:center;margin-top:20px;">
                <span style="font-size:0.75rem;color:#3d5a6b;">
                    🔒 Protected by BankPro Security
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Hard-stop – prevent the rest of app.py from rendering
    st.stop()
