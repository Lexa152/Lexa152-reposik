from datetime import datetime


def filter_by_state(data, state="EXECUTED"):
    """filter_by_state"""
    return [item for item in data if item.get("state") == state]


def sort_by_date(data, reverse=False):
    """sort_by_date"""
    def parse_date(item):
        raw = item.get("date")
        if not isinstance(raw, str):
            return datetime.min
        try:
            return datetime.fromisoformat(raw)
        except (ValueError, TypeError):
            return datetime.min

    return sorted(data, key=parse_date, reverse=reverse)
