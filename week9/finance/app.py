import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get user's current cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    
    # Get user's current assets
    assets = db.execute("SELECT symbol, shares FROM assets WHERE user_id = ?", session["user_id"])
    
    # Calculate current values for each stock
    portfolio = []
    total_stocks_value = 0
    
    for asset in assets:
        # Look up current stock price
        stock = lookup(asset["symbol"])
        if stock:
            current_value = stock["price"] * asset["shares"]
            total_stocks_value += current_value
            
            portfolio.append({
                "symbol": asset["symbol"],
                "name": stock["name"],
                "shares": asset["shares"],
                "price": stock["price"],
                "total_value": current_value
            })
    
    # Calculate grand total
    grand_total = user_cash + total_stocks_value
    
    return render_template("index.html", portfolio=portfolio, user_cash=user_cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        confirm = request.form.get("confirm")
        
        # Step 1: Look up stock and show confirmation
        if not confirm:
            # Validate input
            if not symbol:
                return apology("must provide symbol", 400)
            if not shares or not shares.isdigit() or int(shares) <= 0:
                return apology("must provide valid number of shares", 400)
            
            shares = int(shares)
            
            # Look up stock
            stock = lookup(symbol)
            if not stock:
                return apology("invalid symbol", 400)
            
            # Get user's current cash
            user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
            total_cost = stock["price"] * shares
            
            # Show confirmation page
            return render_template("buy.html", stock=stock, shares=shares, user_cash=user_cash, total_cost=total_cost)
        
        # Step 2: Confirm purchase
        else:
            # Validate input again
            if not symbol:
                return apology("must provide symbol", 400)
            if not shares or not shares.isdigit() or int(shares) <= 0:
                return apology("must provide valid number of shares", 400)
            
            shares = int(shares)
            
            # Look up stock again to get current price
            stock = lookup(symbol)
            if not stock:
                return apology("invalid symbol", 400)
            
            # Get user's current cash
            user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
            
            # Check if user has enough cash
            total_cost = stock["price"] * shares
            if user_cash < total_cost:
                return apology("insufficient funds", 400)
            
            # Update user's cash
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
            
            # Insert into actions table
            db.execute("INSERT INTO actions (user_id, action, symbol, shares, price, total_amount) VALUES (?, ?, ?, ?, ?, ?)", 
                       session["user_id"], "buy", stock["symbol"], shares, stock["price"], total_cost)
            
            # Update assets table
            # Check if user already owns this stock
            existing_asset = db.execute("SELECT shares FROM assets WHERE user_id = ? AND symbol = ?", 
                                       session["user_id"], stock["symbol"])
            
            if existing_asset:
                # Update existing shares
                db.execute("UPDATE assets SET shares = shares + ? WHERE user_id = ? AND symbol = ?", 
                           shares, session["user_id"], stock["symbol"])
            else:
                # Insert new asset
                db.execute("INSERT INTO assets (user_id, symbol, shares) VALUES (?, ?, ?)", 
                           session["user_id"], stock["symbol"], shares)
            
            flash(f"Successfully bought {shares} shares of {stock['symbol']} at {usd(stock['price'])} per share")

            return redirect("/")
        
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # 只需要 GET 方法
    # 从数据库查询用户的交易记录
    transactions = db.execute("""
        SELECT * FROM actions 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    """, session["user_id"])
    
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if stock:
            return render_template("quoted.html", stock=stock)
        else:
            return apology("invalid symbol", 400)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            return apology("passwords do not match", 403)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        # Validate input
        if not symbol:
            return apology("must select a stock", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide valid number of shares", 400)
        
        shares = int(shares)
        
        # Check if user owns this stock and has enough shares
        user_asset = db.execute("SELECT shares FROM assets WHERE user_id = ? AND symbol = ?", 
                               session["user_id"], symbol)
        
        if not user_asset:
            return apology("you don't own this stock", 400)
        
        if user_asset[0]["shares"] < shares:
            return apology("you don't own enough shares", 400)
        
        # Look up current stock price
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)
        
        # Calculate total sale amount
        total_amount = stock["price"] * shares
        
        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_amount, session["user_id"])
        
        # Insert into actions table
        db.execute("INSERT INTO actions (user_id, action, symbol, shares, price, total_amount) VALUES (?, ?, ?, ?, ?, ?)", 
                   session["user_id"], "sell", stock["symbol"], shares, stock["price"], total_amount)
        
        # Update assets table
        if user_asset[0]["shares"] == shares:
            # If selling all shares, remove the asset
            db.execute("DELETE FROM assets WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        else:
            # If selling some shares, update the remaining shares
            db.execute("UPDATE assets SET shares = shares - ? WHERE user_id = ? AND symbol = ?", 
                       shares, session["user_id"], symbol)
        
        flash(f"Successfully sold {shares} shares of {stock['symbol']} at {usd(stock['price'])} per share")
        
        return redirect("/")
    
    else:
        # Get user's current stocks for the dropdown
        user_stocks = db.execute("SELECT symbol FROM assets WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", user_stocks=user_stocks)



if __name__ == "__main__":
    app.run(debug=True)

