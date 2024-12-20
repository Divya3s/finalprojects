from datetime import datetime
import json
import os

class BankAccount:
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        try:
            if amount > 0:
                self.balance += amount
                self.record_transaction("Deposit", amount)
                print(f"Deposited ${amount} into account {self.account_number}, Balance: ${self.balance}")
            else:
                print("Deposit must be positive.")
        except Exception as e:
            print(f"Error during deposit: {e}")

    def withdraw(self, amount):
        try:
            if 0 < amount <= self.balance:
                self.balance -= amount
                self.record_transaction("Withdrawl",amount)
                print(f"Withdrawl ${amount} into account {self.account_number}, balance: ${self.balance}")
            else:
                print("Insufficient Balance or invalid amount.")

        except Exception as e:
            print(f"Error during withdrawl: {e}")

    def transfer(self, target_account, amount):
        try:
            if 0 < amount <= self.balance:
                self.withdraw(amount)
                target_account.deposit(amount)
                print(f"Transferred ${amount} to account {target_account.account_number}.")
            else:
                print("Insufficient balance or invalid amount.")
        except Exception as e:
            print(f"Error during transfer: {e}")

    def record_transaction(self, transaction_type, amount):
        try:
            transaction = {
                "type": transaction_type,
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d%H:%M:%S")            
            }
            self.transactions.append(transaction)
        except Exception as e:
            print(f"Error during transaction:{e}")

    def show_transaction(self):
        try:
            print(f"Transaction History for Account {self.account_number}")
            for txn in self.transactions:
                print(f"{txn['date']} - {txn['type']}:${txn['amount']}")
        except Exception as e:
            print(f"Error during transaction:{e}")

    def to_dict(self):
        return{
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance,
            "transaction": self.transactions
        }

    @staticmethod
    def from_dict(data):
        account = BankAccount(data["account_number"], data["account_holder"], data["balance"])
        account.transactions = data["transactions"]
        return account

    def save_accounts(accounts, filename="account.json"):
        try:
            with open(filename, "w") as file:
                json.dump([acc.to_dict() for acc in accounts], file, indent = 4)
            print("Accounts saved successfully.")
        except Exception as e:
            print(f"Error saving accounts:{e}")


    def load_accounts(filename="account.json"):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    data = json.load(file)
                    return [BankAccount.from_dict for acc in data]

        except json.JSONDecodeError:
            print("Error reading the accounts file, corrupted.")
        except Exception as e:
            print(f"Error loading account:{e}")
        return []

    def create_account(accounts):
        try:
            account_number = input("Enter Account Number:")
            account_holder = input("Enter Account Holder Name:")
            new_account = BankAccount(account_number, account_holder)
            accounts.append(new_account)
            print("Account created Successfully.")
        except Exception as e:
            print(f"Error creating account:{e}")

    def main():
        accounts = load_accounts()

        while True:
            ptint("\n Banking Application")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transfer")
            print("5. Show Transactions")
            print("6. save and exit")

            choice = input("Choose the input option as 1 to 6:")

            if choice == "1":
                create_account(accounts)
            
            elif choice == "2":
                acc_number = input("Enter Account Number: ")
                account = next((acc for acc in accounts if acc.account_number == acc_number), None)
                if account:
                    try:
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    except ValueError:
                        print("Invalid input. Please enter a numeric value.")
                else:
                    print("Account not found.")
            
            elif choice == "3":
                acc_number = input("Enter Account Number: ")
                account = next((acc for acc in accounts if acc.account_number == acc_number), None)
                if account:
                    try:
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    except ValueError:
                        print("Invalid input. Please enter a numeric value.")
                else:
                    print("Account not found.")
            
            elif choice == "4":
                src_number = input("Enter Source Account Number: ")
                target_number = input("Enter Target Account Number: ")
                src_account = next((acc for acc in accounts if acc.account_number == src_number), None)
                target_account = next((acc for acc in accounts if acc.account_number == target_number),None)
                if src_account and target_account:
                    try:
                        amount = float(input("Enter amount to transfer: "))
                        src_account.transfer(target_account, amount)
                    except ValueError:
                        print("Invalid input. Please enter a numeric value.")
                else:
                    print("One or both accounts not found.")
            
            elif choice == "5":
                acc_number = input("Enter Account Number: ")
                account = next((acc for acc in accounts if acc.account_number == acc_number), None)
                if account:
                    account.show_transactions()
                else:
                    print("Account not found.")
            
            elif choice == "6":
                save_accounts(accounts)
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

    if __name__ == "__main__":
        main()
        
