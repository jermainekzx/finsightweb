from flask import Flask, render_template, request, redirect, session, url_for
import yfinance as yf
import bcrypt

from init_db import save_user, load_user, get_password_hash, add_to_watchlist, get_watchlist, remove_from_watchlist, get_user_id
# setting up first attempt at the flask app
finsight = Flask(__name__)
finsight.secret_key = 'finsight_secret_key' 

# home page, to check if the app is working
@finsight.route('/')
def home():
    return render_template('home.html')

# updated health score, including interest coverage ratio and current ratio, to assess the financial health of a stock
def health_score(de_ratio, current_ratio, interest_coverage):
    if de_ratio < 1 and current_ratio > 1.5 and interest_coverage > 3:
        return "LOW RISK"
    elif de_ratio < 2 and current_ratio > 1 and interest_coverage > 2:
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
    ebit = stock_info.get('ebitda', 'N/A')
    interest_expense = stock_info.get('interestExpense', 'N/A')

    # work out interest coverage ratio if we have both numbers
    # skip it if interest expense is 0 since we cant divide by 0
    if ebit != 'N/A' and interest_expense != 'N/A' and interest_expense != 0:
        interest_coverage = ebit / abs(interest_expense)
    else:
        interest_coverage = 'N/A'

    # only calculate a risk score if all 3 ratios are available
    if debt_to_equity != 'N/A' and current_ratio != 'N/A' and interest_coverage != 'N/A':
        risk_assessment = health_score(debt_to_equity, current_ratio, interest_coverage)
    else:
        risk_assessment = "N/A"
    
    chosen_period = request.args.get('period', '1mo')
    if chosen_period not in ['1mo', '3mo', '1y']:
        chosen_period = '1mo'

    hist = pulldata.history(period=chosen_period)
    chart_dates = [str(d.date()) for d in hist.index]
    chart_prices = [round(float(p), 2) for p in hist['Close']]

    return render_template('stock.html', ticker=ticker, price=pricedata, pe=pe_ratio, market_cap=market_cap, week_high=week_high, week_low=week_low, risk_assessment=risk_assessment, user_id=user_id, user_name=username_from_db, chart_dates=chart_dates, chart_prices=chart_prices)


@finsight.route('/screener', methods=['GET', 'POST'])
def screener():
    all_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'JNJ', 'XOM', 'PFE', 'META', 'D05.SI', 'O39.SI', 'U11.SI', 'C6L.SI', 'Z74.SI', 'BN4.SI', 'A17U.SI', 'C38U.SI', 'S68U.SI', 'M44U.SI', 'G13U.SI']
    selected_sector = request.form.get('sector', '')
    selected_exchange = request.form.get('exchange', '')
    selected_pe_min = request.form.get('pe_min', '')
    selected_pe_max = request.form.get('pe_max', '')
    selected_mcap_min = request.form.get('mcap_min', '')
    selected_mcap_max = request.form.get('mcap_max', '')

    # turn the form values into numbers, blank means no filter on that side
    pe_min = float(selected_pe_min) if selected_pe_min else None
    pe_max = float(selected_pe_max) if selected_pe_max else None
    mcap_min = float(selected_mcap_min) if selected_mcap_min else None
    mcap_max = float(selected_mcap_max) if selected_mcap_max else None

    results = []
    for ticker in all_tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        info_sector = info.get('sector', 'N/A')
        info_currentPrice = info.get('currentPrice', 'N/A')
        info_marketCap = info.get('marketCap', 'N/A')
        info_pe = info.get('trailingPE', 'N/A')

        if ticker.endswith('.SI'):
            exchange = 'SGX'
        else:
            exchange = 'US'

        # start assuming it passes, then rule it out if it fails any filter
        include_stock = True

        if selected_sector != '' and info_sector != selected_sector:
            include_stock = False

        if selected_exchange != '' and exchange != selected_exchange:
            include_stock = False

        # only check pe if a pe filter was actually set
        if pe_min is not None or pe_max is not None:
            if info_pe == 'N/A':
                include_stock = False
            elif pe_min is not None and info_pe < pe_min:
                include_stock = False
            elif pe_max is not None and info_pe > pe_max:
                include_stock = False

        # same for market cap
        if mcap_min is not None or mcap_max is not None:
            if info_marketCap == 'N/A':
                include_stock = False
            elif mcap_min is not None and info_marketCap < mcap_min:
                include_stock = False
            elif mcap_max is not None and info_marketCap > mcap_max:
                include_stock = False

        if include_stock:
            results.append({
                'ticker': ticker,
                'sector': info_sector,
                'exchange': exchange,
                'currentPrice': info_currentPrice,
                'marketCap': info_marketCap,
                'pe': info_pe
            })

    return render_template('screener.html', results=results, selected_sector=selected_sector, selected_exchange=selected_exchange, selected_pe_min=selected_pe_min, selected_pe_max=selected_pe_max, selected_mcap_min=selected_mcap_min, selected_mcap_max=selected_mcap_max)

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
        if stored_hash and bcrypt.checkpw(password.encode(), stored_hash.encode()):
                user_id = get_user_id(username)
                session['user_id'] = user_id
                session['username'] = username

                print("Login successful!")
                return redirect(url_for('view_watchlist', user_id=user_id))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@finsight.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip().upper()
        if ticker:
            active_user_id = session.get('user_id', 0) 
            return redirect(url_for('user_stock_profile', user_id=active_user_id, ticker=ticker))
    return render_template('search.html')

@finsight.route('/user/<int:user_id>/watchlist')
def view_watchlist(user_id):
    watchlist = get_watchlist(user_id)
    return render_template('watchlist.html', user_id=user_id, watchlist=watchlist)

@finsight.route('/user/<int:user_id>/watchlist/add', methods=['POST'])
def add_stock(user_id):
    ticker = request.form.get('ticker', '').strip().upper()
    if ticker:
        add_to_watchlist(user_id, ticker)
    return redirect(url_for('view_watchlist', user_id=user_id))

@finsight.route('/user/<int:user_id>/watchlist/remove/<ticker>', methods=['POST'])
def remove_stock(user_id, ticker):
    remove_from_watchlist(user_id, ticker)
    return redirect(url_for('view_watchlist', user_id=user_id))

@finsight.route('/logout')
def logout():
    session.clear() 
    print("User logged out successfully.")
    return redirect(url_for('home'))


# first trial to run
if __name__ == '__main__':
    finsight.run(debug=True)