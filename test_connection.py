from bank.database import get_connection

connection = get_connection()

if connection.is_connected():
    print("MySQL connected successfully!")

connection.close()