import pandas as pd
from src.reports import spending_by_category
from src.services import transactions_phone_numbers
from src.utils import get_data_excel
from src.views import web_main

transactions = get_data_excel("../data/operations.xlsx")
transactions_df = pd.read_excel("../data/operations.xlsx")


def main(user_date: str, operations: list, operations_df: pd.DataFrame, user_category: str) -> None:
    """Вызывает результаты всех реализованных функций"""
    print(web_main(user_date))
    print(transactions_phone_numbers(operations))
    print(spending_by_category(operations_df, user_category, user_date))


if __name__ == "__main__":
    main("2021-12-30 17:50:17", transactions, transactions_df, "Пополнение")
