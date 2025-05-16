from files import Files
from validators import validate_phone

class User(Files):
    __USER_ID = 1

    def __init__(self, name, phone, balance=1000, ride_history=None):
        self.user_id = User.__USER_ID
        self.name = name
        self.phone = phone
        self.balance = balance
        self.ride_history = ride_history if ride_history else []
        User.increment_user_id()

    @classmethod
    def increment_user_id(cls):
        """Лічильник індексів, робить їх унікальними"""
        cls.__USER_ID += 1

    def to_dict(self):
        """Перетворення об'єкта в словник"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
            "ride_history": self.ride_history
        }

    @staticmethod
    def from_dict(user_dict):
        """Створює новий об'єкт з словника"""
        user = User(
            user_dict["name"],
            user_dict["phone"],
            user_dict.get("balance", 1000),
            user_dict.get("ride_history", [])
        )
        user.user_id = user_dict["user_id"]
        return user

    @staticmethod
    def register_user():
        """Реєстрація користувача"""
        print("\nРеєстрація користувача")
        name = input("Введіть ім'я: ")
        phone = input("Введіть номер телефону (+380xxxxxxxxx): ")

        if not name:
            print("Ім'я не може бути порожнім")
            return

        if not validate_phone(phone):
            print("Некоректний формат номера телефону. Використовуйте формат +380xxxxxxxxx")
            return

        users = User.load_from_file("users.json")
        for user in users:
            if user.phone == phone:
                print("Користувач з таким номером телефону вже існує")
                return

        new_user = User(name, phone)
        users.append(new_user)
        User.save_to_file(users, "users.json")
        print(f"Користувач {name} з ID {new_user.user_id} успішно зареєстрований!")

    @staticmethod
    def find_by_id(user_id):
        """Пошук за ід"""
        users = User.load_from_file("users.json")
        for user in users:
            if user.user_id == user_id:
                return user
        return None

    def add_ride(self, ride_id):
        """Додавання поїздки(ід) до історії користувача"""
        if ride_id not in self.ride_history:
            self.ride_history.append(ride_id)
            users = User.load_from_file("users.json")
            for i, user in enumerate(users):
                if user.user_id == self.user_id:
                    users[i] = self
                    User.save_to_file(users, "users.json")
                    return True
        return False

    def can_pay(self, price):
        """Перевірка балансу"""
        return self.balance >= float(price)

    def process_payment(self, price):
        """Зняття оплати"""
        if self.can_pay(price):
            self.balance -= float(price)
            users = User.load_from_file("users.json")
            for i, user in enumerate(users):
                if user.user_id == self.user_id:
                    users[i] = self
                    User.save_to_file(users, "users.json")
                    return True
        return False

    @staticmethod
    def user_report():
        """Формування звіту користувача"""
        print("\nЗвіт про користувача")
        user_id_input = input("Введіть ID користувача: ")

        try:
            user_id = int(user_id_input)
        except ValueError:
            print("ID користувача повинен бути числом")
            return

        user = User.find_by_id(user_id)
        if not user:
            print("Користувача з таким ID не знайдено")
            return

        print(f"\nІм'я: {user.name}")
        print(f"Телефон: {user.phone}")
        print(f"ID: {user.user_id}")
        print(f"Баланс: {user.balance} грн")

        if not user.ride_history:
            print("Історія поїздок порожня")
            return

        print("\nІсторія поїздок:")
        from program_clases.ride import Ride
        rides = Ride.load_from_file("rides.json")

        total_spent = 0
        ride_count = 0

        for ride in rides:
            if ride.ride_id in user.ride_history:
                print(f"Поїздка {ride.ride_id}:")
                print(f"  Від: {ride.start_location}")
                print(f"  До: {ride.end_location}")
                print(f"  Ціна: {ride.price} грн")
                print(f"  Дата початку: {ride.start_time}")
                print(f"  Дата закінчення: {ride.end_time if ride.end_time else 'В процесі'}")
                print("-" * 30)

                total_spent += float(ride.price)
                ride_count += 1

        print(f"\nВсього поїздок: {ride_count}")
        print(f"Загальна сума витрат: {total_spent} грн")