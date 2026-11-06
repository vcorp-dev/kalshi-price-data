"""
Kalshi price-data client — backed by the DepthFeed aggregator.

DepthFeed (https://kalshipricedata.com) aggregates Kalshi price data — live and
historical, full yes/no order-book depth, continuous and pre-stitched — into one
REST API, alongside Polymarket and Limitless. Kalshi's own API serves only live
state, fragments data across endpoints, and cannot back-fill order books; this
client gives you the history instead, through a single endpoint.

Public (no key): overview(), health().
With a key (https://kalshipricedata.com/price-data): markets(), orderbook_latest(),
snapshots(). Check current plan access at https://depthfeed.com/pricing.
"""

from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://api.depthfeed.com"


class KalshiPriceData:
    """Client for Kalshi price data via the DepthFeed aggregator API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = BASE_URL,
        timeout: float = 20.0,
        session: requests.Session | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.s = session or requests.Session()
        self.s.headers.setdefault("User-Agent", "kalshi-price-data/1.0")
        if api_key:
            self.s.headers["X-API-Key"] = api_key

    def _get(self, path: str, **params: Any) -> Any:
        clean = {k: v for k, v in params.items() if v is not None}
        r = self.s.get(f"{self.base_url}{path}", params=clean, timeout=self.timeout)
        r.raise_for_status()
        body = r.json()
        # DepthFeed wraps payloads as {"data": …, "pagination"?: …, "meta": …}
        return body.get("data", body) if isinstance(body, dict) else body

    # --- public (no key) ---------------------------------------------------

    def health(self) -> Any:
        """Service health. Public — no key required."""
        return self._get("/v3/health")

    def overview(self) -> Any:
        """Live cross-venue overview (Kalshi + Polymarket + Limitless).

        Public — no key required.
        """
        return self._get("/v3/overview")

    def demo(self) -> Any:
        """Keyless sample of real order-book depth across venues (BTC 15m, top
        levels). Public — no key required. A taste of the full archive; grab a
        key for every level, asset, window and the full history.
        """
        return self._get("/v3/demo")

    # --- Kalshi markets / history (key; account limits apply) -------------------------

    def markets(
        self,
        coin: str | None = None,
        type: str | None = None,
        limit: int = 100,
        cursor: str | None = None,
    ) -> Any:
        """List Kalshi markets.

        `coin` is the base asset (e.g. "btc"); `type` is the window
        (15m/1h/24h/1w).
        """
        return self._get("/v3/kalshi/markets", coin=coin, type=type,
                         limit=limit, cursor=cursor)

    def orderbook_latest(self, ticker: str) -> Any:
        """Newest yes/no order book for a Kalshi ticker."""
        return self._get(f"/v3/kalshi/{ticker}/orderbook/latest")

    def snapshots(
        self,
        ticker: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        interval: str | None = None,
        limit: int = 100,
        cursor: str | None = None,
    ) -> Any:
        """Historical yes/no order-book depth for one Kalshi ticker.

        `interval` downsamples server-side to one book per bucket (e.g. "1m").
        """
        return self._get(
            f"/v3/kalshi/{ticker}/snapshots",
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            limit=limit,
            cursor=cursor,
        )

    @staticmethod
    def implied_yes_ask(best_no_bid: float) -> float:
        """A no bid at price p is a yes offer at 1 − p. Cents or 0–1 both work
        (cents return cents). Handy for turning the two sides into one price."""
        unit = 100.0 if best_no_bid > 1 else 1.0
        return unit - best_no_bid
