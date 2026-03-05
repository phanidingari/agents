import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account('user123', 1000.0)

    def test_initial_deposit(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(self.account.transactions[-1], {'type': 'deposit', 'amount': 500.0})

    def test_withdraw_success(self):
        result = self.account.withdraw(300.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.transactions[-1], {'type': 'withdraw', 'amount': 300.0})

    def test_withdraw_failure(self):
        result = self.account.withdraw(1100.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_buy_shares_success(self):
        result = self.account.buy_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 250.0)  # 1000 - (5 * 150)
        self.assertEqual(self.account.holdings['AAPL'], 5)
        self.assertEqual(self.account.transactions[-1]['type'], 'buy')
        self.assertEqual(self.account.transactions[-1]['symbol'], 'AAPL')

    def test_buy_shares_failure(self):
        result = self.account.buy_shares('TSLA', 2)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertNotIn('TSLA', self.account.holdings)

    def test_sell_shares_success(self):
        self.account.buy_shares('AAPL', 5)
        result = self.account.sell_shares('AAPL', 3)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)  # After selling 3 AAPL at 150 each
        self.assertEqual(self.account.holdings['AAPL'], 2)
        self.assertEqual(self.account.transactions[-1]['type'], 'sell')
        self.assertEqual(self.account.transactions[-1]['symbol'], 'AAPL')

    def test_sell_shares_failure(self):
        result = self.account.sell_shares('AAPL', 3)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertNotIn('AAPL', self.account.holdings)

    def test_get_portfolio_value(self):
        self.account.buy_shares('AAPL', 5)
        portfolio_value = self.account.get_portfolio_value()
        self.assertAlmostEqual(portfolio_value, 1750.0)  # 250 balance + (5 * 150)

    def test_get_profit_or_loss(self):
        self.account.buy_shares('AAPL', 5)
        profit_or_loss = self.account.get_profit_or_loss()
        self.assertAlmostEqual(profit_or_loss, 750.0)  # 1750 portfolio value - 1000 initial deposit

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 5)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 5})

    def test_get_transactions(self):
        self.account.deposit(500.0)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0], {'type': 'deposit', 'amount': 500.0})

if __name__ == '__main__':
    unittest.main()