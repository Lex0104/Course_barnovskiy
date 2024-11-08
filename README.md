# Разработка приложения для анализа транзакций, которые находятся в Excel-файле. Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.

## Описание:
В курсовой были реализованы модули необходимые для реализации данной работы:
1) main.py - модуль представлен, как "Главный" модуль, в который были импортированы все функции для работы приложения
2) reports.py - модуль формирует отчет через функцию, так же согласно заданию были выведены затраты за последние 3 месяца
3) services.py - модуль формирует на возврат данных (транзакций) - был выбран путь "Поиск по номерам телефона"
4) views.py - модуль возвращает на для веб-страницы библиотеку JSON
5) utils.py - в модуле прописаны:
5.1) Данные о финансовых транзакциях из файла excel
5.2) Операции за текущий месяц
5.3) Приветствие в зависимости от времени суток
5.4) Возвращает данные по каждой карте
5.5) Представлены топ-5 транзакций по сумме платежа
5.6) Cтоимость акций S&P 500
5.7) Возвращает курсы валют

## Установка:
python3 -m venv venv - загрузка виртуального окружения
source ./venv/bin/activate - активация окружения
pip install pandas - установление пакет pandas в окружении
poerty install - установление менеджера пакетов (менеджер зависимостей)

1. Клонируйте репозиторий:
```
git@github.com:Lex0104/Course_barnovskiy.git
```
## Использование:
1) Загрузка файл с банковскими операциями в папку data в формате EXCEL.
2) Модуль services направлен на получения транзакций, через мобильные номера.
3) В модуле reports получены общие суммы трат по указанной категории в течении последних трёх месяцев.
Также можете использовать модуль main для получения результатов всех реализованных функций.
