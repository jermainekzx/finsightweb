from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf

from init_db import save_user, load_user
# setting up first attempt at the flask app
finsight = Flask(__name__)

# home page, to check if the app is working
@finsight.route('/')
def home():
    return "Finsight Ok"

@finsight.route('/user/<int:user_id>/stock/<ticker>')
def user_stock_profile(user_id, ticker):
    username_from_db = load_user(user_id)
    if username_from_db is None:
        username_from_db = "Guest User"
    
    # fetching data ticker
    pulldata = yf.Ticker(ticker)
    # getting stock info
    stock_info = pulldata.info

    # price data 
    pricedata = stock_info.get('currentPrice', 'N/A')
    # price to earnings
    pe_ratio = stock_info.get('trailingPE', 'N/A')
    # market cap
    market_cap = stock_info.get('marketCap', 'N/A')
    # weekly high
    week_high = stock_info.get('fiftyTwoWeekHigh', 'N/A')
    # weekly low
    week_low = stock_info.get('fiftyTwoWeekLow', 'N/A')

    return render_template('stock.html', ticker=ticker, price=pricedata, pe=pe_ratio, market_cap=market_cap, week_high=week_high, week_low=week_low)

# basic barebones health score
def health_score(de_ratio, current_ratio):
    if de_ratio < 1 and current_ratio > 1.5:
        return "LOW RISK"
    elif de_ratio < 2 and current_ratio > 1:
        return "MEDIUM RISK"
    else:
        return "HIGH RISK"
        
# first trial to run
if __name__ == '__main__':
    finsight.run(debug=True)
