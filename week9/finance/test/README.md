# CS50 Finance Test Suite

This directory contains comprehensive unit tests for the CS50 Finance application.

## Test Structure

### `test_app.py`
Main test file containing:
- **TestFinanceApp**: Tests for the main application functionality
- **TestDatabaseOperations**: Tests for database operations

### `test_config.py`
Test configuration and test data constants

### `run_tests.py`
Test runner script for executing all tests

## Running Tests

### Option 1: Run all tests
```bash
cd week9/finance
python test/run_tests.py
```

### Option 2: Run specific test file
```bash
cd week9/finance
python -m unittest test.test_app -v
```

### Option 3: Run specific test class
```bash
cd week9/finance
python -m unittest test.test_app.TestFinanceApp -v
```

### Option 4: Run specific test method
```bash
cd week9/finance
python -m unittest test.test_app.TestFinanceApp.test_buy_stock_successful_lookup -v
```

## Test Coverage

### Application Tests (`TestFinanceApp`)
- ✅ Initial buy page rendering
- ✅ Invalid stock symbol handling
- ✅ Invalid shares input validation
- ✅ Successful stock lookup
- ✅ Insufficient funds handling
- ✅ Helper functions (USD formatting)

### Database Tests (`TestDatabaseOperations`)
- ✅ User cash updates
- ✅ Actions table operations
- ✅ Assets table operations

## Test Features

### Mocking
- Uses `unittest.mock.patch` to mock external API calls
- Prevents actual network requests during testing

### Temporary Database
- Creates temporary SQLite database for each test
- Automatically cleans up after each test
- Isolates test data from production

### Session Management
- Simulates user login for authenticated routes
- Tests both GET and POST requests

## Adding New Tests

To add new tests:

1. **Create test method** in appropriate test class:
```python
def test_new_feature(self):
    """Test description"""
    # Test implementation
    pass
```

2. **Follow naming convention**: `test_<feature_name>`

3. **Use descriptive docstrings** explaining what is being tested

4. **Test both success and failure cases**

## Test Best Practices

- Each test should be independent
- Use `setUp()` and `tearDown()` for test isolation
- Mock external dependencies
- Test edge cases and error conditions
- Use descriptive test names and assertions

## Troubleshooting

### Import Errors
Make sure you're running tests from the correct directory:
```bash
cd week9/finance
python test/run_tests.py
```

### Database Errors
Tests create temporary databases automatically. If you see database errors, check that the test directory has write permissions.

### Mock Issues
If mocking isn't working, ensure you're patching the correct module path in your test.
