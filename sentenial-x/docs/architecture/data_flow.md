# Sentinel-X Data Flow Architecture

## Overview

Sentinel-X is a high-performance, modular crypto trading bot built for speed, reliability, and extensibility. The data flow is **real-time first**, event-driven, and designed to minimize latency from market data ingestion to trade execution. Everything is asynchronous (Python `asyncio`), uses queues for decoupling, and has built-in fault tolerance, retries, and circuit breakers.

The system handles:
- Live market data (ticks, order books, klines)
- Historical data for backtesting/training
- Signal generation (TA, ML, custom strategies)
- Risk checks
- Order execution
- Portfolio tracking
- Logging / metrics

## High-Level Data Flow Diagram

```mermaid
graph TD
    subgraph "External Sources"
        A1[Crypto Exchanges<br>(Binance, Bybit, Coinbase, etc.)]
        A2[WebSocket Feeds<br>(price, trades, orderbook)]
        A3[REST APIs<br>(klines, balances, orders)]
        A4[Optional External Feeds<br>(News, On-chain, Twitter/X sentiment)]
    end

    subgraph "Ingestion Layer"
        B1[WebSocket Manager<br>(ccxt.async or raw ws)]
        B2[REST Poller<br>(scheduled fetches)]
        B3[Data Normalizer<br>(to unified Candle/Tick objects)]
    end

    subgraph "Core Pipeline"
        C1[Message Queue<br>(asyncio Queue or Redis Streams)]
        C2[Feature Engine<br>(TA indicators, orderbook imbalance, etc.)]
        C3[Strategy Engine<br>(parallel strategy evaluation)]
        C4[Signal Aggregator<br>(combine/vote across strategies)]
    end

    subgraph "Decision & Risk"
        D1[Risk Manager<br>(position sizing, drawdown, exposure limits)]
        D2[Signal Filter<br>(confidence threshold, cooldowns)]
    end

    subgraph "Execution Layer"
        E1[Order Executor<br>(market/limit/stop orders via ccxt)]
        E2[Order Tracker<br>(fill monitoring, partial fills)]
    end

    subgraph "Persistence & Feedback"
        F1[Time-Series DB<br>(InfluxDB or PostgreSQL + Timescale)]
        F2[Relational DB<br>(SQLite/PostgreSQL for trades, config)]
        F3[Logging & Metrics<br>(structured logs + Prometheus)]
        F4[Portfolio State<br>(real-time P&L, positions)]
    end

    A1 -->|A2: Live streams| B1
    A1 -->|A3: Periodic| B2
    A4 --> B1
    B1 & B2 --> B3 --> C1
    C1 --> C2 --> C3 --> C4 --> D1 --> D2
    D2 --> E1 --> A1
    E1 --> E2 --> F4
    C1 & C2 & C3 & D1 & E1 & E2 --> F1 & F3
    E2 --> F2
    F4 --> D1
