"""
Test configuration for CS50 Finance application
"""

import os
import tempfile

# Test database configuration
TEST_DATABASE = tempfile.mktemp()

# Test user credentials
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"
TEST_INITIAL_CASH = 10000.00

# Test stock data
TEST_STOCK_DATA = {
    'AAPL': {
        'name': 'Apple Inc.',
        'symbol': 'AAPL',
        'price': 150.00
    },
    'MSFT': {
        'name': 'Microsoft Corporation',
        'symbol': 'MSFT',
        'price': 300.00
    },
    'GOOGL': {
        'name': 'Alphabet Inc.',
        'symbol': 'GOOGL',
        'price': 2500.00
    }
}

# Test scenarios
TEST_SCENARIOS = {
    'valid_purchase': {
        'symbol': 'AAPL',
        'shares': 10,
        'expected_cost': 1500.00
    },
    'insufficient_funds': {
        'symbol': 'GOOGL',
        'shares': 5,
        'expected_cost': 12500.00
    },
    'invalid_symbol': {
        'symbol': 'INVALID',
        'shares': 10
    },
    'invalid_shares': {
        'symbol': 'AAPL',
        'shares': 'abc'
    }
}
