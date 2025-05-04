import os

# Variable to auto-generate unique account numbers
init_account_number = 1000
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
    with open("accounts.txt", "a") as file:
        for accNo, acc in accounts.items():
            file.write(f"Account Number: {accNo}\n")
            file.write(f"Name: {acc['name']}\n")
            file.write(f"Email: {acc['email']}\n")
            file.write(f"NIC: {acc['nic']}\n")
            file.write(f"Phone: {acc['phone']}\n")
            file.write(f"Balance: {acc['balance']}\n")
            file.write("\n")
    print("Accounts saved to file.")

    # Save Transaction History
def save_transaction_history(account_number,Transaction_type,amount):
        with open("transactionHistory.txt", "a") as file:
            for accNo, acc in accounts.items():
                file.write(f"Account Number: {account_number}\n")
                file.write(f"Transaction Name: {Transaction_type}\n")
                file.write(f"Amount: {amount}\n")
                file.write("\n")
        print("Transaction History is saved Successfully.")


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
                elif line.startswith("Transactions:"):
                    tx_str = line.split(":", 1)[1].strip()
                    current_account["transactions"] = tx_str.split(", ")
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
        print("5. Money Transfer")
        print("6. Transaction History")
        print("7. Exit")

        choice = input("Choose an option: ").strip()
        if choice == '1':
            create_new_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            print("Check Balance")
        elif choice == '5':
            print("Money Transfer")
        elif choice == '6':
            print("Transaction History")
        elif choice == '7':
            print("Exiting system...")
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




# Entry point of the application
if __name__ == "__main__":
    if user_authentication():
        load_account_details()  # Load existing account data before showing the menu
        display_main_menu()
