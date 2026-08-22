from bank.database import get_connection

class Account:
    def __init__(self, acc_no, customer_id,account_type, balance):
        self.acc_no = acc_no
        self.customer_id = customer_id
        self.account_type = account_type
        self.balance = balance

    def save(self):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO account
            (customer_id, account_type, balance)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                self.customer_id,
                self.account_type,
                self.balance
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

    def deposit(self, amount):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE account
            SET balance = balance + %s
            WHERE account_no = %s
        """

        cursor.execute(
            query,
            (amount, self.acc_no)
        )

        connection.commit()

        cursor.close()
        connection.close()

    def withdraw(self, amount):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE account
            SET balance = balance - %s
            WHERE account_no = %s
            AND balance >= %s
        """

        cursor.execute(
            query,
            (amount, self.acc_no, amount)
        )

        connection.commit()

        if cursor.rowcount == 0:
            print("Insufficient balance")

        cursor.close()
        connection.close()