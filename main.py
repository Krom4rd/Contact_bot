import pathlib


# Кеш для контактів
cache = {}


# Функція декоратор для обробки помилок
def input_error(inner):
    def wrap(*args):
        try:
            return inner(*args)
        except IndexError:
            return "Give me name and phone please"
        except ValueError:
            return "Give me name and phone please"
        except KeyError:
            return "Give me name and phone please"
        except TypeError:
            return "Give me name and phone please"
    return wrap


# Функція привітання для команди "hello"
@input_error
def greating(data):
    return 'How can I help you?'


# Функція додавання нового контакту "add ..."
@input_error
def add_contact(data):
    # Поділ списку data на дві змінні name ,number
    name, number = data
    # Вилучить з номера телефону всі символи крім цифр
    number = ''.join(n for n in number if n.isdigit())
    # Перевірка на наявність контакту з таким імям
    if name in cache.keys():
        return f"Contact with name: {name} already present in cache,\n\
use command 'change' to replace number for this name"
    # Запис нового контакту в кеш
    if len(number):
        cache[name] = number
        return f"Contact with name:'{name}', number:'{number}' appened"
    else:
        return f'Number must consist of numbers only'


# Функція для заміни номера телефону для контакту "change ..."
@input_error
def change_number(data):
    name, number = data
    number = ''.join(n for n in number if n.isdigit())
    # Перевірка на наявність контакту з таким імям
    if name in cache.keys():
        # Старий номер
        old_number = cache[name]
        # Заміна номера
        cache[name] = number
        return f'Contact with name: "{name}" replace phone number from:\
 "{old_number}" to "{number}"'
    # Якщо не існує контакту з таким імям поверне повідомлення
    else:
        return f'Contact with name: {name} not detected in cache,\n\
use command "add" to added new contact'


# Функція для виведення потрібного номера за Імям контакту "phone ..."
@input_error
def phone_output(data):
    name = data[0]
    if name in cache.keys():
        return f"Contact: {name}, phone number: {cache[name]}"
    else:
        return f'Contact with name: {name} not deected in cache,\n\
use command "add" to added new contact'


# Функція для виведення всієї контактної книги в косоль "show all"
@input_error
def show_all(data):
    if cache:
        return '\n'.join(f'Contact: {name} - phone number: {cache[name]}' for name in cache)
    else:
        return 'Contacts list empty'


# Функція яка виведе в консоль інформацію про всі доступні функції "about"
@input_error
def about(data):
    return '"hello", відповідає у консоль "How can I help you?"\n\
-"add ...". За цією командою бот зберігає у пам\'яті новий контакт.\n\
    Замість ... користувач вводить ім\'я та номер телефону, обов\'язково через пробіл.\n\
-"change ..." За цією командою бот зберігає в пам\'яті новий номер телефону існуючого контакту.\n\
    Замість ... користувач вводить ім\'я та номер телефону, обов\'язково через пробіл.\n\
    Переданий аргумент "номер телефону" відкидає любі символи крім цифр.\n\
-"phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту.\n\
    Замість ... користувач вводить ім\'я контакту, чий номер треба показати.\n\
-"show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.\n\
-"delete ..." За цією командою бот видалить з пам\'яті контакт.\n\
    Замість ... користувач вводить ім\'я контакту який треба видалити.\n\
-"good bye", "close", "exit" по будь-якій з цих команд бот коректно завершує свою роботу виведе у консоль "Good bye!".\n\
    При коректнову завершенні роботи програми кеш буде збережено та при повторному виклику програми кеш буде відновлено.'


# Функція для видалення контакту за імям
@input_error
def delete(name):
    if name in cache.keys():
        cache.pop(name)
        return f'Contact with name: "{name}" deleted.'


# Функція яка перетворює введені користувачем данні на список
# для коректної роботи функцій
@input_error
def func_data(user_input):
    for key, value in COMMANDS.items():
        if user_input[0].lower() in value and len(user_input) > 2:
            return key, [user_input[1].lower().capitalize(), user_input[2]]
        elif user_input[0].lower() in value and len(user_input) == 2:
            return key, user_input[1].lower().capitalize()
        elif user_input[0].lower() in value and len(user_input) <= 1:
            return key, None


# Функція для пошуку команди в COMMANDS
@input_error
def command_cheker(command):
    # Поділ переданих данних користувачем через пробіл
    command_list = command.split()
    # Пустий рядок переданий користувачем
    if not command_list:
        return 'continue'
    # 'exit', 'good bye', 'close' вихід з програми
    if command_list[0].lower() in COMMANDS[exit]:
        return 'Good bye'
    # Існуюча команда продовжить роботу над переданими данними
    elif command_list[0].lower() in COMMANDS.values():
        return command_list
    # Якщо не було знайдено переданої команди
    # буде перевіряти список команд за двома значеннями переданими користувачем
    elif str(' '.join(i.lower() for i in command_list if command_list[0:1])) in COMMANDS.values():
        # Зроблено для команди show all
        return [' '.join(i.lower() for i in command_list if command_list[0:1])]
    elif str(' '.join(i.lower() for i in command_list if command_list[0:1])) in COMMANDS[exit]:
        return 'Good bye'
    # Якщо буде передано незрозумілу команду виведе в консоль повідомлення
    else:
        return 'Sorry it\'s unknown command.\n\
Press command "about" to more information'


# Словник ключ = Функція, значення= Ключові слова для запуску функцій
COMMANDS = {
    greating: 'hello',
    add_contact: 'add',
    change_number: 'change',
    phone_output: 'phone',
    show_all: 'show all',
    exit: ['exit', 'good bye', 'close'],
    delete: 'delete',
    about: 'about'
}


# Функція для запису кешу в окремий файл для зберігання данних
@input_error
def save_cache():
    # Якщо кеш пустий та окремий файл для зберігання існує тоді файл буде видалено
    if not cache and pathlib.Path("memory.txt").exists():
        pathlib.Path("memory.txt").unlink()
        return None
    elif not cache:
        return None
    with open('memory.txt', 'w') as file:
        for key, value in cache.items():
            file.write(f'Name: {key},Number: {value}\n')


# Функія для відновлення кешу при повторному виклику програми
@input_error
def return_cache():
    with open('memory.txt', 'r') as file:
        for line in file.readlines():
            if not line.replace('\n', ''):
                continue
            splited_line = line.split(',')
            name = splited_line[0].replace('Name: ', '')
            number = splited_line[1].replace('Number: ', '').replace('\n', '')
            cache[name] = number


# Основна функція для порядку роботи та виведення даних в консоль
def main():
    # Якщо раніше використовувалася програма та було створено кеш: його буде відновлено
    if pathlib.Path("memory.txt").exists():
        return_cache()
    # Цикл для тривалої роботи програми
    while True:
        # Отримання даних від користувача
        user_input = command_cheker(input('>>> '))
        # Перевірка переданих даних
        if user_input == 'continue':
            continue
        elif user_input == 'Good bye':
            # Вихід з програми та запис кешу в окремий файл
            print('Good bye')
            save_cache()
            break
        elif isinstance(user_input, type(str())):
            print(user_input)
            continue
        # Запуск команд
        else:
            func, data = func_data(user_input)
            result = func(data)
            print(result)


if __name__ == '__main__':
    main()
