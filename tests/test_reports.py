import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture()
def transactions() -> pd.DataFrame:
    transactions_data = [
        {"Дата платежа": "30.12.2021", "Категория": "Пополнения", "Сумма операции с округлением": 5046.48},
        {"Дата платежа": "18.12.2021", "Категория": "Пополнения", "Сумма операции с округлением": 174000.00},
        {"Дата платежа": "27.09.2020", "Категория": "Цветы", "Сумма операции с округлением": -315.00},
        {"Дата платежа": "27.09.2020", "Категория": "Супермаркеты", "Сумма операции с округлением": -122.97},
        {"Дата платежа": "28.08.2020", "Категория": "Аптеки", "Сумма операции с округлением": -277.00},
    ]
    transactions_df = pd.DataFrame(transactions_data)
    return transactions_df


def test_spending_by_category(transactions: pd.DataFrame) -> None:
    result_df = spending_by_category(transactions, "Пополнения", "2021-18-12 17:50:17")
    assert len(result_df) == 1


def test_spending_by_category_no_data(transactions: pd.DataFrame) -> None:
    result_df = spending_by_category(transactions, "Аптеки")
    assert len(result_df) == 1
    assert result_df["Траты"].values == 0