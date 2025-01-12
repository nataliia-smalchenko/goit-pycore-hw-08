"""Модуль містить додаткові функції"""
from functools import wraps
from datetime import timedelta, date
import calendar

def parse_input(user_input):
    """
    Розбиває введений рядок на команду та аргументи.

    Аргументи:
        user_input (str): Введений рядок з командою та аргументами.

    Повертає:
        tuple: Кортеж, де перший елемент — це команда (стрічка), 
               а решта елементів — це аргументи (список).
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    """
    Декоратор для обробки помилок при виклику функцій.

    Аргументи:
        func (callable): Функція, яку потрібно обгорнути.

    Повертає:
        callable: Обгорнуту функцію з обробкою помилок.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"

    return inner

def get_nearest_congratulation_day(user_birthday, today):
    """
    Визначає найближчий день для привітання з днем народження, враховуючи вихідні та високосні роки. Якщо день народження припадає на суботу чи неділю, метод коригує день на найближчий робочий день (понеділок або вівторок).

    Аргументи:
        user_birthday (date): Дата народження користувача.
        today (date): Поточна дата.

    Повертає:
        date: Найближчий день для привітання з днем народження, враховуючи всі корекції.
    """
    # Перевіряємо, чи є день народження 29 лютого
    if calendar.isleap(user_birthday.year) and user_birthday.month == 2 \
                    and user_birthday.day == 29:
        if calendar.isleap(today.year):
            # Якщо зараз високосний рік
            nearest_user_birthday = date(today.year, user_birthday.month, user_birthday.day)
            if nearest_user_birthday < today:
                nearest_user_birthday = date(today.year + 1, 3, 1)
        else:
            # Якщо зараз не високосний рік, день народження переноситься на 1 березня
            nearest_user_birthday = date(today.year, 3, 1)
            if nearest_user_birthday < today:
                if calendar.isleap(nearest_user_birthday.year):
                    nearest_user_birthday = date(today.year + 1, user_birthday.month, user_birthday.day)
                else:
                    nearest_user_birthday = date(today.year + 1, 3, 1)
    else:
        # Якщо день народження не 29 лютого, просто перевіряємо на найближчий день
        nearest_user_birthday = date(today.year, user_birthday.month, user_birthday.day)
        if nearest_user_birthday < today:
            nearest_user_birthday = date(today.year + 1, user_birthday.month, user_birthday.day)

    # Переносимо день привітання на робочий день, якщо він припадає на вихідний
    if nearest_user_birthday.weekday() == 5:
        congratulation_day = nearest_user_birthday + timedelta(days=2)
    elif nearest_user_birthday.weekday() == 6:
        congratulation_day = nearest_user_birthday + timedelta(days=1)
    else:
        congratulation_day = nearest_user_birthday

    # Повертаємо день для привітання
    return congratulation_day
