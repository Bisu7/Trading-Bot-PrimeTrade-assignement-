import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from bot.client import BinanceBotClient
from bot.orders import OrderManager
from bot.validators import Validator
from bot.logging_config import setup_logging
import sys

# Initialize components
console = Console()
logger = setup_logging()

def show_banner():
    banner = """
    [bold cyan]╔══════════════════════════════════════════════╗[/bold cyan]
    [bold cyan]║[/bold cyan] [bold white]Binance Futures Testnet Trading Bot[/bold white]       [bold cyan]║[/bold cyan]
    [bold cyan]╚══════════════════════════════════════════════╝[/bold cyan]
    """
    console.print(banner)

def get_order_input():
    # 1. Symbol
    symbol = questionary.text(
        "Enter Trading Symbol (e.g., BTCUSDT):",
        default="BTCUSDT",
        validate=lambda text: Validator.validate_symbol(text)[0] or Validator.validate_symbol(text)[1]
    ).ask()
    if symbol is None: return None

    # 2. Side
    side = questionary.select(
        "Select Side:",
        choices=["BUY", "SELL"]
    ).ask()
    if side is None: return None

    # 3. Order Type
    order_type = questionary.select(
        "Select Order Type:",
        choices=["MARKET", "LIMIT", "STOP_LIMIT"]
    ).ask()
    if order_type is None: return None

    # 4. Quantity
    quantity = questionary.text(
        "Enter Quantity:",
        validate=lambda text: Validator.validate_quantity(text)[0] or Validator.validate_quantity(text)[1]
    ).ask()
    if quantity is None: return None

    # 5. Price (if needed)
    price = None
    stop_price = None
    if order_type in ["LIMIT", "STOP_LIMIT"]:
        price = questionary.text(
            "Enter Limit Price:",
            validate=lambda text: Validator.validate_price(text, order_type)[0] or Validator.validate_price(text, order_type)[1]
        ).ask()
        if price is None: return None

    if order_type == "STOP_LIMIT":
        stop_price = questionary.text(
            "Enter Stop Price:",
            validate=lambda text: Validator.validate_price(text, "STOP_LIMIT")[0] or Validator.validate_price(text, "STOP_LIMIT")[1]
        ).ask()
        if stop_price is None: return None

    return {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type,
        "quantity": float(quantity),
        "price": float(price) if price else None,
        "stop_price": float(stop_price) if stop_price else None
    }

def display_order_summary(order_data):
    table = Table(title="Order Confirmation", show_header=True, header_style="bold magenta")
    table.add_column("Field", style="dim")
    table.add_column("Value")
    
    table.add_row("Symbol", order_data["symbol"])
    table.add_row("Side", order_data["side"])
    table.add_row("Type", order_data["type"])
    table.add_row("Quantity", str(order_data["quantity"]))
    
    if order_data["price"]:
        table.add_row("Limit Price", str(order_data["price"]))
    if order_data["stop_price"]:
        table.add_row("Stop Price", str(order_data["stop_price"]))
        
    console.print(table)
    
    confirm = questionary.confirm("Do you want to place this order?").ask()
    return confirm

def main():
    show_banner()
    
    try:
        bot_client = BinanceBotClient()
        order_manager = OrderManager(bot_client.get_futures_client())
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        sys.exit(1)

    while True:
        order_data = get_order_input()
        if not order_data:
            break
            
        if display_order_summary(order_data):
            success = False
            response = None
            
            with console.status("[bold green]Placing order..."):
                if order_data["type"] == "MARKET":
                    success, response = order_manager.place_market_order(
                        order_data["symbol"], order_data["side"], order_data["quantity"]
                    )
                elif order_data["type"] == "LIMIT":
                    success, response = order_manager.place_limit_order(
                        order_data["symbol"], order_data["side"], order_data["quantity"], order_data["price"]
                    )
                elif order_data["type"] == "STOP_LIMIT":
                    success, response = order_manager.place_stop_limit_order(
                        order_data["symbol"], order_data["side"], order_data["quantity"], order_data["price"], order_data["stop_price"]
                    )

            if success:
                console.print(Panel(f"[bold green]Order Placed Successfully![/bold green]\n"
                                    f"Order ID: {response.get('orderId')}\n"
                                    f"Status: {response.get('status')}\n"
                                    f"Avg Price: {response.get('avgPrice', 'N/A')}\n"
                                    f"Executed Qty: {response.get('executedQty', 'N/A')}",
                                    title="Success", border_style="green"))
            else:
                console.print(Panel(f"[bold red]Order Failed![/bold red]\nError: {response}",
                                    title="Failure", border_style="red"))
        
        if not questionary.confirm("Place another order?").ask():
            break

    console.print("[bold cyan]Goodbye![/bold cyan]")

if __name__ == "__main__":
    main()
