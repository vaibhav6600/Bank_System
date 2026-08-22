from bank.database import get_connection


def save_transaction(account_no, transaction_type, amount):

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