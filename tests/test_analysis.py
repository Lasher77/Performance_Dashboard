import math

from src import analysis


def test_to_dataframe_columns():
    df = analysis.to_dataframe()
    expected = [
        'active_members',
        'inactive_members',
        'total_members',
        'active_ratio',
        'inactive_ratio',
    ]
    assert list(df.columns) == expected


def test_to_dataframe_values():
    df = analysis.to_dataframe()
    assert df['active_members'][0] == 120
    assert df['inactive_members'][0] == 30
    assert df['total_members'][0] == 150
    assert math.isclose(df['active_ratio'][0], 120 / 150)
    assert math.isclose(df['inactive_ratio'][0], 30 / 150)
