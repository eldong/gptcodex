from decimal import Decimal

import pytest

from app.services.conversion import convert_usd


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
