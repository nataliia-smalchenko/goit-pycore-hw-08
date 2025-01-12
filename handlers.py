"""Модуль містить функції для обробки роботи з контактами"""

from tabulate import tabulate
from my_utils import input_error
from models import Record, Birthday
from datetime import datetime

@input_error
def add_contact(args, book):
    """
    Додає новий контакт до списку контактів.

    Аргументи:
        args (list): Список з двох елементів: ім'я та номер телефону.
        contacts (dict): Словник контактів, де ключем є ім'я, а значенням - номер телефону.

    Повертає:
        str: Повідомлення про успішне додавання контакту.

    Викидає:
        ValueError: Якщо не надано ім'я або номер телефону, або контакт з таким ім'ям вже існує.
    """
    if len(args) < 2:
        raise ValueError("You did not provide a name or phone number.")
    if len(args) > 2:
        raise ValueError("You have specified more arguments than required.\n" \
                         "The command takes 2 arguments: name and phone number.")
    
    name, phone, *_ = args
    if name in book:
        raise ValueError(f"Contact with name {name} already added.")
    
    book.add_record(Record(name))
    book[name].add_phone(phone)
    return "Contact added."

@input_error
def change_contact(args, book):
    """
    Змінює існуючий контакт у списку контактів.

    Аргументи:
        args (list): Список з двох елементів: ім'я та новий номер телефону.
        contacts (dict): Словник контактів, де ключем є ім'я, а значенням - номер телефону.

    Повертає:
        str: Повідомлення про успішне оновлення контакту.

    Викидає:
        ValueError: Якщо не надано ім'я або номер телефону, або контакт з таким ім'ям не знайдений.
    """
    if len(args) < 3:
        raise ValueError("You did not provide a name, old phone number or new phone number.")
    if len(args) > 3:
        raise ValueError("You have specified more arguments than required.\n" \
                         "The command takes 2 arguments: name and phone number.")

    name, old_phone, new_phone = args
    if name not in book:
        raise ValueError(f"There is no contact with name {name}.")

    book.data[name].edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book):
    """
    Показує номер телефону для вказаного контакту.

    Аргументи:
        args (list): Список з одним елементом - ім'я контакту.
        contacts (dict): Словник контактів, де ключем є ім'я, а значенням - номер телефону.

    Повертає:
        str: Номер телефону для зазначеного контакту.

    Викидає:
        ValueError: Якщо не надано ім'я або контакт з таким ім'ям не знайдений.
    """
    if len(args) < 1:
        raise ValueError("You did not provide a name.")
    if len(args) > 1:
        raise ValueError("You have specified more arguments than required.\n" \
                         "The command takes only 1 argument: name.")

    name = args[0]
    if name not in book:
        raise ValueError(f"There is no contact with name {name}.")

    return ', '.join(p.value for p in book.data[name].phones)

@input_error
def show_all(book):
    """
    Показує всі контакти в списку.

    Аргументи:
        contacts (dict): Словник контактів, де ключем є ім'я, а значенням - номер телефону.

    Повертає:
        str: Створену таблицю з усіма контактами у форматі "Name | Phone".
    """
    contacts_list = [
        (name, ', '.join(p.value for p in book.data[name].phones), book.data[name].birthday)
          for name in book.data
    ]
    return tabulate(contacts_list, headers=("Name", "Phone"), tablefmt="fancy_grid")

@input_error
def add_birthday(args, book):
    """
    Додає дату народження для конкретного контакту.

    Аргументи:
        args (list): Список з двох елементів: ім'я контакту та дата народження у форматі "DD.MM.YYYY".
        book (AddressBook): Об'єкт адресної книги.

    Повертає:
        str: Повідомлення про успішне додавання дати народження.

    Викидає:
        ValueError: Якщо не надано ім'я або дату народження, або контакт з таким ім'ям не знайдений.
    """
    if len(args) < 2:
        raise ValueError("You did not provide a name or birthday.")
    if len(args) > 2:
        raise ValueError("You have specified more arguments than required.\n" \
                         "The command takes 2 arguments: name and birthday.")
    
    name, birthday_str = args
    if name not in book:
        raise ValueError(f"There is no contact with name {name}.")
    
    # Додаємо дату народження
    try:
        book.data[name].add_birthday(Birthday(birthday_str))
    except ValueError as e:
        raise ValueError(f"Invalid birthday format. Use DD.MM.YYYY.") from e

    return f"Birthday for {name} added successfully."

@input_error
def show_birthday(args, book):
    """
    Показує дату народження для вказаного контакту.

    Аргументи:
        args (list): Список з одним елементом — ім'я контакту.
        book (AddressBook): Об'єкт адресної книги.

    Повертає:
        str: Дата народження для зазначеного контакту.

    Викидає:
        ValueError: Якщо не надано ім'я або контакт з таким ім'ям не знайдений, або дата народження не вказана.
    """
    if len(args) < 1:
        raise ValueError("You did not provide a name.")
    if len(args) > 1:
        raise ValueError("You have specified more arguments than required.\n" \
                         "The command takes only 1 argument: name.")

    name = args[0]
    if name not in book:
        raise ValueError(f"There is no contact with name {name}.")

    record = book.data[name]
    if record.birthday is None:
        raise ValueError(f"There is no birthday for {name}.")

    return f"Birthday of {name} is {record.birthday}."

@input_error
def birthdays(args, book):
    """
    Показує список контактів з найближчими днями народження.

    Аргументи:
        args (list): Список з кількості днів для пошуку найближчих днів народження (за замовчуванням 7).
        book (AddressBook): Об'єкт адресної книги.

    Повертає:
        str: Список контактів з найближчими днями народження у форматі таблиці.

    Викидає:
        ValueError: Якщо аргумент з кількістю днів не є числом.
    """
    days = 7  # Значення за замовчуванням

    if args:
        try:
            days = int(args[0])
        except ValueError:
            raise ValueError("Please provide a valid number of days.")

    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if not upcoming_birthdays:
        return f"No upcoming birthdays within the next {days} days."

    contacts_list = [
        (record["record"].name, ', '.join(p.value for p in record["record"].phones), record["record"].birthday, record["congratulation_day"].strftime("%d.%m.%Y"))
          for record in upcoming_birthdays
    ]
    return tabulate(contacts_list, headers=("Name", "Phone", "Birthday", "Congratulation day"), tablefmt="fancy_grid")