from decimal import Decimal
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

import pytest
import httpx

from app.services.conversion import convert_usd, _get_rates, _fetch_exchange_rates


@pytest.fixture(autouse=True)
def mock_exchange_api():
    """Mock the exchange rate API to return consistent test data."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "result": "success",
        "rates": {
            "EUR": 0.92,
            "INR": 83.00,
            "GBP": 0.79,
        }
    }
    mock_response.raise_for_status = Mock()
    
    with patch('app.services.conversion.httpx.get', return_value=mock_response):
        # Clear cache before each test
        import app.services.conversion as conv
        conv._rates_cache = None
        conv._cache_timestamp = None
        yield


def test_convert_usd_to_eur():
    assert convert_usd("10", "EUR") == Decimal("9.20")


def test_convert_usd_to_inr():
    assert convert_usd(5, "INR") == Decimal("415.00")


def test_convert_rejects_negative_amount():
    with pytest.raises(ValueError):
        convert_usd(-1, "EUR")


def test_convert_rejects_invalid_amount():
    with pytest.raises(ValueError):
        convert_usd("abc", "EUR")


def test_convert_rejects_unsupported_currency():
    with pytest.raises(ValueError):
        convert_usd("10", "GBP")


def test_fallback_to_hardcoded_rates_on_api_failure():
    """Test that fallback rates are used when API fails."""
    import app.services.conversion as conv
    conv._rates_cache = None
    conv._cache_timestamp = None
    
    with patch('app.services.conversion.httpx.get', side_effect=httpx.RequestError("Network error")):
        rates = _get_rates()
        # Should fall back to hardcoded rates
        assert "EUR" in rates
        assert "INR" in rates
        # Fallback rates should work for conversion
        result = convert_usd("10", "EUR")
        assert result == Decimal("9.20")


def test_cache_is_used():
    """Test that cached rates are reused."""
    import app.services.conversion as conv
    
    # First call - should fetch from API
    rates1 = _get_rates()
    assert rates1 is not None
    
    # Mock API to return different data
    mock_response = Mock()
    mock_response.json.return_value = {
        "result": "success",
        "rates": {
            "EUR": 0.50,  # Different rate
            "INR": 50.00,  # Different rate
        }
    }
    mock_response.raise_for_status = Mock()
    
    with patch('app.services.conversion.httpx.get', return_value=mock_response):
        # Second call - should use cache with old rates
        rates2 = _get_rates()
        assert rates2["EUR"] == Decimal("0.92")  # Old cached rate
        assert rates2["INR"] == Decimal("83.00")  # Old cached rate
