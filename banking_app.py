import os
import sys


# Variable to auto-generate unique account numbers
init_account_number = 1000
INTEREST_RATE = 0.03  # 3% annual interest
accounts = {}


# Load username and password from user.txt
def load_username_and_password():
    user_data = {}
    if os.path.exists("user.txt"):
        with open("user.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("username:"):
                    user_data["username"] = line.split(":", 1)[1].strip()
                elif line.startswith("password:"):
                    user_data["password"] = line.split(":", 1)[1].strip()
    return user_data


# Authentication function
def user_authentication():
    user_data = load_username_and_password()
    if not user_data:
        print("User data not found.")
        return False

    input_username = input("Enter Username: ").strip()
    input_password = input("Enter Password: ").strip()

    if input_username == user_data.get("username") and input_password == user_data.get("password"):
        print("Login successful!")
        return True
    else:
        print("Invalid credentials.")
        return False


# Helper function to get non-empty input
def get_non_empty_input(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Error: This field cannot be empty.")


# Function to create a new User
def create_new_account():
    global init_account_number

    print("\nCreate a New Account")

    name = get_non_empty_input("Enter account holder's name: ")

    # Email Duplicate Entry Validation
    while True:
        email = get_non_empty_input("Enter email address: ")
        if any(acc["email"].lower() == email.lower() for acc in accounts.values()):
            print("Error: This email address is already registered.")
        else:
            break

    # NIC Duplicate Entry Validation
    while True:
        nic = get_non_empty_input("Enter NIC: ")
        if any(acc["nic"].lower() == nic.lower() for acc in accounts.values()):
            print("Error: This NIC is already registered.")
        else:
            break

    # Phone number duplicate Entry Validation
    while True:
        phone = get_non_empty_input("Enter phone number: ")
        if any(acc["phone"] == phone for acc in accounts.values()):
            print("Error: This phone number is already registered.")
        else:
            break


    # Initial deposit validation
    while True:
        initial_input = get_non_empty_input("Enter initial deposit amount: ")
        try:
            initial_deposit = float(initial_input)
            if initial_deposit < 0:
                print("Amount cannot be negative. Please enter a positive value.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    # Generate and print unique account number
    account_number = init_account_number
    init_account_number += 1

    print(f"\nAccount successfully created!")
    print(f"Your Account Number is: {account_number}")

    accounts[account_number] = {
        'name': name,
        'email': email,
        'nic': nic,
        'phone': phone,
        'balance': initial_deposit,
        'transactions': [f"Account created with initial deposit of {initial_deposit}"]
    }

    save_account_details()
    save_transaction_history(account_number,"Initial Deposit",initial_deposit)


# Save account details to a file
def save_account_details():
    with open("accounts.txt", "w") as file:
        for accNo, acc in accounts.items():
            file.write(f"Account Number: {accNo}\n")
            file.write(f"Name: {acc['name']}\n")
            file.write(f"Email: {acc['email']}\n")
            file.write(f"NIC: {acc['nic']}\n")
            file.write(f"Phone: {acc['phone']}\n")
            file.write(f"Balance: {acc['balance']:.2f}\n")  # Two decimal places
            file.write("\n")
    print("Accounts saved to file.")

# Save Transaction History only once to avoid duplicates
def save_transaction_history(account_number, transaction_type, amount):
    from datetime import datetime

    # Read current transaction history to avoid duplicates
    existing_transactions = []
    if os.path.exists("transactionHistory.txt"):
        with open("transactionHistory.txt", "r") as file:
            existing_transactions = file.readlines()

    # Check if the transaction for this account already exists
    transaction_found = False
    for line in existing_transactions:
        if f"Account Number: {account_number}" in line and f"Transaction Name: {transaction_type}" in line:
            transaction_found = True
            break

    if not transaction_found:
        # Get current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save transaction only if it doesn't exist already
        with open("transactionHistory.txt", "a") as file:
            file.write(f"Account Number: {account_number}\n")
            file.write(f"Transaction Name: {transaction_type}\n")
            file.write(f"Amount: {amount:.2f}\n")
            file.write(f"Date and Time: {current_time}\n")
            file.write("\n")


# Load existing account details from file
def load_account_details():
    global accounts, init_account_number
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as file:
            lines = file.readlines()
            current_account = {}
            acc_no = None
            for line in lines:
                line = line.strip()
                if line.startswith("Account Number:"):
                    if acc_no is not None and current_account:  # Save previous account
                        current_account["transactions"] = []
                        accounts[acc_no] = current_account
                        init_account_number = max(init_account_number, acc_no + 1)

                    acc_no = int(line.split(":")[1].strip())
                    current_account = {}
                elif line.startswith("Name:"):
                    current_account["name"] = line.split(":")[1].strip()
                elif line.startswith("Email:"):
                    current_account["email"] = line.split(":")[1].strip()
                elif line.startswith("NIC:"):
                    current_account["nic"] = line.split(":")[1].strip()
                elif line.startswith("Phone:"):
                    current_account["phone"] = line.split(":")[1].strip()
                elif line.startswith("Balance:"):
                    current_account["balance"] = float(line.split(":")[1].strip())

            # Save the last account after reading
            if acc_no is not None and current_account:
                current_account["transactions"] = []
                accounts[acc_no] = current_account
                init_account_number = max(init_account_number, acc_no + 1)


# Display Main menu after successful authentication
def display_main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Fund Transfer")
        print("6. Transaction History")
        print("7. Apply Interest")
        print("8. Exit")

        choice = input("Choose an option: ").strip()
        if choice == '1':
            create_new_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            fund_transfer()
        elif choice == '6':
            display_transaction_history()
        elif choice == '7':
            apply_interest()
        elif choice == '8':
            exit_application()
            break
        else:
            print("Invalid choice! Please try again.")

# Deposit money, update balance and transaction history
def deposit_money():
    print("\n--- Deposit Money ---")
    try:
        acc_no = int(get_non_empty_input("Enter your account number: "))
        if acc_no not in accounts:
            print("Account not found!")
            return

        deposit_input = get_non_empty_input("Enter amount to deposit: ")
        amount = float(deposit_input)
        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return

        accounts[acc_no]['balance'] += amount
        print(f"Deposit successful. New balance: {accounts[acc_no]['balance']}")

        save_account_details()
        save_transaction_history(acc_no, "Deposit", amount)

    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Withdraw money, update balance and transaction history
def withdraw_money():
    print("\n--- Withdraw Money ---")
    try:
        acc_no = int(get_non_empty_input("Enter your account number: "))
        if acc_no not in accounts:
            print("Account not found!")
            return

        withdraw_input = get_non_empty_input("Enter amount to withdraw: ")
        amount = float(withdraw_input)

        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return

        if amount > accounts[acc_no]['balance']:
            print("Insufficient balance for this transaction.")
            return

        accounts[acc_no]['balance'] -= amount

        print(f"Withdrawal successful. Remaining balance: {accounts[acc_no]['balance']}")

        save_account_details()
        save_transaction_history(acc_no, "Withdrawal", amount)

    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Function to check balance
def check_balance():
    print("\n--- Check Account Balance ---")
    try:
        acc_no = int(get_non_empty_input("Enter your account number: "))
        if acc_no not in accounts:
            print("Account not found!")
            return
        account_holder = accounts[acc_no]['name']
        email = accounts[acc_no]['email']
        phone = accounts[acc_no]['phone']
        balance = accounts[acc_no]['balance']

        print("Account No: " + str(acc_no))
        print("Account Holder: " + account_holder)
        print("E mail: " + email)
        print("Phone: " + phone)
        print("Balance: " + str(balance))

    except ValueError:
        print("Invalid input. Please enter a valid account number.")

# Transfer funds between accounts
def fund_transfer():
    print("\n--- Fund Transfer ---")
    try:
        sender_acc_no = int(get_non_empty_input("Enter sender account number: "))
        if sender_acc_no not in accounts:
            print("Sender account not found!")
            return

        receiver_acc_no = int(get_non_empty_input("Enter recipient's account number: "))
        if receiver_acc_no not in accounts:
            print("Recipient account not found!")
            return

        if sender_acc_no == receiver_acc_no:
            print("Cannot transfer to the same account.")
            return

        transfer_input = get_non_empty_input("Enter amount to transfer: ")
        amount = float(transfer_input)

        if amount <= 0:
            print("Transfer amount must be greater than zero.")
            return

        if amount > accounts[sender_acc_no]['balance']:
            print("Insufficient balance for this transaction.")
            return

        # Perform transfer
        accounts[sender_acc_no]['balance'] -= amount
        accounts[receiver_acc_no]['balance'] += amount

        print(f"Transfer successful. Remaining balance: {accounts[sender_acc_no]['balance']:.2f}")

        # Save updated data
        save_account_details()

        # Log transaction for sender and receiver
        save_transaction_history(sender_acc_no, "Transfer Out", amount)
        save_transaction_history(receiver_acc_no, "Transfer In", amount)

    except ValueError:
        print("Invalid input. Please enter valid account numbers and amount.")

# Display Transaction History for a specific account
def display_transaction_history():
    print("\n--- Transaction History ---")
    try:
        acc_no = int(get_non_empty_input("Enter account number: "))
        if acc_no not in accounts:
            print("Account not found!")
            return

        # Display account details
        account = accounts[acc_no]
        print("\nAccount Details:")
        print(f"Account Number : {acc_no}")
        print(f"Account Holder : {account['name']}")
        print(f"Email          : {account['email']}")
        print(f"Phone          : {account['phone']}")
        print(f"Current Balance: {account['balance']:.2f}")

        print("\nTransaction History:")

        if not os.path.exists("transactionHistory.txt"):
            print("No transaction history found.")
            return

        with open("transactionHistory.txt", "r") as file:
            lines = file.readlines()

        found = False
        i = 0
        while i < len(lines):
            if lines[i].strip() == f"Account Number: {acc_no}":
                found = True
                print("-" * 40)
                print(lines[i].strip())         # Account Number
                print(lines[i+1].strip())       # Transaction Name
                print(lines[i+2].strip())       # Amount
                print(lines[i+3].strip())       # Date and Time
                i += 5                          # Skip to next block
            else:
                i += 1

        if not found:
            print("No transactions found for this account.")

    except ValueError:
        print("Invalid input. Please enter a valid account number.")



def apply_interest():
    print("\n--- Apply Interest to All Accounts ---")
    try:
        for acc_no, acc in accounts.items():
            interest = acc['balance'] * INTEREST_RATE
            acc['balance'] += interest
            acc['transactions'].append(f"Interest of {interest:.2f} applied")
            save_transaction_history(acc_no, "Interest", interest)

        save_account_details()
        print("Interest applied to all accounts successfully.")

    except Exception as e:
        print(f"An error occurred while applying interest: {str(e)}")


#Exite from the application

def exit_application():
    while True:
        confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
        if confirm == 'y':
            print("\nHave a nice day. Goodbye!")
            sys.exit()
        elif confirm == 'n':
            print("Returning to main menu...")
            return
        else:
            print("Invalid input. Please enter 'y' or 'n'.")



# Entry point of the application
if __name__ == "__main__":
    try:
        if user_authentication():
            load_account_details()
            display_main_menu()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Exiting safely...")
        sys.exit()