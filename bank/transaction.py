from bank.database import get_connection


def save_transaction(account_no, transaction_type, amount):
    """Insert a new row into transaction_history."""
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO transaction_history
        (account_no, transaction_type, amount)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (account_no, transaction_type, amount)
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_transactions(user_id=None):
    """
    Return transaction rows as a list of dicts.

    Parameters
    ----------
    user_id : int or None
        * None  – return ALL transactions (admin view).
        * int   – return only transactions belonging to this customer_id.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if user_id is not None:
            # Customer view: only rows where the account belongs to this customer
            query = """
                SELECT
                    th.id,
                    th.account_no,
                    c.name        AS customer_name,
                    th.transaction_type,
                    th.amount,
                    th.created_at
                FROM transaction_history th
                JOIN account  a ON th.account_no    = a.account_no
                JOIN customer c ON a.customer_id    = c.customer_id
                WHERE c.customer_id = %s
                ORDER BY th.id DESC
            """
            cursor.execute(query, (user_id,))
        else:
            # Admin view: all transactions
            query = """
                SELECT
                    th.id,
                    th.account_no,
                    c.name        AS customer_name,
                    th.transaction_type,
                    th.amount,
                    th.created_at
                FROM transaction_history th
                LEFT JOIN account  a ON th.account_no = a.account_no
                LEFT JOIN customer c ON a.customer_id = c.customer_id
                ORDER BY th.id DESC
            """
            cursor.execute(query)

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Exception as e:
        print(f"[transaction] get_transactions error: {e}")
        return []