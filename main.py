def get_id():
    """Функция для нахождения уникального ID для записи.
    Используется при создании новой записи
    """
    with open('phonebase.txt', "rt") as phonesbase:
        ids = set()
        for line in phonesbase:
            record_id = ""
            for char in line:
                if char.isdigit():
                    record_id += char
                else:
                    break
            if record_id == "":
                ids.add(-1)
            else:
                ids.add(int(record_id))
    new_id = 0
    while True:
        if new_id in ids:
            new_id += 1
        else:
            return new_id


class PhoneRecord:
    """Класс записи в телефонной книге. Инициалоизирует элементы в нужном виде
    """
    phone_work = ""
    phone_personal = ""
    organization = ""
    name = ""
    surname = ""
    fname = ""

    def make_record(self):
        """
        Функция подготовки данных для записи в файл
        Возвращает готовую строку для записи в файл
        """
        record = (f"{get_id()},{self.organization},{self.name},{self.surname},"
                  f"{self.fname},{self.phone_work},{self.phone_personal};\n")
        return record


def phone_validation(number: str):
    """Функция валидации вводимого номера телефона.
    Принимает номер телефона в виде строки.
    Проверяет наличие 11 знаков, а также только ли цифры содержатся в значении.
    Возвращает флаг - прошла или нет проверку, а также сообщение для пользователя"""
    message = ""
    valid_flag = True
    if len(number) != 11:
        message = "Введите номер в формате 7-код-ххххххх - всего 11 цифр"
        valid_flag = False
    elif not number.isdigit():
        message = "Номер телефона должен содержать только цифры"
        valid_flag = False
    if number == "":
        valid_flag = True
        return valid_flag, message
    return valid_flag, message


def text_validation(text: str):
    """Функция валидации вводимого текста.
    Принимает текст.
    Проверяет наличие в тексте запятых.
    Возвращает флаг - прошла или нет проверку, а также сообщение для пользователя
    """
    message = ""
    valid_flag = True
    if ',' in text:
        valid_flag = False
        message = "Не допускаются запятые в словах, попробуйте еще раз"
    return valid_flag, message


class PhoneBook:
    """Телефонноа/ книга с основными функциями для взаимодействия"""

    def add_record(self):
        """Добавить запись в книгу.
        Предлагает добавить новую запись, присваивает ID записи, записывает результат в файл
        """
        new_record = PhoneRecord()
        print("Создание новой записи:")

        while new_record.organization == "" and new_record.name == "":
            valid_flag = False
            while not valid_flag:
                new_record.organization = str(input('Организация:  '))
                valid_flag, message = text_validation(new_record.organization)
                print(message) if not valid_flag else None
            valid_flag = False
            while not valid_flag:
                new_record.name = str(input('Имя:  '))
                valid_flag, message = text_validation(new_record.name)
                print(message) if not valid_flag else None
            if new_record.organization != "" or new_record.name != "":
                break
            print("Оба поля - Имя и Организация - не могут быть пустыми, заполните пожалуйста")

        valid_flag = False
        while not valid_flag:
            new_record.surname = str(input('Фамилия:  '))
            valid_flag, message = text_validation(new_record.surname)
            print(message) if not valid_flag else None
        valid_flag = False
        while not valid_flag:
            new_record.fname = str(input('Отчество:  '))
            valid_flag, message = text_validation(new_record.fname)
            print(message) if not valid_flag else None

        while new_record.phone_work == "" and new_record.phone_personal == "":
            valid_flag = False
            while not valid_flag:
                new_record.phone_work = str(input("Рабочий телефон:  "))
                valid_flag, message = phone_validation(new_record.phone_work)
                print(message) if not valid_flag else None
            valid_flag = False
            while not valid_flag:
                new_record.phone_personal = str(input("Личный телефон:  "))
                valid_flag, message = phone_validation(new_record.phone_personal)
                print(message) if not valid_flag else None
            if new_record.phone_work != "" or new_record.phone_personal != "":
                break
            print("Оба поля номера телефона не могут быть пустыми, заполните пожалуйста")

        with open('phonebase.txt', "at") as phonebase:
            phonebase.write(new_record.make_record())

        print('\nЗапись добавлена в книгу')
        self.user_menu()

    def edit_record(self):
        pass

    def find_record(self):
        pass

    def show_phone_book(self):
        pass

    def user_menu(self):
        print('\nТЕЛЕФОНАЯ КНИГА\n\n'
              '1. Просмотр и редактирование\n'
              '2. Добавить запись\n'
              '3. Поиск записей\n')
        user_choice = 0
        while user_choice not in {"1", "2", "3"}:
            user_choice = input('Введите номер пункта и нажмите ENTER\n')
            print('Такого пункта нет, попробуйте снова') if user_choice not in {"1", "2", "3"} else None
        if user_choice == "1":
            self.show_phone_book()
        if user_choice == "2":
            self.add_record()
        if user_choice == "3":
            self.find_record()


if __name__ == '__main__':
    PhoneBook().user_menu()
