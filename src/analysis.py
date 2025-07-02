# Simple analysis module

def get_membership_metrics():
    """Return aggregated membership metrics."""
    # Placeholder implementation
    return {
        'active_members': 120,
        'inactive_members': 30,
        'total_members': 150
    }


def to_dataframe():
    """Return membership metrics as a simple DataFrame like structure."""
    metrics = get_membership_metrics()
    active = metrics['active_members']
    inactive = metrics['inactive_members']
    total = metrics['total_members']
    data = {
        'active_members': [active],
        'inactive_members': [inactive],
        'total_members': [total],
        'active_ratio': [active / total],
        'inactive_ratio': [inactive / total],
    }

    try:
        import pandas as pd  # type: ignore
    except Exception:  # pragma: no cover - fallback when pandas is missing
        class SimpleDataFrame(dict):
            def __init__(self, d):
                super().__init__(d)
                self.columns = list(d.keys())

            def __getitem__(self, item):
                return self.get(item)

        return SimpleDataFrame(data)

    return pd.DataFrame(data)
