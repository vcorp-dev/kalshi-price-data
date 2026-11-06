# Kalshi Price Data

**The fastest way to get Kalshi historical data and live price data** — yes/no contract prices, the full order book behind them, and a replayable historical series — through one aggregated API. This small Python client runs against [DepthFeed](https://depthfeed.com) and includes a keyless live overview.

[![DepthFeed — Kalshi price data API](https://img.shields.io/badge/Get%20the%20data-DepthFeed-2563eb)](https://kalshipricedata.com/price-data)
[![Kalshi order book history — 114M+ snapshots](https://img.shields.io/badge/Order%20book%20history-114M%2B%20snapshots-16a34a)](https://kalshipricedata.com/order-book-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

<!-- Kalshi price data · Kalshi price API · Kalshi order book data · Kalshi historical prices · Kalshi market data · prediction market price data -->

> **Which "Kalshi price data" do you mean?** This is **prediction-market price data** — the yes/no price of a *Kalshi market* (e.g. "Will BTC be above $X at 4pm?"), read off the live order book. It is **not** the `$KALSHI` pre-IPO stock/token. If you want the market's own probability price, its depth, and its history, you're in the right place.

---

## Installation and quickstart — get a Kalshi price in 6 lines

```bash
pip install -r requirements.txt
```

```python
from kalshi_price_data import KalshiPriceData

k = KalshiPriceData()          # defaults to the DepthFeed aggregator
ov = k.overview()              # public endpoint — no key needed
print(ov)                      # live Kalshi (+ Polymarket + Limitless) prices
```

`overview()` hits `https://api.depthfeed.com/v3/overview` — a public endpoint, so the snippet **runs as-is**. For per-market Kalshi history and full yes/no depth, add a [key](https://kalshipricedata.com/price-data).

---

## Table of contents

- [What "Kalshi price data" actually is](#what-kalshi-price-data-actually-is)
- [Why the public API isn't enough](#why-the-public-api-isnt-enough)
- [Live proof and data coverage](#live-proof-and-data-coverage)
- [Usage examples](#usage-examples)
- [FAQ](#faq)
- [Further reading](#further-reading)

---

## What "Kalshi price data" actually is

Kalshi is a regulated exchange that runs a **central limit order book** on yes/no event contracts. Every market has a **yes** side and a **no** side; prices are quoted in **cents from `1` to `99`** (equivalently `0`–`1`), and the price *is* the market-implied probability of the event.

So "Kalshi price data" is really **two layers**:

1. **The contract price** — yes and no quoted `0`–`1`. The honest live number is the best-bid/ask, and the two sides tie together: **a yes bid at price `p` is a no offer at `1 − p`**, so the implied yes ask is `1 −` the best no bid.
2. **The order book** — the full ladder of resting yes and no orders (`[price, size]`). That's where depth, spread and liquidity actually live — not in a last-trade print.

---

## Why the public API isn't enough

Kalshi's public endpoints are real and key-free for live data, but the history is the problem:

> **Live state is easy; continuous history is not. Kalshi's data is fragmented across endpoints — you must stitch trades, markets and order books together yourself — and order-book depth cannot be back-filled once it has streamed past.**

You can read a market's book *now*, but reconstructing what the yes/no ladder looked like minute-by-minute last week means you needed to be recording it live, across hundreds of thousands of markets, without gaps. That's an infrastructure project, not an API call.

That's the gap an aggregator fills.

---

## Live proof and data coverage

[**DepthFeed**](https://kalshipricedata.com/price-data) is the aggregator. It has already captured the full Kalshi yes/no order book — forward, continuously — into one queryable API, alongside two other venues. The figures below are **measured from the live archive** (June 2026), not estimates:

- **114M+ order-book snapshots** across **550,000+ Kalshi markets**, back to **March 2026**.
- **Full yes/no L2 depth** preserved. On BTC 15-minute markets the typical book is a one-cent spread, **~96 price levels per side** (up to the full 100), **~156,000 contracts** of resting depth.
- Windows captured: **15-minute, hourly, daily and weekly** — filterable by `?type=` and `?coin=`.
- **One endpoint, three venues** — Kalshi **+ Polymarket + Limitless** — the same "BTC up or down, next 15 min" question priced side-by-side. (Polymarket sister repo: [**polymarket-price-data**](https://github.com/vcorp-dev/polymarket-price-data).)
- **REST + WebSocket**, cursor pagination, server-side downsampling, Parquet bulk export.

You don't run a collector. You call an endpoint.

---

## Usage examples

The client defaults to the DepthFeed aggregator. **Everything is testable against the live endpoints.**

### No key — try real data instantly

```python
from kalshi_price_data import KalshiPriceData
k = KalshiPriceData()
k.overview()     # GET /v3/overview  (public) — live cross-venue prices (incl. Kalshi)
k.health()       # GET /v3/health    (public)
```

`overview()` returns live cross-venue market prices with no signup. It is the fastest way to verify connectivity before adding an API key for historical snapshots and full depth.

### With a key — Kalshi markets, history, full yes/no depth

```python
k = KalshiPriceData(api_key="YOUR_DEPTHFEED_KEY")

# List Kalshi BTC 15-minute markets
markets = k.markets(coin="btc", type="15m", limit=20)

# Latest order book for a ticker
book = k.orderbook_latest(markets[0]["ticker"])

# Historical yes/no depth for a ticker
snaps = k.snapshots(markets[0]["ticker"], limit=100)
```

Runnable scripts: [`examples/overview_no_key.py`](./examples/overview_no_key.py) · [`examples/market_history.py`](./examples/market_history.py).

Full endpoint reference: **[kalshipricedata.com/docs](https://kalshipricedata.com/docs)** · [API overview](https://kalshipricedata.com/data-api).

→ **[Grab an API key at kalshipricedata.com/price-data](https://kalshipricedata.com/price-data)**
See [current DepthFeed plans and limits](https://depthfeed.com/pricing). Check `/v3/whoami` for your account's effective access.

---

## FAQ

**Does Kalshi have a price API?**
Yes — Kalshi's public endpoints serve *live* market data without a key. For live **plus** continuous history and full yes/no depth pre-stitched in one place, use the DepthFeed aggregator (see [current plan access](https://depthfeed.com/pricing)).

**How do I get historical Kalshi price data?**
Order-book depth can't be back-filled — it has to be recorded live across every market. DepthFeed holds 114M+ Kalshi snapshots back to March 2026; query one ticker's history with [`examples/market_history.py`](./examples/market_history.py).

**What do Kalshi prices mean?**
Yes and no contracts quoted `1`–`99¢` (`0`–`1`); the price is the implied probability. A yes bid at `p` is a no offer at `1 − p`, so the implied yes ask is `1 −` the best no bid.

**Can I get Kalshi and Polymarket prices together?**
Yes — that's the point of an aggregator. One DepthFeed call returns the same market priced across Kalshi, Polymarket and Limitless. See [**polymarket-price-data**](https://github.com/vcorp-dev/polymarket-price-data).

**How do I download Kalshi price data to CSV / Parquet?**
For Parquet delivery, see [bulk data options](https://depthfeed.com/bulk-data). REST responses are JSON you can write to CSV.

---

## Further reading

- 🔌 [Official DepthFeed Kalshi API guide](https://depthfeed.com/resources/kalshi-api-guide)
- 🧪 [Prediction-market trading bot backtesting](https://depthfeed.com/resources/prediction-market-trading-bot-backtesting)
- 🧪 [Paper trade Kalshi strategies on live displayed books](https://depthfeed.com/kalshi-paper-trading)
- 📈 [Kalshi price data, explained](https://kalshipricedata.com/resources/kalshi-price-data-explained)
- ⏱️ [Kalshi market windows explained](https://kalshipricedata.com/resources/kalshi-market-windows-explained)
- ⚙️ [How Kalshi crypto markets settle](https://kalshipricedata.com/resources/how-kalshi-crypto-markets-settle)
- 📊 [Order-book depth vs last price](https://kalshipricedata.com/resources/order-book-depth-vs-last-price)
- ⚖️ [Polymarket vs Kalshi data](https://kalshipricedata.com/resources/polymarket-vs-kalshi-data)
- 🟦 Polymarket too? → [**polymarket-price-data**](https://github.com/vcorp-dev/polymarket-price-data)

---

Contributions are welcome; see [CONTRIBUTING.md](./CONTRIBUTING.md). For product help, use [DepthFeed support](https://depthfeed.com/contact). Report vulnerabilities privately through [SECURITY.md](./SECURITY.md).

*Independent open-source project. Not affiliated with Kalshi. Archive figures are measured from [DepthFeed](https://depthfeed.com) (a VCorp product). © 2026 VCorp. MIT licensed.*
