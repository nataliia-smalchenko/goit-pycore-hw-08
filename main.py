"""
Головний модуль для роботи з контактами, який відповіає за введення-виведення 
та керування виконанням відповідних операцій.
"""
from models import AddressBook
from handlers import add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays
from my_utils import parse_input

def main():
    """
    Головна функція, яка реалізує взаємодію з користувачем через командний інтерфейс.

    Запускає цикл, який чекає вводу команди від користувача та виконує відповідні дії.
    Завершує програму, коли користувач вводить команду "close" або "exit".
    """
    book = AddressBook.load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            book.save_data()
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
