import gradio as gr
from accounts import Account, get_share_price

# Initialize a single user account with an initial deposit
account = Account(user_id="user_1", initial_deposit=1000.0)

def create_account(user_id, initial_deposit):
    global account
    account = Account(user_id=user_id, initial_deposit=initial_deposit)
    return f"Account created for {user_id} with initial deposit of ${initial_deposit}"

def deposit_funds(amount):
    account.deposit(amount)
    return f"Deposited ${amount}. Current balance: ${account.balance}"

def withdraw_funds(amount):
    if account.withdraw(amount):
        return f"Withdrew ${amount}. Current balance: ${account.balance}"
    else:
        return f"Insufficient funds to withdraw ${amount}. Current balance: ${account.balance}"

def buy_shares(symbol, quantity):
    if account.buy_shares(symbol, quantity):
        return f"Bought {quantity} shares of {symbol}. Current balance: ${account.balance}"
    else:
        return f"Failed to buy {quantity} shares of {symbol}. Check your balance or share price."

def sell_shares(symbol, quantity):
    if account.sell_shares(symbol, quantity):
        return f"Sold {quantity} shares of {symbol}. Current balance: ${account.balance}"
    else:
        return f"Failed to sell {quantity} shares of {symbol}. Check your holdings."

def get_portfolio_value():
    return f"Total portfolio value: ${account.get_portfolio_value()}"

def get_profit_or_loss():
    return f"Profit/Loss: ${account.get_profit_or_loss()}"

def get_holdings():
    holdings = account.get_holdings()
    return f"Holdings: {holdings}"

def get_transactions():
    transactions = account.get_transactions()
    return f"Transactions: {transactions}"

with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        user_id = gr.Textbox(label="User ID")
        initial_deposit = gr.Number(label="Initial Deposit", value=1000)
        create_account_btn = gr.Button("Create Account")
        create_account_output = gr.Textbox(label="Create Account Output")
        
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_btn = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Deposit Output")
        
        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_btn = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Withdraw Output")
    
    with gr.Tab("Trading"):
        symbol_to_buy = gr.Textbox(label="Symbol to Buy")
        quantity_to_buy = gr.Number(label="Quantity to Buy")
        buy_btn = gr.Button("Buy Shares")
        buy_output = gr.Textbox(label="Buy Output")
        
        symbol_to_sell = gr.Textbox(label="Symbol to Sell")
        quantity_to_sell = gr.Number(label="Quantity to Sell")
        sell_btn = gr.Button("Sell Shares")
        sell_output = gr.Textbox(label="Sell Output")
    
    with gr.Tab("Reports"):
        portfolio_value_btn = gr.Button("Get Portfolio Value")
        portfolio_value_output = gr.Textbox(label="Portfolio Value")
        
        profit_loss_btn = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Profit/Loss")
        
        holdings_btn = gr.Button("Get Holdings")
        holdings_output = gr.Textbox(label="Holdings")
        
        transactions_btn = gr.Button("Get Transactions")
        transactions_output = gr.Textbox(label="Transactions")
    
    create_account_btn.click(fn=create_account, inputs=[user_id, initial_deposit], outputs=create_account_output)
    deposit_btn.click(fn=deposit_funds, inputs=deposit_amount, outputs=deposit_output)
    withdraw_btn.click(fn=withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    buy_btn.click(fn=buy_shares, inputs=[symbol_to_buy, quantity_to_buy], outputs=buy_output)
    sell_btn.click(fn=sell_shares, inputs=[symbol_to_sell, quantity_to_sell], outputs=sell_output)
    portfolio_value_btn.click(fn=get_portfolio_value, outputs=portfolio_value_output)
    profit_loss_btn.click(fn=get_profit_or_loss, outputs=profit_loss_output)
    holdings_btn.click(fn=get_holdings, outputs=holdings_output)
    transactions_btn.click(fn=get_transactions, outputs=transactions_output)

demo.launch()