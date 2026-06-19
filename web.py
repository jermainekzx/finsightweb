from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf

from init_db import save_user, load_user, add_to_watchlist, get_watchlist
# setting up first attempt at the flask app
finsight = Flask(__name__)

# home page, to check if the app is working
@finsight.route('/')
def home():
    return "Finsight Ok"


# basic barebones health score
def health_score(de_ratio, current_ratio):
    if de_ratio < 1 and current_ratio > 1.5:
        return "LOW RISK"
    elif de_ratio < 2 and current_ratio > 1:
        return "MEDIUM RISK"
    else:
        return "HIGH RISK"

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
    # debt to equity ratio
    debt_to_equity = stock_info.get('debtToEquity', 'N/A')
    # current ratio
    current_ratio = stock_info.get('currentRatio', 'N/A')

    if debt_to_equity != 'N/A' and current_ratio != 'N/A':
        risk_assessment = health_score(debt_to_equity, current_ratio)

    else:
        risk_assessment = "N/A"

    return render_template('stock.html', ticker=ticker, price=pricedata, pe=pe_ratio, market_cap=market_cap, week_high=week_high, week_low=week_low, risk_assessment=risk_assessment)


# hardcoding and testing a screener functionality \
@finsight.route('/screener', methods=['GET', 'POST'])
def screener():
    # the hardcoded tickers will selected will be SG and US stocks for technology, finance, healthcare and energy
    all_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'JNJ', 'XOM', 'PFE', 'META', 'D05.SI', 'O39.SI', 'U11.SI', 'C6L.SI', 'Z74.SI', 'BN4.SI', 'A17U.SI', 'C38U.SI', 'S68U.SI', 'M44U.SI', 'G13U.SI']
    selected_sector = request.form.get('sector', '') # fallback
    selected_exchange = request.form.get('exchange', '') # fallback

    results = []
    for ticker in all_tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        info_sector = info.get('sector', 'N/A')
        info_currentPrice = info.get('currentPrice', 'N/A')
        info_marketCap = info.get('marketCap', 'N/A')

        if ticker.endswith('.SI'):
            exchange = 'SGX'
        else:
            exchange = 'US'

        if (selected_sector == '' or info_sector == selected_sector) and (selected_exchange == '' or exchange == selected_exchange):
            results.append({
                'ticker': ticker,
                'sector': info_sector,
                'exchange': exchange,
                'currentPrice': info_currentPrice,
                'marketCap': info_marketCap
            })
    return render_template('screener.html', results=results, selected_sector=selected_sector, selected_exchange=selected_exchange)

@finsight.route('/user/<int:user_id>/watchlist')
def view_watchlist(user_id):
    watchlist = get_watchlist(user_id)
    return render_template('watchlist.html', user_id=user_id, watchlist=watchlist)

@finsight.route('/user/<int:user_id>/watchlist/add/<ticker>', methods=['POST'])
def add_stock(user_id, ticker):
    add_to_watchlist(user_id, ticker)
    return redirect(url_for('view_watchlist', user_id=user_id))
    
# first trial to run
if __name__ == '__main__':
    finsight.run(debug=True)