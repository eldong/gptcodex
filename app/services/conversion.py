"""Currency conversion helpers."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Dict, List

# Hard-coded USD conversion rates in Decimal for precision
_RATES: Dict[str, Decimal] = {
    "EUR": Decimal("0.92"),
    "INR": Decimal("83.00"),
}


def get_supported_currencies() -> List[str]:
    """Return the list of allowed target currencies."""
    return list(_RATES.keys())


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
    if currency_code not in _RATES:
        raise ValueError("Unsupported currency selection.")

    rate = _RATES[currency_code]
    converted = (usd_amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return converted
