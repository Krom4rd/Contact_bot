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
                print('Date of birthday is not valid! (dd.mm.yyyy)')

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
            return 'This contact not have date of birthday'
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

    def global_find(self, string: str):
        if not string:
            return
        result = AddressBook()
        for k,v in self.data.items():
            if v.name.value.lower().find(string[0].lower()) != -1:
                result.add_record(v)
                continue
            for phone in v.phones:
                if phone.value.find(string[0]) != -1:
                    result.add_record(v)
        if len(result) >= 1:
            return result
        else:
            return 

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

