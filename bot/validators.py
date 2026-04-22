import re

class Validator:
    @staticmethod
    def validate_symbol(symbol: str):
        """Validate Binance symbol format (e.g., BTCUSDT)."""
        if not symbol or not re.match(r"^[A-Z0-9]{5,12}$", symbol):
            return False, "Invalid symbol format. Example: BTCUSDT"
        return True, ""

    @staticmethod
    def validate_quantity(quantity: str):
        """Validate that quantity is a positive float."""
        try:
            val = float(quantity)
            if val <= 0:
                return False, "Quantity must be greater than zero."
            return True, ""
        except ValueError:
            return False, "Quantity must be a valid number."

    @staticmethod
    def validate_price(price: str, order_type: str):
        """Validate price for LIMIT and STOP_LIMIT orders."""
        if order_type == "MARKET":
            return True, ""
        try:
            val = float(price)
            if val <= 0:
                return False, "Price must be greater than zero."
            return True, ""
        except ValueError:
            return False, "Price must be a valid number."

    @staticmethod
    def validate_side(side: str):
        """Validate order side."""
        if side.upper() not in ["BUY", "SELL"]:
            return False, "Side must be either BUY or SELL."
        return True, ""
