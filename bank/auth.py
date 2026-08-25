"""
bank/auth.py
Authentication helpers for the BankPro app.

The `users` table stores passwords in the `password_hash` column.
For this project we support two storage strategies:
  1. Plain-text (legacy) – compare directly.
  2. bcrypt hash – use bcrypt.checkpw().

We auto-detect which strategy is in use so older accounts still work.
"""

import sys
sys.path.append(r"C:\Users\Admin\PycharmProjects\PythonProject")

from bank.database import get_connection

# Try importing bcrypt; if unavailable, only plain-text passwords work.
try:
    import bcrypt
    _BCRYPT_AVAILABLE = True
except ImportError:
    _BCRYPT_AVAILABLE = False


def _verify_password(plain: str, stored: str) -> bool:
    """Return True if `plain` matches `stored` (bcrypt hash or plain-text)."""
    if _BCRYPT_AVAILABLE and stored.startswith("$2"):
        # bcrypt hash
        return bcrypt.checkpw(plain.encode(), stored.encode())
    # Plain-text comparison (legacy / development)
    return plain == stored


def _hash_password(plain: str) -> str:
    """Return a bcrypt hash if bcrypt is available, else plain-text."""
    if _BCRYPT_AVAILABLE:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()
    return plain


def get_user_by_username(username: str) -> dict | None:
    """
    Fetch the user row from `users` table plus the associated customer_id.

    Returns a dict with keys:
        user_id, username, role, is_active, password_hash, customer_id (may be None)
    or None if not found.
    """
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        # Left-join to customer table on matching email or username so we can
        # look up the customer_id that belongs to this user.
        cur.execute(
            """
            SELECT
                u.user_id,
                u.username,
                u.email,
                u.password_hash,
                u.role,
                u.is_active,
                c.customer_id
            FROM users u
            LEFT JOIN customer c ON c.email = u.email
            WHERE u.username = %s
            LIMIT 1
            """,
            (username,)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row
    except Exception as e:
        print(f"[auth] get_user_by_username error: {e}")
        return None


def authenticate(username: str, password: str) -> dict | None:
    """
    Validate credentials.

    Returns the user dict (with customer_id) on success, or None on failure.
    """
    if not username or not password:
        return None

    user = get_user_by_username(username)
    if user is None:
        return None

    if not user.get("is_active"):
        return None

    if not _verify_password(password, user["password_hash"]):
        return None

    return user


def register_customer_user(name: str, email: str, phone: str, password: str) -> tuple[bool, str]:
    """
    Register a new customer via self-registration.

    Steps:
      1. Check that the email is not already used in `users` or `customer`.
      2. Insert a new row into `customer` (is_active=1).
      3. Insert a new row into `users` with role='CUSTOMER', is_active=1,
         and the hashed (or plain) password chosen by the customer.

    Returns (True, "ok") on success or (False, error_message) on failure.
    """
    if not all([name, email, phone, password]):
        return False, "All fields are required."

    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)

        # Check for duplicate email in users table
        cur.execute("SELECT user_id FROM users WHERE email = %s LIMIT 1", (email,))
        if cur.fetchone():
            cur.close(); conn.close()
            return False, "An account with this email already exists. Please log in."

        # Check for duplicate email in customer table
        cur.execute("SELECT customer_id FROM customer WHERE email = %s LIMIT 1", (email,))
        if cur.fetchone():
            cur.close(); conn.close()
            return False, "A customer with this email already exists."

        # Insert into customer
        cur.execute(
            "INSERT INTO customer (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        conn.commit()

        # Insert into users (username = email, role = CUSTOMER)
        pw_hash = _hash_password(password)
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (%s, %s, %s, 'CUSTOMER', 1)
            """,
            (email, email, pw_hash)
        )
        conn.commit()
        cur.close(); conn.close()
        return True, "ok"

    except Exception as e:
        return False, str(e)


def create_customer_with_default_user(name: str, email: str, phone: str) -> tuple[bool, str]:
    """
    Admin helper: inserts a customer AND a matching users row with default password '1234'.

    Returns (True, "ok") on success or (False, error_message) on failure.
    """
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)

        # Check for duplicate email in users table
        cur.execute("SELECT user_id FROM users WHERE email = %s LIMIT 1", (email,))
        if cur.fetchone():
            cur.close(); conn.close()
            return False, "A user with this email already exists."

        # Insert into customer
        cur.execute(
            "INSERT INTO customer (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        conn.commit()

        # Insert into users with default password "1234"
        pw_hash = _hash_password("1234")
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (%s, %s, %s, 'CUSTOMER', 1)
            """,
            (email, email, pw_hash)
        )
        conn.commit()
        cur.close(); conn.close()
        return True, "ok"

    except Exception as e:
        return False, str(e)
