from datetime import datetime

class relativedelta:
    """Simplified relativedelta supporting month offsets."""

    def __init__(self, months=0):
        self.months = months

    def __rsub__(self, other: datetime) -> datetime:
        return subtract_months(other, self.months)


def subtract_months(dt: datetime, months: int) -> datetime:
    year = dt.year
    month = dt.month - months
    while month <= 0:
        month += 12
        year -= 1
    # handle day overflow for month end
    day = min(dt.day, _days_in_month(year, month))
    return dt.replace(year=year, month=month, day=day)


def _days_in_month(year: int, month: int) -> int:
    if month == 2:
        # leap year check
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 29
        return 28
    thirty_days = {4, 6, 9, 11}
    return 30 if month in thirty_days else 31
