import itertools
import json
import os

# Автор проекта: Емельянов Григорий Андреевич @emelyagr https://github.com/emelyagr
# Author of the project: Emelyanov Grigory Andreevich @emelyagr https://github.com/emelyagr -->


# Класс для хранения данных пользователя
class UserData:
    def __init__(self, social_id, last_name, first_name, middle_name, address, birth_year, hobbies):
        self.social_id = social_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.address = address
        self.birth_year = birth_year
        self.hobbies = hobbies

# Класс для генерации электронных почт и паролей и работы с историей
class EmailPasswordGenerator:
    def __init__(self):
        self.history = []
        self.history_id = 0
        self.history_file = "history.json"  # Путь к файлу истории
        self.load_history()

    # Загрузка истории из файла
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as file:
                self.history = json.load(file)
                if self.history:
                    self.history_id = max(record['id'] for record in self.history)
        else:
            self.save_history()

    # Сохранение истории в файл
    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(self.history, file, ensure_ascii=False, indent=4)

    # Генерация электронных почт на основе данных пользователя
    def generate_emails(self, user_data):
        domains = ["gmail.com", "yahoo.com", "outlook.com", "mail.ru", "yandex.ru", "rambler.ru", "vk.com"]
        parts = [
            user_data.first_name, 
            user_data.middle_name, 
            user_data.last_name, 
            str(user_data.birth_year)
        ]
        emails = set()
        
        # Генерация уникальных комбинаций для адресов электронной почты
        for comb in itertools.permutations(parts, 2):
            for domain in domains:
                email = f"{''.join(comb)}@{domain}"
                emails.add(email)
                if len(emails) >= 100:
                    return list(emails)

        return list(emails)

    # Генерация паролей на основе данных пользователя
    def generate_passwords(self, user_data):
        # Удаление запятых и пробелов из вводимых данных и объединение их в одну строку без пробелов
        clean_parts = [
            user_data.social_id.replace(',', '').replace(' ', ''),
            user_data.last_name.replace(',', '').replace(' ', ''),
            user_data.first_name.replace(',', '').replace(' ', ''),
            user_data.middle_name.replace(',', '').replace(' ', ''),
            user_data.address.replace(',', '').replace(' ', ''),
            str(user_data.birth_year).replace(',', '').replace(' ', ''),
        ] + [hobby.replace(',', '').replace(' ', '') for hobby in user_data.hobbies]

        passwords = set()

        # Генерация уникальных комбинаций для паролей
        for comb in itertools.permutations(clean_parts, 2):
            password_base = ''.join(comb)
            # Добавление символов, цифр и вариаций регистра
            variations = [
                password_base,
                password_base[::-1],
                password_base.upper(),
                password_base.lower(),
                password_base.capitalize(),
                password_base + "123",
                password_base + "!",
                "!" + password_base,
                password_base.replace('a', '@').replace('o', '0').replace('i', '1').replace('e', '3'),
                password_base.capitalize() + "!",
                password_base.upper() + "123",
                "!" + password_base.lower(),
                password_base.replace('a', '@').replace('o', '0') + "123",
                password_base[::-1].replace('i', '1').replace('e', '3') + "!"
            ]
            for variation in variations:
                passwords.add(variation)
                if len(passwords) >= 100:
                    return list(passwords)

        return list(passwords)

    # Сохранение запроса в историю
    def save_to_history(self, user_data, emails, passwords):
        self.history_id += 1
        self.history.append({
            'id': self.history_id,
            'user_data': {
                'social_id': user_data.social_id,
                'last_name': user_data.last_name,
                'first_name': user_data.first_name,
                'middle_name': user_data.middle_name,
                'address': user_data.address,
                'birth_year': user_data.birth_year,
                'hobbies': user_data.hobbies
            },
            'emails': emails,
            'passwords': passwords
        })
        self.save_history()

    # Возврат списка историй
    def get_history(self):
        return [(record['id'], record['user_data']['first_name'], record['user_data']['last_name']) for record in self.history]

    # Получение истории по ID
    def get_history_by_id(self, history_id):
        for record in self.history:
            if record['id'] == history_id:
                return record
        return None

    # Генерация электронных почт и паролей и сохранение их в историю
    def process_user_data(self, user_data):
        emails = self.generate_emails(user_data)
        passwords = self.generate_passwords(user_data)
        self.save_to_history(user_data, emails, passwords)
        return emails, passwords

# Автор проекта: Емельянов Григорий Андреевич @emelyagr https://github.com/emelyagr
# Author of the project: Emelyanov Grigory Andreevich @emelyagr https://github.com/emelyagr -->

def main():
    generator = EmailPasswordGenerator()

    while True:
        print("Введите данные пользователя или 'history' для просмотра истории или 'exit' для выхода:")
        command = input().strip()

        if command == 'history':
            history = generator.get_history()
            print("История:")
            for record in history:
                print(f"ID: {record[0]}, Имя: {record[1]} {record[2]}")
            
            print("Введите ID для просмотра деталей или 'back' для возврата:")
            sub_command = input().strip()
            if sub_command == 'back':
                continue
            else:
                try:
                    history_id = int(sub_command)
                    record = generator.get_history_by_id(history_id)
                    if record:
                        print(f"Данные пользователя для ID {history_id}:")
                        print(f"Имя: {record['user_data']['first_name']} {record['user_data']['last_name']}")
                        print("Электронные почты:")
                        for email in record['emails']:
                            print(email)
                        print("\nПароли:")
                        for password in record['passwords']:
                            print(password)
                    else:
                        print("Неверный ID.")
                except ValueError:
                    print("Неверный ввод.")
        
        elif command == 'exit':
            break

        else:
            social_id = input("Введите ID в соц. сетях: ")
            last_name = input("Введите фамилию: ")
            first_name = input("Введите имя: ")
            middle_name = input("Введите отчество: ")
            address = input("Введите адрес проживания: ")
            birth_year = input("Введите год рождения: ")
            hobbies = input("Введите хобби (через запятую): ").split(',')

            user_data = UserData(social_id, last_name, first_name, middle_name, address, birth_year, hobbies)
            emails, passwords = generator.process_user_data(user_data)

            print("Сгенерированные электронные почты:")
            for email in emails:
                print(email)

            print("\nСгенерированные пароли:")
            for password in passwords:
                print(password)

if __name__ == "__main__":
    main()
