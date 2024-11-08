import json

from src.services import transactions_phone_numbers


def test_transactions_phone_numbers(operations) -> None:
    result = [
        {
            "Дата операции": "30.12.2021 17:50:17",
            "Дата платежа": "30.12.2021",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": 174000.00,
            "Валюта операции": "RUB",
            "Сумма платежа": 174000.00,
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Пополнения",
            "MCC": "",
            "Описание": "МТС Mobile +7 981 333-44-55",
            "Бонусы (включая кэшбэк)": 0.00,
            "Округление на инвесткопилку": 0.00,
            "Сумма операции с округлением": 174000.00,
        },
    ]
    assert transactions_phone_numbers(operations) == json.dumps(result, ensure_ascii=False)