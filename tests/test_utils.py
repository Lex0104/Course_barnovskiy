from datetime import datetime
from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd
import pytest
from src.utils import (
    currency_rates,
    get_data_excel,
    greeting_user,
    operations_cards,
    sort_date_operations,
    stock_prices,
    top_five,
)


@patch("builtins.open", new_callable=mock_open)
@patch("pandas.read_excel")
def test_get_data_excel(mock_read_excel: Any, mock_file: Any) -> None:
    mock_read_excel.return_value = pd.DataFrame({"amount": [100], "currency": ["USD"]})
    transactions = get_data_excel("data/transactions.xlsx")
    assert transactions == [{"amount": 100, "currency": "USD"}]



def test_sort_date_operations(operations_list: list) -> None:
    assert sort_date_operations(operations_list, "2021-12-30 17:50:30") == [
        {
            "Дата операции": "30.12.2021 17:50:30",
            "Дата платежа": "30.12.2021",
            "Номер карты": "",
            "Статус": "OK",
            "Сумма операции": 5046.00,
            "Валюта операции": "RUB",
            "Сумма платежа": 5046.00,
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Пополнение",
            "MCC": "",
            "Описание": "Пополнение через Газпромбанк",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 5046.00,
        }
    ]


@pytest.mark.parametrize(
    ("now_datetime", "expected_greeting"),
    [
        (datetime(2024, 1, 1, hour=6, minute=0), "Доброе утро"),
        (datetime(2024, 1, 1, hour=14, minute=0), "Добрый день"),
        (datetime(2024, 1, 1, hour=20, minute=0), "Добрый вечер"),
        (datetime(2024, 1, 1, hour=3, minute=0), "Доброй ночи"),
    ],
)
@patch("src.utils.datetime")
def test_get_greeting(mocked_datetime: datetime, now_datetime: datetime, expected_greeting: str) -> None:
    mocked_datetime.now.return_value = now_datetime
    assert greeting_user() == expected_greeting


def test_operations_cards() -> None:
    assert operations_cards([{"Номер карты": "*1234", "Сумма операции с округлением": 1.0}]) == [
        {"four_digits": "1234", "total_spent": 1.0, "cashback": 0.01}
    ]


def test_top_five_transactions(small_operations_list: list) -> None:
    assert top_five(small_operations_list) == [
        {"date": "30.12.2021", "amount": 5046.00, "category": "Пополнение", "описание": "Пополнение через Газпромбанк"}
    ]


@patch("requests.get")
def test_currency_rates(mock_usd: Any, mock_eur: Any) -> None:
    mock_usd.return_value.status_code = 200
    mock_eur.return_value.status_code = 200
    mock_usd.return_value.json.return_value = {"data": {"RUB": {"value": 1.00}}}
    mock_eur.return_value.json.return_value = {"data": {"RUB": {"value": 1.00}}}
    assert currency_rates() == [{"currency": "USD", "rate": 1.00}, {"currency": "EUR", "rate": 1.00}]


@patch("requests.get")
def test_stock_prices(mock_convert: Any):
    mock_convert.return_value.status_code = 200
    mock_convert.return_value.json.return_value = {"data": [{"symbol": "AAPL", "close": 1.0}]}
    assert stock_prices() == [{"stock": "AAPL", "price": 1.0}]