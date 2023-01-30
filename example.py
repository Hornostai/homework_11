from collections import UserDict
from datetime import datetime, timedelta


class Field:  # батько для Name, Phone
    def __init__(self, value):
        self.value = value
        self.__value = None

    def __repr__(self) -> str:
        return self.value  # тут треба просто self.value


class Name(Field):  # наслідується від FIeld і має вже поле value
    pass


class Phone(Field):  # наслідується від FIeld і має вже поле value
    """Перевірка робиться в сеттері, тобто ми створимо захищене поле
    self.__value і якщо перевірка пройде ми наше значення що прийшло запишемо в
    захищенне поле"""

    @property  # це геттер - він повертає захищенне поле
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if (
            len(value) == 10 and value.isdigit()
        ):  # тут перевірка телефона на довжину та щоб він був лише цифри
            self.__value = value
            # return self.__value # це не потрібно, сеттер нічого не повертає
        else:
            raise ValueError(f"Wrong number - number should have 10 symbols")

    #@value.setter
    #def value(self, value):
    #    if (
    #        len(value) == 10 and value.isdigit()
    #    ):  # тут перевірка телефона на довжину та щоб він був лише цифри
    #        self.__value = value
    #        # return self.__value # це не потрібно, сеттер нічого не повертає
    #    else:
    #        return f"Wrong number - number should have 10 symbols"


class Birthday(Field):
    @property  # це геттер - він повертає захищенне поле
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            bday = datetime.strptime(value, "%d.%m.%Y" )
            self.__value = value
        except TypeError:
            return f"Format your birthday is not correct"

        # """Тут зробіть перевірку на день народження якусь
        # і якщо пройде то пристоюйте self.__value = value"""


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        if (
            birthday
        ):  # тут логіка яка, якщо прийшоов День Народження - то записуємо, якщо немає - то пуста строка
            self.birthday = birthday
        else:
            self.birthday = ""

    def add_phone(self, phone: Phone) -> None:
        self.phones.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> str:
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return f"Phone for contact {self.name.value} change successful"
        return f"Contact {self.name.value} dont have phone {old_phone.value}"

    def days_to_birthday(self):
        birthday_date = datetime.strftime(self.birthday.value, "%d.%m.%Y")
        current_date = datetime.now()
        birthday_date = birthday_date.replace(year=current_date.year)
        delta_days = birthday_date - current_date

        target_bday = datetime.strftime(birthday_date, "%d-%B-%Y")

        if delta_days > 0:
            return f"{delta_days.days} days left before {target_bday}"
        else:
            birthday_date = birthday_date.replace(year=birthday_date.year + 1)
            delta_days = birthday_date - current_date
            return f"{delta_days.days} days left before {target_bday}"

    def __repr__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phones])} Birthday: {self.birthday}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def iterator(self, n=2):
        self.n = n  # це кількість записів на сторінці
        index = 1
        print_block = "-" * 50 + "\n"  # це типу строка для розділу сторінок
        for record in self.data.values():  # ітерується по записам record
            print_block += str(record) + "\n"
            if index < n:
                index += 1
            # якщо індекс більше числа н то повертаються записи (в нашому випадку два записи)
            else:
                yield print_block
                index, print_block = 1, "-" * 50 + "\n"
        yield print_block  # тут повертається все що залишилось

    def next(self, n=2):
        result = "List of all users:\n"
        # це наш ітератор(генератор більше тому що yield)
        print_list = self.iterator(n)
        for item in print_list:  # на кожній ітерації наш ітератор повертає по 2 записи
            result += f"{item}"  # ми іх збираємо в змінну і повертаємо
        return result


"""Функції для роботи консольного бота"""


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print("Give me name and phone please")
        except ValueError:
            print("Enter user name")
        except IndexError:
            print("Check your input and try again")
        except TypeError:
            print("typeerror")

    return wrapper


@input_error
def add_contact(*args: str, PHONE_VOCABULAR):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[2])
    rec = Record(name, phone, birthday)
    PHONE_VOCABULAR.add_record(rec)
    return f"Contact {name.value} with phone: {phone.value} and birthday {birthday.value} was created!"


@input_error
def simple_func(args: str):
    return args.upper()


def greeting():
    return "How can I help you?"


#@input_error
def show_all(PHONE_VOCABULAR,*args):
    if PHONE_VOCABULAR:
        #result = "List of all users:"
        #for key in PHONE_VOCABULAR:
        #    result += f"\n{PHONE_VOCABULAR[key]}"
        #return result
        return PHONE_VOCABULAR.next()
    return f"Phone Vocabulary don`t have contact now"


def exiting():
    print("Goodbye")


def unknown(*args):
    print("Command not exist")


@input_error
def change(*args, PHONE_VOCABULAR):
    rec = PHONE_VOCABULAR.get(args[0])
    if rec:
        old_phone = Phone(args[1])
        new_phone = Phone(args[2])
        return rec.edit_phone(old_phone, new_phone)
    return f"Contact with name {args[0]} not in AddressBook"


@input_error
def show_phone(*args, PHONE_VOCABULAR):
    rec = PHONE_VOCABULAR.get(args[0])
    if rec:
        return rec
    return f"Contact with name {args[0]} is not in the phone book"


COMMANDS = {
    greeting: ["hello"],
    add_contact: ["add", "додай", "+"],  # add + name + numer
    exiting: ["exit", "close", "."],
    change: ["change", "edit"],  # change + name + numer + new numer
    show_phone: ["phone"],  # phone + name
    show_all: ["show", "all"],
}


def command_parser(user_input: str):
    for command, key_words in COMMANDS.items():
        for key_word in key_words:
            if user_input.startswith(key_word):
                return command, user_input.replace(key_word, "").split()
    return unknown, None


def main():
    PHONE_VOCABULAR = AddressBook()  # створюємо обьект классу при виклику функції
    while True:
        user_input = input(">>> ")
        if user_input in COMMANDS[exiting]:
            exiting()
            break
        command, data = command_parser(user_input)
        if data:
            print(command(*data, PHONE_VOCABULAR=PHONE_VOCABULAR))
        else:
            print(command(PHONE_VOCABULAR))


if __name__ == "__main__":
    p1 = Phone(
        "1234512345"
    )  # в форматі 12345 - вже не проходить тести, томущо валідація на 10 симовлів
    p2 = Phone("1234512344")
    print(p1.value == p2.value)
    name = Name("Bill")
    phone = Phone("1234567890")
    birthday = Birthday("03.03.2003")
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)
    assert isinstance(ab["Bill"], Record)
    assert isinstance(ab["Bill"].name, Name)
    assert isinstance(ab["Bill"].phones, list)
    assert isinstance(ab["Bill"].phones[0], Phone)
    assert isinstance(ab["Bill"].birthday, Birthday)
    assert ab["Bill"].phones[0].value == "1234567890"
    print("All Ok)")  # тести пройшли
    """Командний бот"""

    main()
