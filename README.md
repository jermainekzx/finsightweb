# Finsight - Equity Research, Simplified 
Team: John Luke Lim Kang & Jermaine  Khor | Orbital 2026 | Apollo 11 | Team 7666
Proposed level of achievement: Apollo 11

# Motivation behind the project
Investors and students in Singapore face a fragmented research experience. To screen stocks by fundamental metrics, view price history and assess financial health, a student analyst has to jump between multiple platforms. Most of which are either paywalled, US-centric or poorly suited to SGX-listed equities. This process has too many hoops, which unnecessarily complicates investing.

Professional tools like Bloomberg terminals and FactSet are inaccessible to most undergraduates. Free alternatives like Yahoo Finance lack the clean, focused interface that a student analyst actually needs. This fragmentation is a real barrier to making informed decisions during investment.

FinSight is built to close that gap, and our goal is a simple unified platform that brings together stock screening, fundamental data, price history, and a quantitative financial health indicator. This allows users, specifically student analysts, to develop rigorous, data-driven approaches to equity research without needing access to professional or pay-walled tools. 

# Aim
FinSight is a web application for students to research stocks listed on the Singapore Exchange (SGX) and US markets. Users can search for stocks, view clean price charts, and use a colour-coded Financial Health Score to assess whether a company is financially stable. Logged-in users can also maintain a personal watchlist to track stocks they are interested in.

# Features

- Stock Screener | As a beginner retail investor, I want to filter SGX and US-listed stocks by exchange, sector and market capitalisation so that I can identify companies that match my investment criteria without switching between multiple platforms. Data is fetched live via the yfinance API. This is the primary entry point for users who want to discover stocks matching specific criteria.
  
- Stock Detail Page | Each stock has a dedicated page showing its current price, price to earnings ratio, earnings per share (EPS), market cap, dividend yield, and 52-week high and low. Every metric has an explanation, making the platform accessible to beginners. Data will be fetched in real time via yfinance (Yahoo! Finance API)
  
- Personal Watchlist | Authenticated users can save stocks to a personal watchlist, add annotations and remove stocks. Watchlist data is stored in a database.

- Financial Health Score | A colour-coded risk indicator (Low, Medium and High) calculated from three financial ratios: debt-to-equity, current ratio and interest coverage ratio. The ratios are combined into a colour-coded Financial Health Score that helps users quickly identify potentially risky companies.

# Extension Features 

- Interactive Price Charts | Historical closing prices rendered using Chart.js over 1M, 3M and 1Y windows, where users are given the option to toggle between them.

- Stock search | A search bar that suggests stock tickers and company names, using live data

- Watchlist CSV Export | Logged-in users can download their watchlist as a CSV file for use in Excel and other tools.

# User Stories (potential use cases)
- As a beginner retail investor, I want to filter SGX and US-listed stocks by exchange, sector and market capitalisation so that I can narrow down my options without switching between multiple platforms.
  
- As a student analyst, I want to avoid financially distressed companies. I want to view a colour-coded financial health score for easy decision-making and to save time so that I can quickly assess risk before doing deeper research.

- As a user tracking multiple stocks who wants to stay organised, I want to create a personal account and save stocks to a watchlist so that I can efficiently check through my stock list.

- As a student learning about price movements, I want to view interactive historical price charts over different timeframes so that I can understand how a stock has performed over time.

# System Design

Finsight follows a standard three-tier web application architecture. The presentation layer consists of Jinja2 HTML templates rendered by Flask, with Chart.js handling interactive price charts on the client side. The application layer is built entirely in Python for simplicity using Flask, which handles all routing, logic and calculations.

The data layer consists of a SQLite database for storing user accounts and watchlists, and the yfinance API for fetching live and historical market data.

When a user visits a stock page, the browser first sends a GET request to the stock route. Flask matches the URL and calls the route function. The function fetches live data from yfinance using the ticker symbol. Relevant fields are extracted from the response dictionary using .get(). The Financial Health Score is computed from the ratio data. The score will then be displayed to the user. Flask passes all values to the stock template via render_template. Jinja2 then fills the placeholders and returns the finished HTML to the browser. 

The current database schema for Milestone 1 contains one table:

User table: id (int, primary key), username (txt, unique, and not null), password_hash (text, not null)

The database will have a Watchlist table added with the following columns: id (int, primary key), user_id (int, foreign key referencing user), ticker (txt, not null), note (txt).

# Tech Stack

Python 3 is the primary language for all backend logic, data processing and calculations, Flask is used as the web framework due to its lightweight nature, as FinSight does not require the full feature set of something like Django, and Flask's simplicity made it appropriate for myself and Jermaine as we are learning web development from scratch. Jinja 2 is Flask's built-in templating engine and allows Python variables to be rendered directly in HTML without needing a separate frontend framework. SQLite via Flask-SQLAlchemy provides the relational database layer. SQLite requires no separate database server, which makes local development and deployment straightforward. yfinance is an open source Python library that fetches live and historical data from Yahoo Finance, providing coverage of both SGX-listed and US-listed equities. Flask-Login handles user session management, login, logout and route protection. Chart.js is a JavaScript library for rendering interactive price charts entirely in the browser. Render is the cloud platform used for deployment, chosen for its free tier which is sufficient for Orbital evaluation, though we are open for changes whenever necessary.

# Software Engineering Practices

All development is managed on GitHub using a feature-branch workflow. The main branch contains only stable reviewed code. Features are developed on dedicated branches named descriptively and merged into a dev branch via pull request before being pushed to the main branch. This ensures that dysfunctional code and bugs never reach the stable branch and gives both Jermaine and I a chance to review each other's work before merging. 

Every feature and bug is tracked as a GitHub Issue with appropriate labels including feature, bug, documentation, backend, frontend, database and testing. Each issue is assigned to a team member and attached to the relevant Orbital milestone. Commit messages follow a consistent format describing what changed and why.

Backend logic is kept separate from frontend rendering. Route functions in app.py handle request logic and pass clean data to templates. Financial scoring logic will be extracted into a separate module. Database models are defined in models.py separately from application logic. Variables, functions and routes are named descriptively and inline comments are added, particularly in the financial health scoring calculation.

# Timeline and Development Plan

| S/N | Tasks | Description | In-Charge | Date |
| :---: | :--- | :--- | :---: | :---: |
| **1** | Finalise ideas | Design user interface layouts in Canva, sketch application features and core user flows. | Jermaine | 11 May - 15 May |
| | | Draft Liftoff presentation slides, compile the video script, and complete recording. | John | | 
| **2** | Preliminary research | Learn how Flask routing works and set up coding environment. | John <br> Jermaine | 16 May - 23 May |
| | | Test pulling live stock data from the yfinance API | John | |
| **3** | Database Initialization | Create the local SQLite database tables to store user profiles. | Jermaine | 24 May - 28 May |
| | | Code the database setup script to test saving and loading user data. | John | |
| **4** | UI & Code Integration | Connect the live yfinance data to our styled HTML frontend pages. | John <br> Jermaine | 29 May - 31 May |
| | | **Evaluation Milestone 1** <br> - Ideation <br> - Proof-of-concept: <br> &nbsp;&nbsp;&nbsp;&nbsp; - 1 hardcoded stock successfully pulling live market numbers. <br> &nbsp;&nbsp;&nbsp;&nbsp; - Local database file verifying it can save and load a test user profile. <br> &nbsp;&nbsp;&nbsp;&nbsp; - Clean web page showing our core design layouts and live price data | | **1 June** |
| **5** | Dynamic Stock Search | Build a search bar that lets users look up any SGX or US stock ticker. | Jermaine | 2 June - 5 June |
| | | Add checks so typing a wrong symbol or lowercase letters doesn't crash the app. | Jermaine | |
| **6** | Personal Watchlist | Create a database table so users can save their favorite stocks. | John | 6 June - 12 June |
| | | Code buttons to easily add, view notes on, or delete stocks from the list. | John | |
| **7** | User Authentication | Create secure registration and login pages for user accounts. | Jermaine | 13 June - 21 June |
| | | Use password hashing so user passwords aren't stored in plain text. | Jermaine | |
| **8** | Interactive Charts | Add a visual section for charts on the stock detail page. | Jermaine | 22 June - 28 June |
| | | Connect **Chart.js** to show 1-month, 3-month, and 1-year historical price graphs. | John | |
| | | **Evaluation Milestone 2** <br> - First Working Prototype <br> - Core Features Operational: <br> &nbsp;&nbsp;&nbsp;&nbsp; - Working stock search bar and user account login sessions. <br> &nbsp;&nbsp;&nbsp;&nbsp; - Personal watchlists that save data permanently to the database. <br> &nbsp;&nbsp;&nbsp;&nbsp; - Interactive price charts displaying stock performance over time. | | **29 June** |
| **9** | Financial Health Engine | Write the math formulas to pull key financial numbers from company reports. | Jermaine | 30 June - 5 July |
| | | Set up thresholds for Debt-to-Equity, Current, and Interest Coverage ratios. | John | |
| **10** | Stock Screener | Build an interactive table page for users to discover new stocks. | Jermaine | 6 July - 10 July |
| | | Allow users to filter the table by sector, exchange, P/E ratio, and market cap. | John | |
| **11** | CSV Export Extension | Write code to turn a user's watchlist into an Excel-friendly format. | Jermaine | 11 July - 17 July |
| | | Add a download button so users can save their watchlist as a `.csv` file. | Jermaine | |
| **12** | System Audits & Polish | Fix any loading lag and clean up database query speeds. | John <br> Jermaine | 18 July - 26 July |
| | | Run final testing to catch and fix any bugs before the official deployment. | John <br> Jermaine | |
| | | **Evaluation Milestone 3** <br> - Complete Minimum Viable Product (MVP) <br> - Final App Release: <br> &nbsp;&nbsp;&nbsp;&nbsp; - Working automated Financial Health Score (Low/Medium/High risk). <br> &nbsp;&nbsp;&nbsp;&nbsp; - Fully operational stock screener with advanced sorting filters. <br> &nbsp;&nbsp;&nbsp;&nbsp; - Watchlist export-to-CSV utility tool and finalized user interface. | | **27 July** |

# Project Log

Refer to the attached spreadsheet: [Project Log](https://docs.google.com/spreadsheets/d/1mq5sMYC5nBjxlFzbSaTtVvULrHvseNUHyRrKQJG9MPM/edit?usp=sharing)