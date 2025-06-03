"""
Test file for SmartGrocery Final Project
File: test_project.py
"""

import pytest
from project import validate_purchase_input, calculate_budget_status, format_purchase_summary


def test_validate_purchase_input():
    """Test the validate_purchase_input function."""
    # Test valid inputs
    assert validate_purchase_input("Apple", 1.50, 3.0) == True
    assert validate_purchase_input("Bread", 2.99, 1.0) == True
    assert validate_purchase_input("Milk", 0.0, 2.0) == True  # Zero price is valid
    assert validate_purchase_input("Eggs", 3.50, 0.0) == True  # Zero quantity is valid

    # Test invalid inputs
    assert validate_purchase_input("", 1.50, 3.0) == False  # Empty product name
    assert validate_purchase_input("   ", 1.50, 3.0) == False  # Whitespace only name
    assert validate_purchase_input("Apple", -1.50, 3.0) == False  # Negative price
    assert validate_purchase_input("Apple", 1.50, -3.0) == False  # Negative quantity
    assert validate_purchase_input("", -1.50, -3.0) == False  # Multiple invalid inputs


def test_calculate_budget_status():
    """Test the calculate_budget_status function."""
    # Test normal budget usage
    result = calculate_budget_status(100.0, 50.0)
    assert result['remaining_budget'] == 50.0
    assert result['percentage_used'] == 50.0
    assert result['is_over_budget'] == False
    assert result['is_low_budget'] == False
    assert result['is_critical_budget'] == False

    # Test over budget scenario
    result = calculate_budget_status(100.0, 120.0)
    assert result['remaining_budget'] == -20.0
    assert result['percentage_used'] == 120.0
    assert result['is_over_budget'] == True

    # Test low budget scenario (between 10-20% remaining)
    result = calculate_budget_status(100.0, 85.0)
    assert result['remaining_budget'] == 15.0
    assert result['percentage_used'] == 85.0
    assert result['is_over_budget'] == False
    assert result['is_low_budget'] == True
    assert result['is_critical_budget'] == False

    # Test critical budget scenario (less than 10% remaining)
    result = calculate_budget_status(100.0, 95.0)
    assert result['remaining_budget'] == 5.0
    assert result['percentage_used'] == 95.0
    assert result['is_over_budget'] == False
    assert result['is_low_budget'] == False
    assert result['is_critical_budget'] == True

    # Test zero budget edge case
    result = calculate_budget_status(0.0, 0.0)
    assert result['remaining_budget'] == 0.0
    assert result['percentage_used'] == 0.0
    assert result['is_over_budget'] == False


def test_format_purchase_summary():
    """Test the format_purchase_summary function."""
    # Test empty purchases list
    result = format_purchase_summary([])
    assert result == "No purchases made yet."

    # Test single purchase
    purchases = [
        {
            'name': 'Apple',
            'quantity': 3.0,
            'unit_price': 1.50,
            'total_price': 4.50
        }
    ]
    result = format_purchase_summary(purchases)
    assert "PURCHASE SUMMARY" in result
    assert "Apple" in result
    assert "3.0" in result
    assert "1.50" in result
    assert "4.50" in result
    assert "TOTAL SPENT:" in result

    # Test multiple purchases
    purchases = [
        {
            'name': 'Apple',
            'quantity': 3.0,
            'unit_price': 1.50,
            'total_price': 4.50
        },
        {
            'name': 'Bread',
            'quantity': 1.0,
            'unit_price': 2.99,
            'total_price': 2.99
        }
    ]
    result = format_purchase_summary(purchases)
    assert "Apple" in result
    assert "Bread" in result
    assert "$7.49" in result  # Total should be 4.50 + 2.99 = 7.49

    # Test formatting consistency
    assert result.count("=") >= 70  # Header separator
    assert result.count("-") >= 70  # Table separators
    assert "Product Name" in result  # Column headers
    assert "Qty" in result
    assert "Unit Price" in result
    assert "Total Price" in result


def test_validate_purchase_input_edge_cases():
    """Test edge cases for validate_purchase_input function."""
    # Test with very large numbers
    assert validate_purchase_input("Expensive Item", 999999.99, 1.0) == True
    assert validate_purchase_input("Bulk Item", 1.0, 999999.0) == True

    # Test with very small positive numbers
    assert validate_purchase_input("Cheap Item", 0.01, 0.1) == True

    # Test with None values (should handle gracefully)
    try:
        result = validate_purchase_input(None, 1.0, 1.0)
        assert result == False
    except:
        pass  # Function might raise exception, which is acceptable

    # Test with special characters in product name
    assert validate_purchase_input("Coca-Cola", 1.50, 1.0) == True
    assert validate_purchase_input("Ben & Jerry's", 5.99, 1.0) == True


def test_calculate_budget_status_edge_cases():
    """Test edge cases for calculate_budget_status function."""
    # Test with very small budget
    result = calculate_budget_status(0.01, 0.005)
    assert result['remaining_budget'] == 0.005
    assert result['percentage_used'] == 50.0

    # Test exact budget usage
    result = calculate_budget_status(100.0, 100.0)
    assert result['remaining_budget'] == 0.0
    assert result['percentage_used'] == 100.0
    assert result['is_over_budget'] == False

    # Test boundary conditions for low budget warning
    result = calculate_budget_status(100.0, 80.0)  # Exactly 20% remaining
    assert result['is_low_budget'] == True

    result = calculate_budget_status(100.0, 79.9)  # Just over 20% remaining
    assert result['is_low_budget'] == False

    # Test boundary conditions for critical budget warning
    result = calculate_budget_status(100.0, 90.0)  # Exactly 10% remaining
    assert result['is_critical_budget'] == True

    result = calculate_budget_status(100.0, 89.9)  # Just over 10% remaining
    assert result['is_critical_budget'] == False
