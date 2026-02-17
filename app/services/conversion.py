"""Currency conversion helpers."""
from __future__ import annotations

import httpx
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Dict, List, Optional
from datetime import datetime, timedelta

# API endpoint for exchange rates (ExchangeRate-API open access)
_API_URL = "https://open.er-api.com/v6/latest/USD"

# Cache for exchange rates to avoid excessive API calls
_rates_cache: Optional[Dict[str, Decimal]] = None
_cache_timestamp: Optional[datetime] = None
_CACHE_DURATION = timedelta(hours=1)  # Cache rates for 1 hour

# Fallback rates in case API is unavailable
_FALLBACK_RATES: Dict[str, Decimal] = {
    "EUR": Decimal("0.92"),
    "INR": Decimal("83.00"),
}



def _fetch_exchange_rates() -> Dict[str, Decimal]:
    """Fetch current exchange rates from the API.
    
    Returns a dictionary of currency codes to exchange rates.
    Raises an exception if the API call fails.
    """
    try:
        response = httpx.get(_API_URL, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        
        if data.get("result") != "success":
            raise ValueError("API returned unsuccessful result")
        
        rates = data.get("rates", {})
        # Convert rates to Decimal for precision
        return {code: Decimal(str(rate)) for code, rate in rates.items()}
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Failed to fetch exchange rates: {e}")
        raise


def _get_rates() -> Dict[str, Decimal]:
    """Get exchange rates, using cache if available and fresh.
    
    Falls back to fallback rates if API is unavailable.
    """
    global _rates_cache, _cache_timestamp
    
    now = datetime.now()
    
    # Return cached rates if they're still fresh
    if _rates_cache and _cache_timestamp:
        if now - _cache_timestamp < _CACHE_DURATION:
            return _rates_cache
    
    # Try to fetch fresh rates from API
    try:
        _rates_cache = _fetch_exchange_rates()
        _cache_timestamp = now
        return _rates_cache
    except Exception:
        # If we have cached rates (even if expired), use them
        if _rates_cache:
            return _rates_cache
        # Otherwise, fall back to hardcoded rates
        return _FALLBACK_RATES


def get_supported_currencies() -> List[str]:
    """Return the list of allowed target currencies."""
    rates = _get_rates()
    # Filter to only include EUR and INR to maintain current functionality
    return [code for code in ["EUR", "INR"] if code in rates]


def convert_usd(amount: str | float | int | Decimal, target_currency: str) -> Decimal:
    """Convert a USD amount to the requested target currency.

    Raises ValueError when the amount cannot be parsed, is negative, or when
    the currency is not supported.
    """

    try:
        usd_amount = Decimal(str(amount))
    except (InvalidOperation, ValueError) as exc:  # ValueError covers float('nan')
        raise ValueError("Invalid amount supplied.") from exc

    if usd_amount < 0:
        raise ValueError("Amount must be zero or greater.")

    currency_code = target_currency.upper()
    
    # Only allow EUR and INR to maintain current functionality
    if currency_code not in ["EUR", "INR"]:
        raise ValueError("Unsupported currency selection.")
    
    rates = _get_rates()
    
    if currency_code not in rates:
        raise ValueError("Unsupported currency selection.")

    rate = rates[currency_code]
    converted = (usd_amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return converted
