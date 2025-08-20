import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from helpers import lookup, usd
from cs50 import SQL


class TestFinanceApp(unittest.TestCase):
    """Test cases for CS50 Finance application"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Create a temporary database for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Store original database connection
        import app as app_module
        self.original_db = app_module.db
        
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['DATABASE'] = self.db_path
        self.app = app.test_client()
        
        # Create test database schema
        self.db = SQL(f"sqlite:///{self.db_path}")
        self.create_test_schema()
        
        # Create test user
        self.test_user_id = self.create_test_user()
        
        # Patch the app's database to use test database
        app_module.db = self.db
    
    def tearDown(self):
        """Clean up after each test"""
        # Restore original database connection
        import app as app_module
        app_module.db = self.original_db
        
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def create_test_schema(self):
        """Create test database schema"""
        self.db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT NOT NULL,
                hash TEXT NOT NULL,
                cash NUMERIC NOT NULL DEFAULT 10000.00
            )
        """)
        
        self.db.execute("""
            CREATE TABLE actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                symbol TEXT NOT NULL,
                shares INTEGER NOT NULL,
                price NUMERIC NOT NULL,
                total_amount NUMERIC NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        
        self.db.execute("""
            CREATE TABLE assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                shares INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                UNIQUE(user_id, symbol)
            )
        """)
    
    def create_test_user(self):
        """Create a test user and return user ID"""
        from werkzeug.security import generate_password_hash
        
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", generate_password_hash("testpass"), 10000.00
        )
        
        result = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")
        return result[0]["id"]
    
    def login_test_user(self):
        """Helper method to login test user"""
        with self.app.session_transaction() as sess:
            sess['user_id'] = self.test_user_id
    
    def test_buy_stock_initial_lookup(self):
        """Test initial stock lookup step"""
        self.login_test_user()
        
        # Test GET request to buy page
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Buy Shares', response.data)
        self.assertIn(b'Look Up Stock', response.data)
    
    def test_buy_stock_invalid_symbol(self):
        """Test buying with invalid stock symbol"""
        self.login_test_user()
        
        response = self.app.post('/buy', data={
            'symbol': 'INVALID',
            'shares': '10'
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_buy_stock_invalid_shares(self):
        """Test buying with invalid number of shares"""
        self.login_test_user()
        
        # Test with non-numeric shares
        response = self.app.post('/buy', data={
            'symbol': 'AAPL',
            'shares': 'abc'
        })
        
        self.assertEqual(response.status_code, 400)
        
        # Test with zero shares
        response = self.app.post('/buy', data={
            'symbol': 'AAPL',
            'shares': '0'
        })
        
        self.assertEqual(response.status_code, 400)
        
        # Test with negative shares
        response = self.app.post('/buy', data={
            'symbol': 'AAPL',
            'shares': '-5'
        })
        
        self.assertEqual(response.status_code, 400)
    
    @patch('app.lookup')
    def test_buy_stock_successful_lookup(self, mock_lookup):
        """Test successful stock lookup"""
        self.login_test_user()
        
        # Mock lookup function to return test stock data
        mock_lookup.return_value = {
            'name': 'Apple Inc.',
            'symbol': 'AAPL',
            'price': 150.00
        }
        
        response = self.app.post('/buy', data={
            'symbol': 'AAPL',
            'shares': '10'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Apple Inc.', response.data)
        self.assertIn(b'AAPL', response.data)
        self.assertIn(b'$1,500.00', response.data)  # 10 * $150.00
    
    @patch('app.lookup')
    def test_buy_stock_insufficient_funds(self, mock_lookup):
        """Test buying when user has insufficient funds"""
        self.login_test_user()
        
        # Mock lookup function to return expensive stock
        mock_lookup.return_value = {
            'name': 'Expensive Stock',
            'symbol': 'EXP',
            'price': 20000.00  # Very expensive
        }
        
        response = self.app.post('/buy', data={
            'symbol': 'EXP',
            'shares': '1'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Insufficient funds', response.data)
    
    @patch('app.lookup')
    def test_buy_stock_database_operations(self, mock_lookup):
        """Test database operations during stock purchase"""
        # This test would require more complex setup and mocking
        # to test actual database operations
        pass
    
    def test_index_page_requires_login(self):
        """Test that index page requires login"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    @patch('app.lookup')
    def test_index_page_with_stocks(self, mock_lookup):
        """Test index page displays portfolio correctly"""
        self.login_test_user()
        
        # Mock lookup function
        mock_lookup.return_value = {
            'name': 'Apple Inc.',
            'symbol': 'AAPL',
            'price': 150.00
        }
        
        # Create test assets
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, self.test_user_id, "AAPL", 10)
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AAPL', response.data)
        self.assertIn(b'Apple Inc.', response.data)
        self.assertIn(b'10', response.data)
        self.assertIn(b'$1,500.00', response.data)  # 10 * $150.00
    
    @patch('app.lookup')
    def test_index_page_no_stocks(self, mock_lookup):
        """Test index page when user has no stocks"""
        self.login_test_user()
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No stocks owned yet', response.data)
        self.assertIn(b'$10,000.00', response.data)  # Initial cash
    
    def test_sell_page_requires_login(self):
        """Test that sell page requires login"""
        response = self.app.get('/sell')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_sell_page_no_stocks(self):
        """Test sell page when user has no stocks to sell"""
        self.login_test_user()
        
        response = self.app.get('/sell')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You don't own any stocks to sell", response.data)
        self.assertIn(b'Buy Some Stocks', response.data)
    
    def test_sell_page_with_stocks(self):
        """Test sell page displays available stocks"""
        self.login_test_user()
        
        # Create test assets
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, self.test_user_id, "AAPL", 10)
        
        response = self.app.get('/sell')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select Stock', response.data)
        self.assertIn(b'AAPL', response.data)
    
    def test_sell_stock_invalid_symbol(self):
        """Test selling with invalid stock symbol"""
        self.login_test_user()
        
        response = self.app.post('/sell', data={
            'symbol': 'INVALID',
            'shares': '5'
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_sell_stock_invalid_shares(self):
        """Test selling with invalid number of shares"""
        self.login_test_user()
        
        # Create test assets
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, self.test_user_id, "AAPL", 10)
        
        # Test with non-numeric shares
        response = self.app.post('/sell', data={
            'symbol': 'AAPL',
            'shares': 'abc'
        })
        
        self.assertEqual(response.status_code, 400)
        
        # Test with zero shares
        response = self.app.post('/sell', data={
            'symbol': 'AAPL',
            'shares': '0'
        })
        
        self.assertEqual(response.status_code, 400)
        
        # Test with negative shares
        response = self.app.post('/sell', data={
            'symbol': 'AAPL',
            'shares': '-5'
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_sell_stock_not_owned(self):
        """Test selling stock user doesn't own"""
        self.login_test_user()
        
        response = self.app.post('/sell', data={
            'symbol': 'GOOGL',
            'shares': '5'
        })
        
        self.assertEqual(response.status_code, 400)
    
    def test_sell_stock_insufficient_shares(self):
        """Test selling more shares than user owns"""
        self.login_test_user()
        
        # Create test assets
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, self.test_user_id, "AAPL", 10)
        
        response = self.app.post('/sell', data={
            'symbol': 'AAPL',
            'shares': '15'
        })
        
        self.assertEqual(response.status_code, 400)
    
    @patch('app.lookup')
    def test_sell_stock_successful(self, mock_lookup):
        """Test successful stock sale"""
        self.login_test_user()
        
        # Mock lookup function
        mock_lookup.return_value = {
            'name': 'Apple Inc.',
            'symbol': 'AAPL',
            'price': 150.00
        }
        
        # Create test assets
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, self.test_user_id, "AAPL", 10)
        
        # Get initial cash
        initial_cash = self.db.execute("SELECT cash FROM users WHERE id = ?", self.test_user_id)[0]["cash"]
        
        response = self.app.post('/sell', data={
            'symbol': 'AAPL',
            'shares': '5'
        })
        
        # Should redirect to index
        self.assertEqual(response.status_code, 302)
        
        # Check that shares were reduced
        remaining_shares = self.db.execute("SELECT shares FROM assets WHERE user_id = ? AND symbol = ?", 
                                         self.test_user_id, "AAPL")[0]["shares"]
        self.assertEqual(remaining_shares, 5)
        
        # Check that cash was increased
        new_cash = self.db.execute("SELECT cash FROM users WHERE id = ?", self.test_user_id)[0]["cash"]
        self.assertEqual(new_cash, initial_cash + (5 * 150.00))
        
        # Check that action was recorded
        actions = self.db.execute("SELECT * FROM actions WHERE user_id = ? AND action = 'sell'", self.test_user_id)
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["symbol"], "AAPL")
        self.assertEqual(actions[0]["shares"], 5)
    
    @patch('app.lookup')
    def test_sell_all_shares(self, mock_lookup):
        """Test selling all shares of a stock"""
        self.login_test_user()
        
        # Mock lookup function
        mock_lookup.return_value = {
            'name': 'Apple Inc.',
            'symbol': 'AAPL',
            'price': 150.00
        }
        
        # Create test assets
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, self.test_user_id, "AAPL", 10)
        
        response = self.app.post('/sell', data={
            'symbol': 'AAPL',
            'shares': '10'
        })
        
        # Should redirect to index
        self.assertEqual(response.status_code, 302)
        
        # Check that asset was removed (since all shares sold)
        assets = self.db.execute("SELECT * FROM assets WHERE user_id = ? AND symbol = ?", 
                                self.test_user_id, "AAPL")
        self.assertEqual(len(assets), 0)
    
    def test_history_page_requires_login(self):
        """Test that history page requires login"""
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_history_page_with_transactions(self):
        """Test history page displays transactions"""
        self.login_test_user()
        
        # Create test actions
        self.db.execute("""
            INSERT INTO actions (user_id, action, symbol, shares, price, total_amount) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, self.test_user_id, "buy", "AAPL", 10, 150.00, 1500.00)
        
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AAPL', response.data)
        self.assertIn(b'buy', response.data)
        self.assertIn(b'10', response.data)
    
    def test_helpers_lookup_function(self):
        """Test the lookup helper function"""
        # Test with a valid symbol (this will make actual API call)
        # In production, you might want to mock this
        pass
    
    def test_helpers_usd_function(self):
        """Test the USD formatting helper function"""
        self.assertEqual(usd(1234.56), "$1,234.56")
        self.assertEqual(usd(0), "$0.00")
        self.assertEqual(usd(1000000), "$1,000,000.00")


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations specifically"""
    
    def setUp(self):
        """Set up test database"""
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.db = SQL(f"sqlite:///{self.db_path}")
        self.create_test_schema()
    
    def tearDown(self):
        """Clean up test database"""
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def create_test_schema(self):
        """Create test database schema"""
        self.db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT NOT NULL,
                hash TEXT NOT NULL,
                cash NUMERIC NOT NULL DEFAULT 10000.00
            )
        """)
        
        self.db.execute("""
            CREATE TABLE actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                symbol TEXT NOT NULL,
                shares INTEGER NOT NULL,
                price NUMERIC NOT NULL,
                total_amount NUMERIC NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        
        self.db.execute("""
            CREATE TABLE assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                shares INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                UNIQUE(user_id, symbol)
            )
        """)
    
    def test_user_cash_update(self):
        """Test updating user cash after purchase"""
        # Create test user
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", "hash", 10000.00
        )
        
        user_id = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")[0]["id"]
        
        # Simulate cash deduction
        purchase_amount = 1500.00
        self.db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", purchase_amount, user_id)
        
        # Check cash was deducted
        remaining_cash = self.db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        self.assertEqual(remaining_cash, 8500.00)
    
    def test_actions_table_insert(self):
        """Test inserting into actions table"""
        # Create test user
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", "hash", 10000.00
        )
        
        user_id = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")[0]["id"]
        
        # Insert test action
        self.db.execute("""
            INSERT INTO actions (user_id, action, symbol, shares, price, total_amount) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, user_id, "buy", "AAPL", 10, 150.00, 1500.00)
        
        # Check action was inserted
        actions = self.db.execute("SELECT * FROM actions WHERE user_id = ?", user_id)
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["symbol"], "AAPL")
        self.assertEqual(actions[0]["shares"], 10)
    
    def test_assets_table_update(self):
        """Test updating assets table"""
        # Create test user
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", "hash", 10000.00
        )
        
        user_id = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")[0]["id"]
        
        # Insert initial asset
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, user_id, "AAPL", 10)
        
        # Update asset shares (simulate buying more)
        self.db.execute("""
            UPDATE assets SET shares = shares + ? 
            WHERE user_id = ? AND symbol = ?
        """, 5, user_id, "AAPL")
        
        # Check shares were updated
        asset = self.db.execute("SELECT shares FROM assets WHERE user_id = ? AND symbol = ?", user_id, "AAPL")[0]
        self.assertEqual(asset["shares"], 15)
    
    def test_assets_table_delete_when_all_sold(self):
        """Test removing asset when all shares are sold"""
        # Create test user
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", "hash", 10000.00
        )
        
        user_id = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")[0]["id"]
        
        # Insert asset
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, user_id, "AAPL", 10)
        
        # Delete asset (simulate selling all shares)
        self.db.execute("""
            DELETE FROM assets 
            WHERE user_id = ? AND symbol = ?
        """, user_id, "AAPL")
        
        # Check asset was removed
        assets = self.db.execute("SELECT * FROM assets WHERE user_id = ? AND symbol = ?", user_id, "AAPL")
        self.assertEqual(len(assets), 0)
    
    def test_sell_transaction_recording(self):
        """Test recording sell transactions in actions table"""
        # Create test user
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", "hash", 10000.00
        )
        
        user_id = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")[0]["id"]
        
        # Insert sell action
        self.db.execute("""
            INSERT INTO actions (user_id, action, symbol, shares, price, total_amount) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, user_id, "sell", "AAPL", 5, 150.00, 750.00)
        
        # Check sell action was recorded
        actions = self.db.execute("SELECT * FROM actions WHERE user_id = ? AND action = 'sell'", user_id)
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["symbol"], "AAPL")
        self.assertEqual(actions[0]["shares"], 5)
        self.assertEqual(actions[0]["price"], 150.00)
        self.assertEqual(actions[0]["total_amount"], 750.00)
    
    def test_portfolio_calculation(self):
        """Test portfolio value calculation"""
        # Create test user
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", "hash", 10000.00
        )
        
        user_id = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")[0]["id"]
        
        # Insert multiple assets
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, user_id, "AAPL", 10)
        
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, user_id, "GOOGL", 5)
        
        # Get portfolio
        assets = self.db.execute("SELECT symbol, shares FROM assets WHERE user_id = ?", user_id)
        
        # Simulate current prices (in real app, this would come from lookup function)
        prices = {"AAPL": 150.00, "GOOGL": 2800.00}
        
        total_value = 0
        for asset in assets:
            total_value += asset["shares"] * prices[asset["symbol"]]
        
        # Check calculation
        expected_value = (10 * 150.00) + (5 * 2800.00)  # 1500 + 14000 = 15500
        self.assertEqual(total_value, expected_value)
    
    def test_user_cash_after_sell(self):
        """Test user cash increases after selling stocks"""
        # Create test user
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", "hash", 10000.00
        )
        
        user_id = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")[0]["id"]
        
        initial_cash = 10000.00
        sell_amount = 750.00
        
        # Simulate cash increase from selling
        self.db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sell_amount, user_id)
        
        # Check cash was increased
        new_cash = self.db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        self.assertEqual(new_cash, initial_cash + sell_amount)
    
    def test_assets_table_unique_constraint(self):
        """Test that assets table enforces unique constraint on user_id + symbol"""
        # Create test user
        self.db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
            "testuser", "hash", 10000.00
        )
        
        user_id = self.db.execute("SELECT id FROM users WHERE username = ?", "testuser")[0]["id"]
        
        # Insert first asset
        self.db.execute("""
            INSERT INTO assets (user_id, symbol, shares) 
            VALUES (?, ?, ?)
        """, user_id, "AAPL", 10)
        
        # Try to insert duplicate (should fail due to unique constraint)
        try:
            self.db.execute("""
                INSERT INTO assets (user_id, symbol, shares) 
                VALUES (?, ?, ?)
            """, user_id, "AAPL", 5)
            self.fail("Should have raised an exception for duplicate key")
        except Exception:
            # Expected behavior - duplicate key should be rejected
            pass
        
        # Check only one asset record exists
        assets = self.db.execute("SELECT * FROM assets WHERE user_id = ? AND symbol = ?", user_id, "AAPL")
        self.assertEqual(len(assets), 1)
        self.assertEqual(assets[0]["shares"], 10)


if __name__ == '__main__':
    unittest.main()
