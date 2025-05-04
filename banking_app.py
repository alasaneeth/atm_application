import os

# Dictionary to store account data
accounts = {}


def isDuplicate(field, value):
    """Check for duplicate field value (e.g., email, NIC)."""
    for account in accounts.values():
        if account[field] == value:
            return True
    return False


def positiveInput(prompt):
    """Validate that user input is a positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Amount cannot be negative. Please enter a positive value.")
            else:
                return value
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def createNewAccount():
    """Create a new account with unique details."""
    print("\nCreate a New Account")

    # Helper function to get non-empty input
    def getNonEmptyInput(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Error: This field cannot be empty.")

    name = getNonEmptyInput("Enter account holder's name: ")
    email = getNonEmptyInput("Enter email address: ")
    if isDuplicate('email', email):
        print("Error: Email already exists.")
        return

    nic = getNonEmptyInput("Enter NIC: ")
    if isDuplicate('nic', nic):
        print("Error: NIC already exists.")
        return

    phone = getNonEmptyInput("Enter phone number: ")
    if isDuplicate('phone', phone):
        print("Error: Phone number already exists.")
        return

    username = getNonEmptyInput("Create a username: ")
    if isDuplicate('username', username):
        print("Error: Username already exists.")
        return

    password = getNonEmptyInput("Create a password: ")
    if isDuplicate('password', password):
        print("Error: Password already exists.")
        return

    initBalance = positiveInput("Enter initial deposit amount: ")
    accountNumber = len(accounts) + 1

    accounts[accountNumber] = {
        'name': name,
        'email': email,
        'nic': nic,
        'phone': phone,
        'username': username,
        'password': password,
        'balance': initBalance,
        'transactions': [f"Account created with initial deposit of {initBalance}"]
    }

    print(f"Account created successfully! Your account number is {accountNumber}.")
    saveUserDetails()
    loadUserDetails()

def authenticate():
    """Authenticate user by username and password."""
    print("\nUser Authentication")
    username = input("Enter username: ")
    password = input("Enter password: ")

    for accNo, account in accounts.items():
        if account['username'] == username and account['password'] == password:
            return accNo

    print("Authentication failed. Invalid username or password.")
    return None


def depositMoney(accountNumber):
    """Deposit money into the account."""
    amount = positiveInput("Enter amount to deposit: ")
    accounts[accountNumber]['balance'] += amount
    accounts[accountNumber]['transactions'].append(f"Deposited {amount}")
    print(f"Deposit successful! New balance: {accounts[accountNumber]['balance']}")


def withdrawMoney(accountNumber):
    """Withdraw money from the account."""
    amount = positiveInput("Enter amount to withdraw: ")
    if amount > accounts[accountNumber]['balance']:
        print("Insufficient balance!")
    else:
        accounts[accountNumber]['balance'] -= amount
        accounts[accountNumber]['transactions'].append(f"Withdrew {amount}")
        print(f"Withdrawal successful! New balance: {accounts[accountNumber]['balance']}")


def checkBalance(accountNumber):
    """Check account balance."""
    print(f"Your current balance is {accounts[accountNumber]['balance']}.")


def transactionHistory(accountNumber):
    """Display transaction history."""
    print("Transaction History:")
    for transaction in accounts[accountNumber]['transactions']:
        print(transaction)


def saveUserDetails():
    """Save account details to a file."""
    with open("accounts.txt", "w") as file:
        for accNo, acc in accounts.items():
            file.write(f"Account Number: {accNo}\n")
            file.write(f"Name: {acc['name']}\n")
            file.write(f"Email: {acc['email']}\n")
            file.write(f"NIC: {acc['nic']}\n")
            file.write(f"Phone: {acc['phone']}\n")
            file.write(f"Username: {acc['username']}\n")
            file.write(f"Password: {acc['password']}\n")
            file.write(f"Balance: {acc['balance']}\n")
            file.write(f"Transactions: {', '.join(acc['transactions'])}\n\n")
    print("Accounts saved to file.")


def loadUserDetails():
    """Load account details from a file if it exists."""
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as file:
            lines = file.readlines()
            accData = {}
            accNo = None

            for line in lines:
                line = line.strip()
                if line.startswith("Account Number:"):
                    accNo = int(line.split(":")[1].strip())
                    accData[accNo] = {}
                elif line.startswith("Name:"):
                    accData[accNo]['name'] = line.split(":")[1].strip()
                elif line.startswith("Email:"):
                    accData[accNo]['email'] = line.split(":")[1].strip()
                elif line.startswith("NIC:"):
                    accData[accNo]['nic'] = line.split(":")[1].strip()
                elif line.startswith("Phone:"):
                    accData[accNo]['phone'] = line.split(":")[1].strip()
                elif line.startswith("Username:"):
                    accData[accNo]['username'] = line.split(":")[1].strip()
                elif line.startswith("Password:"):
                    accData[accNo]['password'] = line.split(":")[1].strip()
                elif line.startswith("Balance:"):
                    accData[accNo]['balance'] = float(line.split(":")[1].strip())
                elif line.startswith("Transactions:"):
                    accData[accNo]['transactions'] = line.split(":")[1].strip().split(", ")

            return accData
    return {}


def mainMenu():
    """Main interaction menu."""
    while True:
        print("\nMenu:")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            createNewAccount()
        elif choice == '2':
            accNo = authenticate()
            if accNo:
                depositMoney(accNo)
        elif choice == '3':
            accNo = authenticate()
            if accNo:
                withdrawMoney(accNo)
        elif choice == '4':
            accNo = authenticate()
            if accNo:
                checkBalance(accNo)
        elif choice == '5':
            accNo = authenticate()
            if accNo:
                transactionHistory(accNo)
        elif choice == '6':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice! Please try again.")


# Load data and start program
accounts = loadUserDetails()
mainMenu()
