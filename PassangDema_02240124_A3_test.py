import unittest
from PassangDema_02240124_A3_PA import BankAccount, InvalidAmountError, InsufficientFundsError

# Replace 'your_banking_module' with the filename of your banking code, without the '.py' extension
# Example: from banking_app import BankAccount, InvalidAmountError, InsufficientFundsError


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Set up test accounts for each test"""
        self.acc1 = BankAccount("001", "Alice", "pass123", "Personal", 1000)
        self.acc2 = BankAccount("002", "Bob", "pass456", "Business", 500)

    # 1️⃣ Unusual user input

    def test_deposit_negative_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.deposit(-100)

    def test_withdraw_negative_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.withdraw(-50)

    def test_transfer_negative_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.transfer(-200, self.acc2)

    def test_mobile_topup_negative_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.mobile_topup(-20, "17123456")

    def test_transfer_to_self(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.transfer(100, self.acc1)

    # 2️⃣ Invalid usage of application functions

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc2.withdraw(1000)

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc2.transfer(1000, self.acc1)

    def test_mobile_topup_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc2.mobile_topup(600, "17123456")

    # 3️⃣ Testing individual main methods (deposit, withdraw, transfer, mobile_topup)

    def test_deposit_success(self):
        self.acc1.deposit(500)
        self.assertEqual(self.acc1.balance, 1500)

    def test_withdraw_success(self):
        self.acc1.withdraw(300)
        self.assertEqual(self.acc1.balance, 700)

    def test_transfer_success(self):
        self.acc1.transfer(200, self.acc2)
        self.assertEqual(self.acc1.balance, 800)
        self.assertEqual(self.acc2.balance, 700)

    def test_mobile_topup_success(self):
        self.acc1.mobile_topup(100, "17123456")
        self.assertEqual(self.acc1.balance, 900)

    # Optional: Test transactions record
    def test_transaction_history_recording(self):
        self.acc1.deposit(100)
        self.acc1.withdraw(50)
        self.assertIn("Deposited Nu.100", self.acc1.get_transactions())
        self.assertIn("Withdrew Nu.50", self.acc1.get_transactions())


if __name__ == "__main__":
    unittest.main()
# This code is a unit test suite for the BankAccount class, testing various scenarios including invalid inputs and successful operations.
#         self.master.title("Banking Application")