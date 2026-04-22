# Simplified Binance Futures Trading Bot

A clean, modular Python application to interact with the Binance Futures Testnet (USDT-M). This bot allows users to place Market, Limit, and Stop-Limit orders through a premium interactive CLI.

## Features

- **Interactive CLI:** Built with `questionary` and `rich` for a smooth user experience.
- **Order Types:** Supports MARKET, LIMIT, and STOP_LOSS_LIMIT orders.
- **Robust Validation:** Ensures correct symbols, quantities, and prices before hitting the API.
- **Structured Logging:** Detailed logs are saved to `logs/trade_log.log`, while clean info is shown in the terminal.
- **Error Handling:** Gracefully handles API errors, network issues, and invalid configurations.

## Prerequisites

- Python 3.8+
- Binance Futures Testnet Account ([Register here](https://testnet.binancefuture.com))
- Testnet API Key and Secret

## Setup

1. **Clone or Extract** the project.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment:**
   - Copy `.env.example` to `.env`.
   - Add your `BINANCE_API_KEY` and `BINANCE_API_SECRET` to the `.env` file.
   ```bash
   cp .env.example .env
   ```

## How to Run

Start the interactive CLI:
```bash
python cli.py
```

Follow the on-screen prompts to select the symbol, side, order type, and quantity.

## Project Structure

```text
trading_bot/
  bot/
    client.py        # Binance API client setup
    orders.py        # Core logic for different order types
    validators.py    # Input validation rules
    logging_config.py # Logging system configuration
  logs/              # Created automatically for log files
  cli.py             # Interactive CLI entry point
  README.md          # Documentation
  requirements.txt   # Dependencies
```

## Assumptions

- The bot is strictly for **Binance Futures Testnet (USDT-M)**.
- Users have sufficient balance in their Testnet account.
- Symbols follow the Binance format (e.g., BTCUSDT).

## Logging

Logs are located in the `logs/` directory. 
- `trade_log.log` contains detailed debugging information, including API request summaries and raw responses.
