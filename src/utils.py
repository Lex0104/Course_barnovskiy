import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

basic_design = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_json = os.path.join(basic_design, "user_settings.json")

current_dir = os.path.dirname(os.path.abspath(__file__))

rel_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

load_dotenv()
for_currency = os.getenv("API_KEY_FOR_CURRENCY")
for_share = os.getenv("API_KEY_FOR_STOCK")


def get_data_excel(path_to_the_file: str) -> list:
    """Возвращение данных о финансовых транзакциях из файла excel"""
    try:
        pd.read_excel(path_to_the_file)

    except ValueError as ex:
        logger.error(f"Произошла ошибка {ex}")

        return []

    else:
        operations = pd.read_excel(path_to_the_file)
        logger.info("Успешное выполнение")
        return operations.to_dict(orient="records")


def sort_date_operations(operations: list, date: str) -> list:
    """Сортирует операции за текущий месяц"""
    sorted_operations = []
    first_day_moth = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").replace(day=1)
    data_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    for operation in operations:
        date_operation = datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if first_day_moth <= date_operation <= data_datetime:
            sorted_operations.append(operation)
    return sorted_operations


def greeting_user() -> str:
    """Возвращает приветствие в зависимости от времени суток"""
    logger.info("Приветствуем пользователя")
    time_moment = datetime.now().hour
    if time_moment < 6:
        return "Доброй ночи"
    elif time_moment < 12:
        return "Доброе утро"
    elif time_moment < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def operations_cards(operations: list) -> list:
    """Возвращает данные по каждой карте"""
    card_number_operations = {}
    result = []
    logger.info("Ищем информацию по каждой карте")
    for operation in operations:
        card_number = str(operation.get("Номер карты"))
        amount = operation.get("Сумма операции с округлением")
        if card_number != "":
            four_digits = card_number[-4:]
            if four_digits in card_number_operations:
                card_number_operations[four_digits]["total_spent"] += amount
            else:
                card_number_operations[four_digits] = {"total_spent": (amount), "cashback": 0}
            card_number_operations[four_digits]["cashback"] = card_number_operations[four_digits]["total_spent"] * 0.01
    for digits, data in card_number_operations.items():
        result.append(
            {"four_digits": digits, "total_spent": round(data["total_spent"], 2), "cashback": data["cashback"]}
        )
    return result


def top_five(operations: list) -> list:
    """Возвращает топ-5 транзакций по сумме платежа"""
    ret_transaction = []
    logger.info("Ищем топ-5 транзакций по сумме платежа.")
    sorted_operations = sorted(operations, key=lambda x: x["Сумма операции с округлением"], reverse=True)
    top_transactions = sorted_operations[:5]
    for sort in top_transactions:
        date = sort["Дата операции"][:10]
        str_amount = sort.get("Сумма операции с округлением")
        ret_transaction.append(
            {"date": date, "amount": str_amount, "category": sort["Категория"], "description": sort["Описание"]}
        )
    return ret_transaction


def currency_rates() -> list:
    """Возвращает курсы валют"""
    logger.info("Поиска курс валют")
    result_usd = requests.get(
        f"https://api.currencyapi.com/v3/latest?apikey={for_currency}&base_currency=USD&currencies=RUB"
    )
    result_eur = requests.get(
        f"https://api.currencyapi.com/v3/latest?apikey={for_currency}&base_currency=EUR&currencies=RUB"
    )
    price_dollar = result_usd.json()["data"]["RUB"]["value"]
    price_eur = result_eur.json()["data"]["RUB"]["value"]
    result = [{"currency": "USD", "rate": round(price_dollar, 2)}, {"currency": "EUR", "rate": round(price_eur, 2)}]
    return result


def stock_prices() -> list:
    """Cтоимость акций S&P 500"""
    logger.info("Поиск основных акций из S&P500")
    # url =
    result = []
    with open(file_json, encoding="utf-8") as file:
        share_shares = json.load(file)
        share_shares = ",".join(share_shares["user_stocks"])
        querystring = {"symbols": share_shares}
        response = requests.get(url, params=querystring)
        for data in response.json()["data"]:
            result.append({"stock": data["symbol"], "price": data["close"]})
        return result