from bank.database import get_connection

class Customer:
    def __init__(self, id,name,email,phone_number):
        self.customer_id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def save(self):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO customer(name, email, phone)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (self.name, self.email, self.phone_number)
        )

        connection.commit()

        cursor.close()
        connection.close()