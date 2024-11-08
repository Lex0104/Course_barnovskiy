import json
import logging
import os
import re

this_catalog = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(this_catalog, "../logs/services.log")
abs_file_path = os.path.abspath(file_path)

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def transactions_phone_numbers(operations: list) -> json:
    """Функция направлена на возвращание JSON со всеми транзакциями, содержащими в описании номера"""
    logger.info("Ищем транзакции содержащие мобильные номера")
    pattern = re.compile(r"\b?:(\+7)\s*(985|981|926|915|949|916|925|\d{3})\s*\d{3}\s*[-]\s*\d{2}\s*[-]\s*\d{2}\b")
    filtered_transactions = [
        operation for operation in operations if "Описание" in operation and pattern.search(operation["Описание"])
    ]
    return json.dumps(filtered_transactions, ensure_ascii=False)
