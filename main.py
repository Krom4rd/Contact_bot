from classes import AddressBook, Record, Birthday
import pickle
import pathlib

cache = AddressBook()

# Функція декоратор для обробки помилок
def input_error(inner):
    def wrap(*args):
        try:
            return inner(*args)
        except IndexError:
            return "IndexError"
        except ValueError:
            return "ValueError"
        except KeyError:
            return "KeyError"
        except TypeError:
            return "TypeError"
        except ArithmeticError:
            return 'ArithmeticError'
    return wrap

# Функція привітання для команди "hello"
def greating(data):
    return 'How can I help you?'

@ input_error
def add_contact(data):
    # Поділ списку data на дві змінні name ,number
    name, number = data
    # Перетворює рядок з імям в необхідний формат
    name = name.lower().title()
    # Перевірка на наявність контакту з таким імям
    if cache.find(name):
        return f"Contact with name: {name} already present in cache,\n\
use command 'change' to replace number for this name"
    if len(number) != 10:
        return f'Phone number must be 10 numbers long'
    elif number.isdigit() == False:
        return f'Number must consist of numbers only'
    else:
        # Запис нового контакту в кеш
        cache.add_record(Record(name, number))
        return f"Contact with name:'{name}', number:'{number}' appened"

# Функція для заміни номера телефону для контакту "change ..."
@ input_error
def change_number(data):
    name, number = data
    name = name.lower().title()
    # Перевірка на наявність контакту з таким імям
    if not cache.find(name):
        return f'Contact with name: {name} not detected in cache,\n\
use command "add" to added new contact'
    if len(number) != 10:
        return f'Phone number must be 10 numbers long'
    elif number.isdigit() == False:
        return f'Number must consist of numbers only'
    else:
        # Старий номер
        old_number = cache.data[name].phones[:]
        # Заміна номера
        cache.delete(name)
        cache.add_record(Record(name, number))
        return f'Contact with name: "{name}" replace phone number from:\
"{old_number}" to "{number}"'

# Функція для виведення потрібного номера за збігом букв чи цифр контакту "phone ..."
@ input_error
def phone_output(data):
    return cache.global_find(data)

# Функція для виведення всієї контактної книги в косоль "show all"
def show_all(data):
    return cache

# Функція для видалення контакту за імям
@ input_error
def delete(data):
    # Перевірка на наявність контакту з таким імям
    if not cache.find(data[0].lower().title()):
        return f'Contact with name: {data[0].lower().title()} not detected in cache,\n\
use command "add" to added new contact'
    cache.delete(data[0].lower().title())
    return f'Contact with name: "{data[0].lower().title()}" deleted.'

# Функція яка виведе в консоль інформацію про всі доступні функції "about"
def about(data):
    return '"hello", відповідає у консоль "How can I help you?"\n\
-"add ...". За цією командою бот зберігає у пам\'яті новий контакт.\n\
    Замість ... користувач вводить ім\'я та номер телефону, обов\'язково через пробіл.\n\
-"change ..." За цією командою бот зберігає в пам\'яті новий номер телефону існуючого контакту.\n\
    Замість ... користувач вводить ім\'я та номер телефону, обов\'язково через пробіл.\n\
    Переданий аргумент "номер телефону" відкидає любі символи крім цифр.\n\
-"phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту.\n\
    Замість ... користувач вводить номер або ім\'яч контакту, чий номер треба показати.\n\
-"birthday ..." За цією командою бот зберігає день народження у пам\'яті для інуючого контакт.\n\
    Замість ... користувач вводить ім\'я та дату народження (дд.мм.рррр), обов\'язково через пробіл.\n\
-"days to birthday ..." За цією командою бот виводить у консоль кількість днів до наступного для народження для контакту.\n\
    Замість ... користувач вводить ім\'я.\n\
-"show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.\n\
-"delete ..." За цією командою бот видалить з пам\'яті контакт.\n\
    Замість ... користувач вводить ім\'я контакту який треба видалити.\n\
-"good bye", "close", "exit" по будь-якій з цих команд бот коректно завершує свою роботу виведе у консоль "Good bye!".\n\
    При коректнову завершенні роботи програми кеш буде збережено та при повторному виклику програми кеш буде відновлено.'

# Функція для додавання дня народження для контакту
@ input_error
def add_birthday(data):
    name, date = data
    name = name.lower().title()
    if not cache.find(name):
        return f'Contact with name: {name} not detected in cache,\n\
use command "add" to added new contact'
    cache[name].add_birthday(date)
    return f'Birthday for {name} added'

# Функція для обчислення та виведення в консоль кількість дні до наступного дня народження контакту
@ input_error
def days_to_birthday(data):
    if not cache.find(data[0].lower().title()):
        return f'Contact with name: {data[0].lower().title()} not detected in cache,\n\
use command "add" to added new contact'
    return cache[data[0].lower().title()].days_to_birthday()

# Функція для запису кешу в окремий файл для зберігання данних
def exit(data):
    # Якщо кеш пустий та окремий файл для зберігання існує тоді файл буде видалено
    if not cache and pathlib.Path('cache.bin').exists():
        pathlib.Path('cache.bin').unlink()
        return None
    with open('cache.bin', 'wb') as file:
        pickle.dump(cache, file)

# Функія для відновлення кешу при повторному виклику програми
def return_cache():
    with open('cache.bin', 'rb') as file:
        global cache
        cache = pickle.load(file)

# Словник ключ = Функція, значення= Ключові слова для запуску функцій
COMMANDS = {
    greating: 'hello',
    add_contact: 'add',
    change_number: 'change',
    phone_output: 'phone',
    show_all: 'show all',
    exit: ['exit', 'good bye', 'close'],
    delete: 'delete',
    about: 'about',
    add_birthday: 'birthday',
    days_to_birthday: 'days to birthday'
}

# Функція для пошуку команди в COMMANDS
def foo_separator(data):
    # Поділ переданих данних користувачем через пробіл
    comand_list = data.lower().split()
    for key, value in COMMANDS.items():
        if len(comand_list) == 1:
            if comand_list[0] == value:
                return key, None
            elif comand_list[0] in COMMANDS[exit]:
                return exit, None
        elif len(comand_list) == 2:
            if comand_list[0] == value:
                return key, comand_list[1:]
            elif comand_list[0] + ' ' + comand_list[1] == value:
                return key, None
            elif comand_list[0] + ' ' + comand_list[1] in COMMANDS[exit]:
                return exit, None
        elif len(comand_list) == 3:
            if comand_list[0] == value:
                return key, comand_list[1:]
            if comand_list[0] + ' ' + comand_list[1] == value:
                return key, comand_list[2]
        elif len(comand_list) > 3:
            if comand_list[0] + ' ' + comand_list[1] + ' ' + comand_list[2] == value:
                return key, comand_list[3:]
    # Якщо не було знайдено переданої команди
    return None, None

# Основна функція для порядку роботи та виведення даних в консоль
def main():
    # Якщо раніше використовувалася програма та було створено кеш: його буде відновлено
    if pathlib.Path('cache.bin').exists():
        return_cache()
    # Цикл для тривалої роботи програми
    while True:
        # Отримання даних від користувачаa
        user_input = input('>>>')
        if user_input:
            func, data = foo_separator(user_input)
        if func == None:
            continue
        elif func == exit:
            # Вихід з програми та запис кешу в окремий файл
            func(data)
            print('Good bye')
            break
        else:
            # Запуск команд
            result = func(data)
            print(result)

if __name__ == '__main__':
    main()