import json

from src.utils import (currency_rates, get_data_excel, greeting_user, operations_cards, sort_date_operations,
                       stock_prices, top_five)


def web_main(date: str) -> json:
    """Возвращает JSON для главной Веб-страницы"""
    operations = get_data_excel("../data/operations.xlsx")
    operations = sort_date_operations(operations, date)
    result = {
        "greeting": greeting_user(),
        "cards": operations_cards(operations),
        "top_transactions": top_five(operations),
        "currency_rates": currency_rates(),
        "stock_prices": stock_prices(),
    }
    return json.dumps(result, ensure_ascii=False)