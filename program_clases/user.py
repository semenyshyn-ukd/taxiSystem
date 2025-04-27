import json
from validators import validate_phone

class User:
    def __init__(self, user_id, name, phone, balance=1000, ride_history=None):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.balance = balance
        self.ride_history = ride_history if ride_history else []

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
            "ride_history": self.ride_history
        }

    @staticmethod
    def from_dict(user_dict):
        return User(
            user_dict["user_id"],
            user_dict["name"],
            user_dict["phone"],
            user_dict.get("balance", 1000),
            user_dict.get("ride_history", [])
        )

    @staticmethod
    def load_users():
        try:
            with open("users.json", "r", encoding="utf-8") as file:
                users_data = json.load(file)
                users = []
                for user_dict in users_data:
                    user = User.from_dict(user_dict)
                    users.append(user)
                return users
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_users(users):
        users_data = []
        for user in users:
            users_data.append(user.to_dict())

        with open("users.json", "w", encoding="utf-8") as file:
            json.dump(users_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def register_user():
        print("\nРеєстрація користувача")
        name = input("Введіть ім'я: ")
        phone = input("Введіть номер телефону (+380xxxxxxxxx): ")

        if not name:
            print("Ім'я не може бути порожнім")
            return

        if not validate_phone(phone):
            print("Некоректний формат номера телефону. Використовуйте формат +380xxxxxxxxx")
            return

        users = User.load_users()
        for user in users:
            if user.phone == phone:
                print("Користувач з таким номером телефону вже існує")
                return

        user_id = len(users) + 1
        new_user = User(user_id, name, phone)
        users.append(new_user)
        User.save_users(users)
        print(f"Користувач {name} з ID {user_id} успішно зареєстрований!")

    @staticmethod
    def find_by_phone(phone):
        users = User.load_users()
        for user in users:
            if user.phone == phone:
                return user
        return None

    @staticmethod
    def find_by_id(user_id):
        users = User.load_users()
        for user in users:
            if user.user_id == user_id:
                return user
        return None

    def add_ride(self, ride_id):
        if ride_id not in self.ride_history:
            self.ride_history.append(ride_id)
            users = User.load_users()
            for i, user in enumerate(users):
                if user.user_id == self.user_id:
                    users[i] = self
                    User.save_users(users)
                    return True
        return False

    def can_pay(self, price):
        return self.balance >= float(price)

    def process_payment(self, price):
        if self.can_pay(price):
            self.balance -= float(price)
            users = User.load_users()
            for i, user in enumerate(users):
                if user.user_id == self.user_id:
                    users[i] = self
                    User.save_users(users)
                    return True
        return False

    @staticmethod
    def user_report():
        print("\nЗвіт про користувача")
        input_id = input("Введіть ID користувача: ")

        try:
            input_id = int(input_id)
        except ValueError:
            print("ID користувача повинен бути числом")
            return

        user = User.find_by_id(input_id)
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
        rides = Ride.load_rides()

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