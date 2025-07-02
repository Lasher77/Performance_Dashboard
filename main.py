import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta

from src.analysis import get_membership_metrics


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Display membership metrics")
    parser.add_argument("--months", type=int, default=1,
                        help="Number of months of data to include")
    return parser.parse_args(args)


def calculate_since_date(months, *, now=None):
    now = now or datetime.now()
    return now - relativedelta(months=months)


def main(args=None):
    args = parse_args(args)
    since = calculate_since_date(args.months)
    metrics = get_membership_metrics()
    print(f"Metrics since {since.date()}: {metrics}")


if __name__ == "__main__":
    main()
