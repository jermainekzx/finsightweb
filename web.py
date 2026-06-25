from flask import Flask, render_template, request, redirect, session, url_for
import yfinance as yf
import bcrypt

from init_db import save_user, load_user, get_password_hash, add_to_watchlist, get_watchlist, remove_from_watchlist
# setting up first attempt at the flask app
finsight = Flask(__name__)

# home page, to check if the app is working
@finsight.route('/')
def home():
    return render_template('home.html')

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
    
    ticker = ticker.upper()
    pulldata = yf.Ticker(ticker)
    try:
        stock_info = pulldata.info
        if not stock_info or ('longName' not in stock_info and 'shortName' not in stock_info):
            raise ValueError("Invalid ticker")
    except Exception as e:
        return f"Error: Invalid ticker '{ticker}'. {ticker} is not a valid stock ticker SGX or US stock symbol."

    pricedata = stock_info.get('currentPrice', 'N/A')
    pe_ratio = stock_info.get('trailingPE', 'N/A')
    market_cap = stock_info.get('marketCap', 'N/A')
    week_high = stock_info.get('fiftyTwoWeekHigh', 'N/A')
    week_low = stock_info.get('fiftyTwoWeekLow', 'N/A')
    debt_to_equity = stock_info.get('debtToEquity', 'N/A')
    current_ratio = stock_info.get('currentRatio', 'N/A')

    if debt_to_equity != 'N/A' and current_ratio != 'N/A':
        risk_assessment = health_score(debt_to_equity, current_ratio)
    else:
        risk_assessment = "N/A"

    return render_template('stock.html', ticker=ticker, price=pricedata, pe=pe_ratio, market_cap=market_cap, week_high=week_high, week_low=week_low, risk_assessment=risk_assessment)


@finsight.route('/screener', methods=['GET', 'POST'])
def screener():
    all_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'JNJ', 'XOM', 'PFE', 'META', 'D05.SI', 'O39.SI', 'U11.SI', 'C6L.SI', 'Z74.SI', 'BN4.SI', 'A17U.SI', 'C38U.SI', 'S68U.SI', 'M44U.SI', 'G13U.SI']
    selected_sector = request.form.get('sector', '')
    selected_exchange = request.form.get('exchange', '')

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


@finsight.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        save_user(username, password)
        return redirect(url_for('home'))
    return render_template('register.html')

@finsight.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        stored_hash = get_password_hash(username)
        if stored_hash:
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                print("Login successful!")
                return redirect(url_for('home'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@finsight.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip().upper()
        if ticker:
            return redirect(url_for('user_stock_profile', user_id=1, ticker=ticker))
    return render_template('search.html')

@finsight.route('/user/<int:user_id>/watchlist')
def view_watchlist(user_id):
    watchlist = get_watchlist(user_id)
    return render_template('watchlist.html', user_id=user_id, watchlist=watchlist)

@finsight.route('/user/<int:user_id>/watchlist/add/<ticker>', methods=['POST'])
def add_stock(user_id, ticker):
    add_to_watchlist(user_id, ticker)
    return redirect(url_for('view_watchlist', user_id=user_id))

@finsight.route('/user/<int:user_id>/watchlist/remove/<ticker>', methods=['POST'])
def remove_stock(user_id, ticker):
    remove_from_watchlist(user_id, ticker)
    return redirect(url_for('view_watchlist', user_id=user_id))

# first trial to run
if __name__ == '__main__':
    finsight.run(debug=True)