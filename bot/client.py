import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv
from .logging_config import setup_logging

logger = setup_logging()
load_dotenv()

class BinanceBotClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.testnet = os.getenv("BINANCE_TESTNET", "True").lower() == "true"
        
        if not self.api_key or not self.api_secret:
            logger.error("API Key or Secret missing. Please check your .env file.")
            raise ValueError("API Key and Secret are required.")

        try:
            self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
            # For Futures USDT-M, we use the futures_ methods
            logger.info(f"Binance Client initialized (Testnet: {self.testnet})")
        except Exception as e:
            logger.exception(f"Failed to initialize Binance Client: {e}")
            raise

    def get_futures_client(self):
        return self.client
