"""Модуль містить опис моделей для роботи з контактами"""

import pickle
from collections import UserDict
from datetime import datetime
from my_utils import get_nearest_congratulation_day

class Field:
    """Клас відповідає за зберігання значення поля та його виведення."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """
    Клас для зберігання імені контакту.
    Це обов'язкове поле для кожного запису. Якщо ім'я не передано,
    викликається помилка.
    """
    def __init__(self, value):
        if not value:
            raise ValueError("Name is required")
        super().__init__(value)

class Phone(Field):
    """
    Клас для зберігання номера телефону.
    Має валідацію формату, перевіряє, щоб номер складався з
    10 цифр.
    """
    def __init__(self, value):
        if len(value.strip()) != 10 or not value.strip().isdigit():
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Birthday(Field):
    """
    Клас, що представляє дату народження. Успадковується від класу Field.
    При ініціалізації об'єкта цей клас перевіряє, чи є вхідне значення 
    в правильному форматі дати "DD.MM.YYYY". Якщо формат некоректний, 
    генерується виключення ValueError.
    """
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
        """
        Повертає рядкове представлення дати народження у форматі "DD.MM.YYYY".

        Повертає:
            str: рядок у форматі "DD.MM.YYYY", яка представляє дату народження.
        """
        return self.value

class Record:
    """
    Клас для зберігання інформації про контакт (ім'я та список телефонів).
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """
        Додає телефон до запису.

        Аргументи:
            phone (str): Номер телефону.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Видаляє телефон із запису.

        Аргументи:
            phone (str): Номер телефону.
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Редагує телефон у записі.

        Аргументи:
            old_phone (str): Старий номер телефону.
            new_phone (str): Новий номер телефону.

        Викидає:
            ValueError: Якщо старий телефон не знайдено.
        """
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        """Шукає телефон у записі.

        Аргументи:
            phone (str): Номер телефону.

        Викидає:
            str: Номер телефону, якщо знайдений, або None.
        """
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None
    

    def add_birthday(self, birthday):
        """Додає дату нароздення для запису.

        Аргументи:
            birthday (date): Номер телефону.
        """
        self.birthday = birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    """Клас для зберігання та управління записами в адресній книзі."""

    def add_record(self, record):
        """Додає запис до адресної книги.

        Аргументи:
            record (Record): Запис для додавання.
        """
        self.data[record.name.value] = record

    def find(self, name):
        """Шукає запис за ім'ям.

        Аргументи:
            name (str): Ім'я для пошуку.

        Повертає:
            Record: Запис, якщо знайдений, або None.
        """
        return self.data.get(name)

    def delete(self, name):
        """Видаляє запис за ім'ям.

        Аргументи:
            name (str): Ім'я для видалення.

        Викидає:
            ValueError: Якщо запис не знайдено.
        """
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record for {name} not found")

    def get_upcoming_birthdays(self, days = 7):
        """
        Повертає список записів з найближчими днями народження (протягом наступних X днів).
        Цей метод перевіряє всі записи в адресній книзі та знаходить ті, де найближчий день 
        народження припадає на наступні `days` днів від сьогоднішньої дати.

        Аргументи:
            days (int): Кількість днів вперед, протягом яких потрібно шукати дні народження. 
            За замовчуванням - 7 днів.

        Повертає:
            list: Список об'єктів класу Record, де день народження припадає на наступні `days` днів.
        """
        refined_records = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday is not None:
                user_birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                congratulation_day = get_nearest_congratulation_day(user_birthday, today)

                # Interval from today to user birthday
                days_to_birthday = (congratulation_day - today).days
                if days_to_birthday <= days:
                    refined_records.append({"record": record, 
                                            "congratulation_day": congratulation_day})

        return refined_records

    def save_data(self, filename="addressbook.pkl"):
        """
        Зберігає поточний стан адресної книги в файл.

        Аргументи:
            filename (str): Назва файлу, в який буде збережено стан адресної книги. За замовчуванням використовується "addressbook.pkl".
        """
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_data(cls, filename="addressbook.pkl"):
        """
        Завантажує адресну книгу з файлу.

        Аргументи:
            filename (str): Назва файлу, з якого буде завантажено дані. За замовчуванням використовується "addressbook.pkl".

        Повертає:
            AddressBook: Об'єкт класу `AddressBook`, який містить дані, завантажені з файлу. Якщо файл не знайдено, повертається новий об'єкт `AddressBook`.
        """
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()
