import sys
sys.path.append(r"C:\Users\Admin\PycharmProjects\PythonProject")
from bank.customer import Customer
from bank.account import Account


#==============================================================================================

print("===========================================")
print("Welcome to the Bank Management System")
print("===========================================")
print("   Total Customers:     12")
print("   Total Accounts:      15")
print("   Total Bank Balance:  ₹2,50,000")
print("---------------------------------------------------------------------------")
print()
print("Choose an operation : ")
print(" [1. Create Customer ]     [2. Create Account ]     [3. Deposit ]")
print(" [4. Withdraw ]     [5. Transfer Money ]     [6. Display Balance ]")
print("---------------------------------------------------------------------------")

cust_id=""
choice = int(input("Please choose an operation : "))

if choice == 1:
    re_enter = ""
    for i in range(3):
        customer_id = input("Please enter the customer id for your account : ")
        name = input("Please enter the name of the customer : ")
        email = input("Please enter the email of the customer : ")
        phone = input("Please enter the phone number of the customer : ")

        if customer_id != "" and name != "" and email != "" and phone != "":
            print("----------------------------------------------------------------------")
            c = Customer(customer_id, name, email, phone)
            print("Customer created successfully!")
            cust_id = customer_id
            break
        else:
            print("----------------------------------------------------------------------")
            print("Invalid input")

            if i == 2:
                print("Reached maximum attempts!")
                break
            re_enter = input("Do you want to re-create customer : ( yes / no )")
        if re_enter == "yes":
            continue

        else:
            break

if cust_id != "":
    cr_acc = input("Do you want to create account? [yes/no] : ")
    if cr_acc == "yes":
        re_enter = ""
        for i in range(3):
            print("----------------------------------------------------------------------")
            acc_no = input("Please enter account number for your account : ")
            account_type = input("Please enter account type for your account : ")
            balance = input("Please enter the first deposit amount  : ")
            if acc_no != "" and account_type !="" and balance != "":
                print("----------------------------------------------------------------------")
                a = Account(acc_no, cust_id,account_type, balance)
                print("Account created successfully!")
                break
            else:
                print("----------------------------------------------------------------------")
                print("Invalid input")
                if i == 2:
                    print("Reached maximum attempts!")
                    break
                re_enter = input("Do you want to re-create customer : ( yes / no )")
                if re_enter == "yes":
                    continue
                else:
                    break

    else:
        print("Thank you...!")
