import tkinter as tk
from tkinter import messagebox, simpledialog

class InvalidAmountError(Exception):
    """
    Raised when a transaction amount is invalid (zero or negative).
    Used to validate deposit, withdraw, transfer, and top-up actions.
    """
    pass


class InsufficientFundsError(Exception):
    """
    Raised when an account balance is insufficient for the requested operation.
    Occurs during withdrawal, transfer, or mobile top-up attempts.
    """
    pass    

class BankAccount:
    """
    Represents a single bank account in the system, with basic financial operations.

    Attributes:
        acc_no (str): Unique account number.
        name (str): Account holder's name.
        password (str): User-defined password for login.
        acc_type (str): 'Personal' or 'Business' account type.
        balance (float): Current account balance.
        transactions (list): Log of all transactions performed.
    """

    def __init__(self, acc_no, name, password, acc_type, balance=0):
        """Initialize account details upon creation."""
        self.acc_no = acc_no
        self.name = name
        self.password = password
        self.acc_type = acc_type
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        """Add funds to account, recording transaction."""
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        self.balance += amount
        self.transactions.append(f"Deposited Nu.{amount}")

    def withdraw(self, amount):
        """Withdraw funds if sufficient, recording transaction."""
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Withdrew Nu.{amount}")

    def transfer(self, amount, target):
        """Transfer funds to another BankAccount."""
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        if target == self:
            raise InvalidAmountError("Cannot transfer to same account")
        self.balance -= amount
        target.balance += amount
        self.transactions.append(f"Sent Nu.{amount} to {target.name} (Acc: {target.acc_no})")
        target.transactions.append(f"Received Nu.{amount} from {self.name} (Acc: {self.acc_no})")

    def mobile_topup(self, amount, number):
        """Deduct funds for a mobile recharge and log transaction."""
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Mobile top-up Nu.{amount} to {number}")

    def get_transactions(self):
        """Retrieve the transaction history list."""
        return self.transactions


# -----------------------------
# BankingApp Class (Tkinter GUI)
# -----------------------------

class BankingApp:
    """
    The main banking GUI application class.

    Manages user sign-ups, logins, deposits, withdrawals, transfers, mobile top-ups,
    and transaction history display, all within a Tkinter-based interface.
    """

    def __init__(self, master):
        """Initialize the banking application window and account system."""
        self.master = master
        master.title("mBoB Bhutanese Banking App")
        self.accounts = {}   # Dictionary to store acc_no: BankAccount pairs
        self.current = None  # Tracks currently logged-in account
        self.main_menu()     # Load the home screen menu

    def main_menu(self):
        """Display the welcome screen with login, signup, and quit options."""
        for widget in self.master.winfo_children():
            widget.destroy()

        # Title and navigation buttons
        tk.Label(self.master, text="Welcome to Bhutanese mBoB Banking App", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.master, text="Login", width=20, command=self.login).pack(pady=5)
        tk.Button(self.master, text="Sign Up", width=20, command=self.sign_up).pack(pady=5)
        tk.Button(self.master, text="Quit", width=20, command=self.master.quit).pack(pady=5)

    def sign_up(self):
        """
        Prompt the user to create a new account.
        Requires an account number, name, account type, password, and opening balance.
        """
        acc_no = simpledialog.askstring("Sign Up", "Enter new account number:")
        if not acc_no:
            return
        if acc_no in self.accounts:
            messagebox.showerror("Error", "Account number already exists")
            return

        name = simpledialog.askstring("Sign Up", "Enter your name:")
        if not name:
            return

        acc_type = simpledialog.askstring("Sign Up", "Account Type (Personal/Business):")
        if not acc_type or acc_type.lower() not in ['personal', 'business']:
            messagebox.showerror("Error", "Invalid account type. Please enter Personal or Business.")
            return

        password = simpledialog.askstring("Sign Up", "Set your password:", show='*')
        if not password:
            return

        bal = simpledialog.askfloat("Sign Up", "Opening balance (Nu.):", minvalue=0)
        if bal is not None:
            self.accounts[acc_no] = BankAccount(acc_no, name, password, acc_type.capitalize(), bal)
            messagebox.showinfo("Success", f"{acc_type.capitalize()} account created for {name}\nAcc No: {acc_no}")

    def login(self):
        """
        Prompt user for login credentials and validate them.
        On successful login, displays account dashboard.
        """
        if not self.accounts:
            messagebox.showerror("Error", "No accounts available")
            return

        acc_no = simpledialog.askstring("Login", "Enter your account number:")
        if not acc_no or acc_no not in self.accounts:
            messagebox.showerror("Error", "Account not found")
            return

        password = simpledialog.askstring("Login", "Enter your password:", show='*')
        if password != self.accounts[acc_no].password:
            messagebox.showerror("Error", "Incorrect password")
            return

        self.current = self.accounts[acc_no]
        messagebox.showinfo("Success", f"Welcome {self.current.name}!")
        self.account_dashboard()

    def account_dashboard(self):
        """Display the main banking dashboard with available account operations."""
        for widget in self.master.winfo_children():
            widget.destroy()

        # Account info display
        tk.Label(self.master, text=f"{self.current.name}'s {self.current.acc_type} Account", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.master, text=f"Account Number: {self.current.acc_no}", font=("Arial", 12)).pack(pady=2)

        self.balance_label = tk.Label(self.master, text=f"Balance: Nu.{self.current.balance:.2f}")
        self.balance_label.pack()

        self.txn_text = tk.Text(self.master, height=8, width=45, state=tk.DISABLED)
        self.txn_text.pack(pady=5)
        self.update_display()

        # Action buttons
        tk.Button(self.master, text="Deposit", width=25, command=self.deposit).pack(pady=2)
        tk.Button(self.master, text="Withdraw", width=25, command=self.withdraw).pack(pady=2)
        tk.Button(self.master, text="Fund Transfer", width=25, command=self.transfer).pack(pady=2)
        tk.Button(self.master, text="Mobile Top-Up", width=25, command=self.mobile_topup).pack(pady=2)
        tk.Button(self.master, text="Logout", width=25, command=self.logout).pack(pady=10)

    def update_display(self):
        """Refresh the transaction history and account balance display."""
        self.balance_label.config(text=f"Balance: Nu.{self.current.balance:.2f}")
        self.txn_text.config(state=tk.NORMAL)
        self.txn_text.delete(1.0, tk.END)
        for t in self.current.transactions:
            self.txn_text.insert(tk.END, f"{t}\n")
        self.txn_text.config(state=tk.DISABLED)

    def deposit(self):
        """Prompt user to deposit money into their account."""
        amt = simpledialog.askfloat("Deposit", "Amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.deposit(amt)
                self.update_display()
                messagebox.showinfo("Success", f"Deposited Nu.{amt}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def withdraw(self):
        """Prompt user to withdraw money from their account."""
        amt = simpledialog.askfloat("Withdraw", "Amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.withdraw(amt)
                self.update_display()
                messagebox.showinfo("Success", f"Withdrew Nu.{amt}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def transfer(self):
        """Prompt user to transfer funds to another registered account."""
        if len(self.accounts) < 2:
            messagebox.showerror("Error", "Need at least 2 accounts")
            return

        target_acc = simpledialog.askstring("Fund Transfer", "Recipient's account number:")
        if not target_acc or target_acc not in self.accounts or target_acc == self.current.acc_no:
            messagebox.showerror("Error", "Invalid recipient")
            return

        amt = simpledialog.askfloat("Fund Transfer", "Amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.transfer(amt, self.accounts[target_acc])
                self.update_display()
                messagebox.showinfo("Success", f"Transferred Nu.{amt} to {target_acc}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def mobile_topup(self):
        """Prompt user for mobile number and top-up amount."""
        number = simpledialog.askstring("Mobile Top-Up", "Mobile number:")
        if number:
            amt = simpledialog.askfloat("Top-Up", "Amount (Nu.):", minvalue=0.01)
            if amt:
                try:
                    self.current.mobile_topup(amt, number)
                    self.update_display()
                    messagebox.showinfo("Success", f"Topped up Nu.{amt} to {number}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def logout(self):
        """Log out the current account and return to the main menu."""
        self.current = None
        self.main_menu()


# Run the banking application window
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()