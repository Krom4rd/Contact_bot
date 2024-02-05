from collections import UserDict
from datetime import date

def value_error_decorator(inner):
    def wraper(*args):
        try:
            return inner(*args)
        except ValueError:
            return 'ValueError'
    return wraper


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self)->str:
        return self._value

    @value.setter
    def value(self, value: str)-> None:
        self._value = value

    def __str__(self):
        return str(self._value)

class Birthday(Field):

    @Field.value.setter
    def value(self, value: str)-> None:
        if value is None:
            self._value = ''
        else: 
            try:       
                day, month, year = value.split('.') 
                birthday_date = date(year=int(year), month=int(month), day=int(day))
                self._value = birthday_date
            except ValueError:
                raise ValueError('Date of birthday is not valid! (dd.mm.yyyy)')

class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        self.name = name.title()


class Phone(Field):
    def __init__(self, phone: str()):
        super().__init__(phone)
        if len(phone) == 10 and phone.isdigit():
            self.phone = int(phone)
        else:
            raise ValueError


class Record():
    def __init__(self, name:str, phone:str=None, birthday:str=None):
        self.name = Name(name)
        self.phones = []

        if phone is not None:
            self.add_phone(phone)

        if birthday is not None:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = Birthday(None)


    @value_error_decorator
    def add_phone(self, phone: str):
        '''Phone number must be 10 numbers long'''
        if len(phone) == 10:
            self.phones.append(Phone(phone))
        else:
            self.value = phone

    @value_error_decorator
    def remove_phone(self, phone):
        '''Phone number must be 10 numbers long'''
        num_index = []
        if [num_index.append(self.phones.index(x)) for x in self.phones if x.phone == int(phone)]:
            self.phones.pop(*num_index)
        else:
            print(f'{phone} not detected')

    def edit_phone(self, old_phone, phone):
        '''Phone number must be 10 numbers long'''
        num_index = []
        if [num_index.append(self.phones.index(x)) for x in self.phones if x.phone == int(old_phone)]:
            self.phones.pop(*num_index)
            self.phones.insert(*num_index, Phone(phone))
        else:
            raise ValueError('Phone not detected')

    @value_error_decorator
    def find_phone(self, phone=None):
        '''Phone number must be 10 numbers long'''
        if phone is None:
            return ', '.join(str(x.phone) for x in self.phones)
        elif int(phone) in [x.phone for x in self.phones]:
            return Phone(phone)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday.value == '':
            return None
        today = date.today()
        actual_birthday = self.birthday.value.replace(year=today.year)
        if actual_birthday < today:
            actual_birthday = self.birthday.value.replace(year=today.year+1)
        time_to_birthday = abs(actual_birthday - today)

        return time_to_birthday.days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    iter_records = 5

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        
    def __iter__(self):
        self.idx = 0
        self.page = 0
        self.list_of_records = [record for record in self.data]

        return self

    def __next__(self):

        if self.idx >= len(self.data):
            raise StopIteration
        self.count_records = 1
        self.page += 1
        self.result = f'Page: {self.page}'

        while self.count_records <= self.iter_records:
            if self.idx >= len(self.data):
                return self.result
            
            self.result += f'\n{self.data[self.list_of_records[self.idx]]}'
            self.count_records += 1
            self.idx += 1
                
        return self.result
    
    def set_iter_records(self, iter_records):
        self.iter_records = iter_records

        
    def __str__(self):

        if not self.data:
            return 'The phone dictionary is empty'
        else:
            self.result = 'The phone dictionary has next contacts:'
            for record in self.data:
                self.result += f'\n{str(self.data[record])}'
            self.result += '\n'

            return self.result

if __name__ == '__main__':

    print('----- Phone(Field)')
    phone = Phone('0123456789')
    print(phone.value)

    phone.value = '9876543210'
    print(phone.value)

    print('----- Birthday(Field)')
    birthday = Birthday('12.05.1990')
    print(birthday.value)

    birthday.value = '12.05.2023'
    print(birthday.value)

    print('----- Name(Field)')
    name = Name('Vitalii')
    get_name = name.value
    print(get_name)

    name.value = 'Bob'
    print(name.value)

    print('----- Record: add phone')
    bob_record = Record('Bob')
    bob_record.add_phone('0123456789')
    bob_record.add_phone('0001112233')
    print(bob_record)

    print('----- Record: edit phone')
    bob_record.edit_phone('0123456789', '0000000000')
    print(bob_record)
    # bob_record.edit_phone('1111111111', '0000000000')

    print('----- Record: add birthday')
    bob_record.add_birthday('30.09.1990')
    print(bob_record)

    print('----- Record: days_to_birthday')
    days = bob_record.days_to_birthday()
    print(days)

    print('----- AddressBook: Iter')
    # Створення нової адресної книги
    book = AddressBook()
    book.add_record(Record(name='Vitalii', phone='0000000000', birthday='12.05.1990'))
    book.add_record(Record(name='Tom', phone='1111111111', birthday='03.02.1977'))
    book.add_record(Record(name='Jane', phone='2222222222', birthday='06.01.1986'))
    book.add_record(Record(name='John', phone='3333333333'))
    book.add_record(Record(name='Andry', phone='4444444444', birthday='17.09.1980'))
    book.add_record(Record(name='Lisa', phone='5555555555', birthday='04.07.1975'))
    book.add_record(Record(name='Natasha', phone='6666666666', birthday='01.11.1991'))
    book.add_record(Record(name='Ira', phone='7777777777', birthday='09.10.1993'))
    book.add_record(Record(name='Vasya', phone='8888888888', birthday='09.05.1965'))
    book.add_record(Record(name='Ivan', phone='9999999999', birthday='21.04.1968'))
    book.add_record(Record(name='Stas', phone='0123456789', birthday='29.03.1974'))
    book.add_record(Record(name='Sasha', phone='9876543210'))
    book.add_record(Record(name='Marina', phone='1234567890', birthday='30.06.1976'))
    book.add_record(Record(name='Boston', phone='0987654321', birthday='10.09.1993'))
    book.add_record(Record(name='Vadim', phone='2345678901', birthday='12.10.1989'))
    book.add_record(Record(name='Oleg', phone='1098765432', birthday='13.01.1978'))
    book.add_record(Record(name='Valera', phone='3456789012', birthday='10.02.1974'))
    book.add_record(Record(name='Anya', phone='2109876543', birthday='15.08.1991'))
    book.add_record(Record(name='Kolya', phone='4567890123', birthday='16.03.1993'))
    book.add_record(Record(name='Misha', phone='3210987654', birthday='08.01.1990'))
    print(book)


    print('----- AddressBook: Iter')
    # Кількість записів на сторінці по замовчуванню
    for line in book:
        print(line)

    # Кількість записів на сторінці змінюємо на 5
    book.set_iter_records(5)

    print('\n----- AddressBook: Повторний Iter')
    for line in book:
        print(line)
