import csv
from typing import Any
from pathlib import Path
from datetime import datetime


def write_csv(data: list[dict[str, Any]], filename: str, output_dir: str = ".") -> Path:
    """Write data to CSV file"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filepath = output_path / filename

    if not data:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["No data found"])
        return filepath

    fieldnames = data[0].keys()

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return filepath


def format_currency(amount: float) -> str:
    """Format currency amount"""
    return f"${amount:,.2f}"


def format_date(date_str: str) -> str:
    """Format date string to YYYY-MM-DD"""
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d")
        return str(date_str)
    except Exception:
        return str(date_str)


def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """Flatten nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            for i, item in enumerate(v):
                items.extend(flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
