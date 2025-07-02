from datetime import datetime
from dateutil.relativedelta import relativedelta

from main import calculate_since_date, parse_args


def test_calculate_since_date():
    now = datetime(2024, 1, 31, 12, 0, 0)
    result = calculate_since_date(2, now=now)
    assert result == now - relativedelta(months=2)


def test_parse_args_default():
    args = parse_args([])
    assert args.months == 1


def test_parse_args_value():
    args = parse_args(["--months", "3"])
    assert args.months == 3
