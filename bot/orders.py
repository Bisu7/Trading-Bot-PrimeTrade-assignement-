from binance.exceptions import BinanceAPIException, BinanceOrderException
from .logging_config import setup_logging

logger = setup_logging()

class OrderManager:
    def __init__(self, client):
        self.client = client

    def place_market_order(self, symbol, side, quantity):
        """Place a MARKET order on Binance Futures."""
        try:
            logger.info(f"Placing MARKET {side} order for {quantity} {symbol}")
            response = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            logger.debug(f"Market order response: {response}")
            return True, response
        except (BinanceAPIException, BinanceOrderException) as e:
            logger.error(f"Failed to place Market order: {e.message}")
            return False, e.message
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return False, str(e)

    def place_limit_order(self, symbol, side, quantity, price):
        """Place a LIMIT order on Binance Futures."""
        try:
            logger.info(f"Placing LIMIT {side} order for {quantity} {symbol} at price {price}")
            response = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='LIMIT',
                timeInForce='GTC',  # Good Till Cancelled
                quantity=quantity,
                price=price
            )
            logger.debug(f"Limit order response: {response}")
            return True, response
        except (BinanceAPIException, BinanceOrderException) as e:
            logger.error(f"Failed to place Limit order: {e.message}")
            return False, e.message
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return False, str(e)

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        """Place a STOP_LOSS_LIMIT order on Binance Futures."""
        try:
            logger.info(f"Placing STOP_LIMIT {side} order for {quantity} {symbol} (Stop: {stop_price}, Limit: {price})")
            response = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='STOP_LOSS_LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                stopPrice=stop_price
            )
            logger.debug(f"Stop-Limit order response: {response}")
            return True, response
        except (BinanceAPIException, BinanceOrderException) as e:
            logger.error(f"Failed to place Stop-Limit order: {e.message}")
            return False, e.message
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return False, str(e)
