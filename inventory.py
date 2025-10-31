import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# ----------------------------- #
#   Global Data Initialization  #
# ----------------------------- #

stock_data: Dict[str, int] = {}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


# ----------------------------- #
#       Inventory Functions     #
# ----------------------------- #

def add_item(item: str = "default", qty: int = 0, logs: Optional[List[str]] = None) -> None:
    """
    Add an item to inventory with the given quantity.
    Includes type checks and logging for safe operation.
    """
    if logs is None:
        logs = []

    # Validate inputs
    if not isinstance(item, str):
        logging.error("Invalid item name: %r (must be a string)", item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid quantity for %s: %r (must be integer)", item, qty)
        return

    # Add/update stock
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s (total now %d)", qty, item, stock_data[item])


def remove_item(item: str, qty: int) -> None:
    """
    Remove a specified quantity of an item.
    If item does not exist, a warning is logged.
    """
    if not isinstance(item, str):
        logging.error("Invalid item name: %r (must be a string)", item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid quantity for %s: %r (must be integer)", item, qty)
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("Removed %s from inventory", item)
        else:
            logging.info("Decreased %s by %d (remaining: %d)", item, qty, stock_data[item])
    except KeyError:
        logging.warning("Cannot remove %s — item not found", item)


def get_qty(item: str) -> int:
    """Return quantity of an item; 0 if not found."""
    if not isinstance(item, str):
        logging.error("Invalid item name: %r", item)
        return 0
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load inventory data from a JSON file safely."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            stock_data = {k: int(v) for k, v in data.items()}
            logging.info("Loaded data from %s", file)
        else:
            logging.error("Invalid data format in %s", file)
    except FileNotFoundError:
        logging.warning("%s not found — starting with empty inventory", file)
    except (json.JSONDecodeError, ValueError) as e:
        logging.error("Error reading %s: %s", file, e)


def save_data(file: str = "inventory.json") -> None:
    """Save inventory data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Saved data to %s", file)
    except OSError as e:
        logging.error("Error saving data to %s: %s", file, e)


def print_data() -> None:
    """Print all inventory items and quantities."""
    print("\nItems Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print()


def check_low_items(threshold: int = 5) -> List[str]:
    """Return items with quantities below the threshold."""
    if not isinstance(threshold, int):
        logging.error("Threshold must be an integer, got %r", threshold)
        return []
    return [item for item, qty in stock_data.items() if qty < threshold]


# ----------------------------- #
#            Main               #
# ----------------------------- #

def main() -> None:
    """Demonstration of inventory operations."""
    load_data()

    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")        # This will log errors, not crash
    remove_item("apple", 3)
    remove_item("orange", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    print_data()


if __name__ == "__main__":
    main()
