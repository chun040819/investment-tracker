from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import pandas as pd
import yfinance as yf


def _build_ticker_symbol(symbol: str, exchange: str | None = None) -> str:
    """
    Build a yfinance ticker symbol. Currently returns symbol directly.
    Exchange-specific suffix mapping can be added here when needed.
    """
    return symbol


def fetch_daily_close(symbol: str, start: date, end: date) -> list[tuple[date, Decimal]]:
    """
    Fetch daily close prices (inclusive of end date) using yfinance.

    Raises:
        ValueError: when no data is returned.
    """
    if start > end:
        raise ValueError("start date must be on or before end date")

    yf_symbol = _build_ticker_symbol(symbol)

    # yfinance end date is exclusive; add one day to include the end date requested.
    df: pd.DataFrame = yf.download(
        yf_symbol,
        start=start,
        end=end + timedelta(days=1),
        progress=False,
        auto_adjust=False,
        interval="1d",
    )

    if df.empty or "Close" not in df.columns:
        raise ValueError(f"No price data for {symbol} between {start} and {end}")

    df = df.dropna(subset=["Close"])
    if df.empty:
        raise ValueError(f"No price data for {symbol} between {start} and {end}")

    closes: list[tuple[date, Decimal]] = []
    for idx, close in df["Close"].items():
        closes.append((idx.date(), Decimal(str(close))))

    return closes
