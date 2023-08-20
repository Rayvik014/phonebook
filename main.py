from sys import exit

# --Настройки отображения записей:

RECORDS_ON_LIST = 7  # Количество записей на одной странице телефонной книги
CHARS_FOR_ID = 3  # Количество зарезервированных символов для отображения поля ID
CHARS_FOR_COMPANY = 20  # Количество зарезервированных символов для названия компании
CHARS_FOR_NAME = 40  # Количество зарезервированных символов для ФИО
CHARS_FOR_PHONE = 13  # Количество зарезервированных символов для телефона (13 - чтобы вместился заголовок)


def get_id():
    """Функция нахождения уникального ID для записи.
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


def phone_validation(number: str):
    """Функция валидации вводимого номера телефона.
    Принимает номер телефона в виде строки.
    Проверяет наличие 11 знаков, а также только ли цифры содержатся в значении.
    Возвращает флаг - прошла или нет проверку, а также сообщение для пользователя"""
    message = ""
    valid_flag = True
    if len(number) != 11:
        message = "Введите номер в формате 7кодххххххх - всего 11 цифр"
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


class PhoneRecord:
    """Класс записи в телефонной книге. Инициализирует элементы в нужном виде
    """
    organization = ""
    name = ""
    surname = ""
    fname = ""
    phone_work = ""
    phone_personal = ""

    def make_record(self, record_id=get_id()):
        """Функция подготовки данных для записи в файл.
        Возвращает готовую строку для записи в файл
        """
        record = (f"{record_id},{self.organization},{self.name},{self.surname},"
                  f"{self.fname},{self.phone_work},{self.phone_personal};\n")
        return record

    @staticmethod
    def read_record(record):
        """Функция разбивает записанные в файл строки по переменным
        Возвращает список
        """
        x = 0
        context = [""] * 7
        for char in record:
            if char != ",":
                if char == ";":
                    break
                context[x] += char
            else:
                x += 1
        return context

    @staticmethod
    def combine_record(context):
        """Функция подготовки строки для вывода на экран"""
        record = (f"{context[0].rjust(CHARS_FOR_ID, ' ')} {context[1].center(CHARS_FOR_COMPANY, ' ')} "
                  f"{(context[3] + ' ' + context[2] + ' ' + context[4]).center(CHARS_FOR_NAME, ' ')}"
                  f"{context[5].center(CHARS_FOR_PHONE, ' ')} {context[6].center(CHARS_FOR_PHONE, ' ')}")
        return record


class PhoneBook:
    """Телефонная книга с основными функциями для взаимодействия"""

    @staticmethod
    def editing(record):
        """Функция последовательно предлагает на ввод поля, если данные в полях уже есть, выводит их
        На вход принимает объект PhoneRecord
        """
        both_valid_flag = False
        while not both_valid_flag:
            valid_flag = False
            while not valid_flag:
                record.organization = str(input(f'Организация: {record.organization} ')) or record.organization
                valid_flag, message = text_validation(record.organization)
                print(message) if not valid_flag else None
            valid_flag = False
            while not valid_flag:
                record.name = str(input(f'Имя: {record.name} ')) or record.name
                valid_flag, message = text_validation(record.name)
                print(message) if not valid_flag else None
            if record.organization != "" or record.name != "":
                both_valid_flag = True
            else:
                print("Оба поля - Имя и Организация - не могут быть пустыми, заполните пожалуйста")

        valid_flag = False
        while not valid_flag:
            record.surname = str(input(f'Фамилия: {record.surname} ')) or record.surname
            valid_flag, message = text_validation(record.surname)
            print(message) if not valid_flag else None
        valid_flag = False
        while not valid_flag:
            record.fname = str(input(f'Отчество: {record.fname} ')) or record.fname
            valid_flag, message = text_validation(record.fname)
            print(message) if not valid_flag else None

        both_valid_flag = False
        while not both_valid_flag:
            valid_flag = False
            while not valid_flag:
                record.phone_work = str(input(f"Рабочий телефон: {record.phone_work} ")) or record.phone_work
                valid_flag, message = phone_validation(record.phone_work)
                print(message) if not valid_flag else None
            valid_flag = False
            while not valid_flag:
                record.phone_personal = str(input(f"Личный телефон: {record.phone_personal} ")) or record.phone_personal
                valid_flag, message = phone_validation(record.phone_personal)
                print(message) if not valid_flag else None
            if record.phone_work != "" or record.phone_personal != "":
                both_valid_flag = True
            else:
                print("Оба поля номера телефона не могут быть пустыми, заполните пожалуйста")

    def add_record(self):
        """Добавить запись в книгу.
        Предлагает добавить новую запись, присваивает ID записи, записывает результат в файл
        """
        new_record = PhoneRecord()
        print("Создание новой записи:")
        self.editing(new_record)
        with open('phonebase.txt', "at") as phonebase:
            phonebase.write(new_record.make_record())
        print('\nЗапись добавлена в книгу')
        self.user_menu()

    def edit_record(self, selected_record):
        """Функция редактирования записи"""
        with open('phonebase.txt', 'rt') as phonebase:
            for line_number, line in enumerate(phonebase):
                record_id = ""
                for char in line:
                    if char.isdigit():
                        record_id += char
                    else:
                        break
                if record_id == selected_record:
                    record = PhoneRecord()
                    record_context = record.read_record(line)
                    record_line_number = line_number
                    break
        record.organization = record_context[1]
        record.name = record_context[2]
        record.surname = record_context[3]
        record.fname = record_context[4]
        record.phone_work = record_context[5]
        record.phone_personal = record_context[6]
        self.editing(record)
        with open('phonebase.txt', 'rt') as phonebase:
            lines = phonebase.readlines()
        with open('phonebase.txt', 'wt') as phonebase:
            for line_number, line in enumerate(lines):
                if line_number == record_line_number:
                    phonebase.write(record.make_record(int(record_context[0])))
                else:
                    phonebase.write(line)
        self.show_phone_book(1)

    def delete_record(self, selected_record_plus_d):
        """Функция удаления записи из базы"""
        selected_record = selected_record_plus_d[0:-1]
        user_answer = "_"
        while user_answer not in "yn":
            user_answer = input(f'\nВы действительно хотите удалить запись {selected_record}? (y/n)')
        if user_answer.lower() == "y":
            deleting_line_number=-1
            with open('phonebase.txt', 'rt') as phonebase:
                lines = phonebase.readlines()
                for line_number, line in enumerate(lines):
                    record_id = ""
                    for char in line:
                        if char.isdigit():
                            record_id += char
                        else:
                            break
                    if record_id == selected_record:
                        deleting_line_number = line_number
            with open('phonebase.txt', 'wt') as phonebase:
                for line_number, line in enumerate(lines):
                    if line_number == deleting_line_number:
                        continue
                    else:
                        phonebase.write(line)
            print(f'\nЗапись {selected_record} былв удалена\n')
        self.show_phone_book(1)

    def find_record(self):
        """Функция поиска по базе"""
        print("Поиск записей по параметру или комбинации параметров.\n\n"
              "Введите последовательно информацию для поиска, можно вводить не полностью, поиск будет произведен\n"
              "по первым символам\n")
        record_id = input('ID:  ')
        record_organization, record_name, record_surname = '', '', ''
        record_fname, record_phone_work, record_phone_personal = '', '', ''
        if not record_id:
            record_organization = input('Организация:   ')
            record_name = input('Имя:   ')
            record_surname = input('Фамилия:   ')
            record_fname = input('Отчество:   ')
            record_phone_work = input('Рабочий телефон:   ')
            record_phone_personal = input('Личный телефон:   ')
        print(self.shapka())
        with open('phonebase.txt', 'rt') as phonebase:
            for line in phonebase:
                context = PhoneRecord.read_record(line)
                if context[0] == record_id:
                    print(PhoneRecord.combine_record(context))
                if (record_organization.lower() in context[1][0:len(record_organization)].lower() and
                        record_name.lower() in context[2][0:len(record_name)].lower() and
                        record_surname.lower() in context[3][0:len(record_surname)].lower() and
                        record_fname.lower() in context[4][0:len(record_fname)].lower() and
                        record_phone_work.lower() in context[5][0:len(record_phone_work)].lower() and
                        record_phone_personal.lower() in context[6][0:len(record_phone_personal)].lower()):
                    print(PhoneRecord.combine_record(context))
        self.user_menu()

    def show_phone_book(self, page_number):
        """Отображение книги на экране. Принимает на вход номер страницы, вызывает сама себя при перелистывании"""
        have_forw_list_bool, have_back_list_bool, ids_list = self.combine_records_for_view(page_number)
        users_choice_list = []
        users_choice = "_"
        while users_choice.lower() not in users_choice_list:
            if have_forw_list_bool:
                users_choice_list.append("x")
            else:
                if "x" in users_choice_list:
                    users_choice_list.remove("x")
            if have_back_list_bool:
                users_choice_list.append("z")
            else:
                if "z" in users_choice_list:
                    users_choice_list.remove("z")

            users_choice = input()
            if users_choice.lower() == "x":
                if users_choice.lower() in users_choice_list:
                    page_number += 1
                    self.show_phone_book(page_number)
                else:
                    continue
            if users_choice.lower() == "z":
                if users_choice.lower() in users_choice_list:
                    page_number -= 1
                    self.show_phone_book(page_number)
                else:
                    continue
            if users_choice.lower() == "q":
                PhoneBook().user_menu()
            if users_choice in ids_list:
                self.edit_record(users_choice)
            deleting_list = []
            for ids in ids_list:
                deleting_list.append(str(ids) + "d")
            if users_choice.lower() in deleting_list:
                self.delete_record(users_choice)

    @staticmethod
    def shapka():
        naming = ["ID", "Организация", "ФИО", "Рабочий тел", "Личный тел"]
        shapka = (f"\n{naming[0].center(CHARS_FOR_ID, ' ')} {naming[1].center(CHARS_FOR_COMPANY, ' ')} "
                  f"{naming[2].center(CHARS_FOR_NAME, ' ')}"
                  f"{naming[3].center(CHARS_FOR_PHONE, ' ')} {naming[4].center(CHARS_FOR_PHONE, ' ')}")
        return shapka

    def combine_records_for_view(self, page_number):
        """Получает на вход номер стрницы для отображения.
        Формирует список записей для отображения, форматирует их, выводит шапку и подвал с инструкциями
        Возвращает BOOL есть ли предыдущая и следующая страницы, а также список ID выведенных записей,
        чтобы их можно было редактировать.
        """
        shapka = self.shapka()
        print(shapka)
        print("-" * len(shapka))
        have_back_list = ""
        have_forw_list = ""
        ids_list = []
        have_back_list_bool = False
        have_forw_list_bool = False
        with (open("phonebase.txt", "rt") as phonebase):
            for line_number, record in enumerate(phonebase):
                context = PhoneRecord.read_record(record)
                ids_list.append(context[0])
                if page_number > 1:
                    have_back_list = "Z - листать назад"
                    have_back_list_bool = True
                if RECORDS_ON_LIST * page_number > line_number >= RECORDS_ON_LIST * (page_number - 1):
                    print(PhoneRecord.combine_record(context))
                if line_number == RECORDS_ON_LIST * page_number:
                    have_forw_list = "X - листать вперед"
                    have_forw_list_bool = True
                    break
        podval = (f"{'-' * len(shapka)}\nСтр.{page_number}     {have_back_list}      {have_forw_list}\n"
                  f"Чтобы редактировать запись, введите ее ID     Q - Для выхода в меню\n"
                  f"Чтобы удалить запись, введите ее ID, а также букву d")
        print(podval)
        return have_forw_list_bool, have_back_list_bool, ids_list

    def user_menu(self):
        """Основное меню программы"""
        print('\nТЕЛЕФОНАЯ КНИГА\n\n'
              '1. Просмотр и редактирование\n'
              '2. Добавить запись\n'
              '3. Поиск записей\n'
              '4. Выход\n')
        user_choice = 0
        while user_choice not in {"1", "2", "3", "4"}:
            user_choice = input('Введите номер пункта и нажмите ENTER\n')
            print('Такого пункта нет, попробуйте снова') if user_choice not in {"1", "2", "3", "4"} else None
        if user_choice == "1":
            self.show_phone_book(page_number=1)
        if user_choice == "2":
            self.add_record()
        if user_choice == "3":
            self.find_record()
        if user_choice == "4":
            print("Вы вышли из программы")
            exit()


if __name__ == '__main__':
    PhoneBook().user_menu()
