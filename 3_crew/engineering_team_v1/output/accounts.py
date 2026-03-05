class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount})

    def withdraw(self, amount: float) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append({'type': 'withdraw', 'amount': amount})
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if total_cost <= self.balance:
            self.balance -= total_cost
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': share_price})
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            share_price = get_share_price(symbol)
            self.holdings[symbol] -= quantity
            self.balance += share_price * quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'price': share_price})
            return True
        return False

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        current_value = self.get_portfolio_value()
        return current_value - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transactions(self) -> list:
        return self.transactions

def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)