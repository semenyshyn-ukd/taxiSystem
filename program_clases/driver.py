import json
from validators import validate_phone


class Driver:
    __DRIVER_ID = 1

    def __init__(self, driver_name, car, phone, rating=0.0, ride_history=None):
        self.driver_id = Driver.__DRIVER_ID
        self.driver_name = driver_name
        self.car = car
        self.phone = phone
        self.rating = rating
        self.ride_history = ride_history if ride_history else []
        Driver.increment_driver_id()

    @classmethod
    def increment_driver_id(cls):
        """Лічильник індексів, робить їх унікальними"""
        cls.__DRIVER_ID += 1

    def to_dict(self):
        """Перетворення об'єкта в словник"""
        return {
            "driver_id": self.driver_id,
            "driver_name": self.driver_name,
            "car": self.car,
            "phone": self.phone,
            "rating": self.rating,
            "ride_history": self.ride_history
        }

    @staticmethod
    def from_dict(driver_dict):
        """Створює новий об'єкт з словника"""
        driver = Driver(
            driver_dict["driver_name"],
            driver_dict["car"],
            driver_dict["phone"],
            driver_dict.get("rating", 0.0),
            driver_dict.get("ride_history", [])
        )
        driver.driver_id = driver_dict["driver_id"]
        return driver

    @staticmethod
    def load_drivers():
        """Підтягує всіх водіїв з словника"""
        try:
            with open("drivers.json", "r", encoding="utf-8") as file:
                drivers_data = json.load(file)
                drivers = []
                for driver_dict in drivers_data:
                    driver = Driver.from_dict(driver_dict)
                    drivers.append(driver)
                return drivers
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_drivers(drivers):
        """Зберігає водіїв у словник"""
        drivers_data = []
        for driver in drivers:
            drivers_data.append(driver.to_dict())

        with open("drivers.json", "w", encoding="utf-8") as file:
            json.dump(drivers_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def register_driver():
        """Реєестрація водія"""
        print("\nРеєстрація водія")
        driver_name = input("Введіть ім'я водія: ")
        phone = input("Введіть номер телефону водія (+380xxxxxxxxx): ")
        car = input("Введіть модель автомобіля: ")

        if not driver_name or not car:
            print("Ім'я та модель автомобіля не можуть бути порожніми")
            return

        if not validate_phone(phone):
            print("Некоректний формат номера телефону. Використовуйте формат +380xxxxxxxxx")
            return

        drivers = Driver.load_drivers()
        for driver in drivers:
            if driver.phone == phone:
                print("Водій з таким номером телефону вже існує")
                return

        new_driver = Driver(driver_name, car, phone)
        drivers.append(new_driver)
        Driver.save_drivers(drivers)
        print(f"Водій {driver_name} з ID {new_driver.driver_id} успішно зареєстрований!")

    @staticmethod
    def find_by_id(driver_id):
        """Пошук водія по індексу"""
        drivers = Driver.load_drivers()
        for driver in drivers:
            if driver.driver_id == driver_id:
                return driver
        return None

    def add_ride(self, ride_id):
        """Додає поїздку(ід) до історії водія і оновлє історію водія"""
        if ride_id not in self.ride_history:
            self.ride_history.append(ride_id)
            drivers = Driver.load_drivers()
            for i, driver in enumerate(drivers):
                if driver.driver_id == self.driver_id:
                    drivers[i] = self
                    Driver.save_drivers(drivers)
                    return True
        return False

    def update_rating(self, new_rating):
        """Оновлює рейтинг водія на основі даних від користувача"""
        if new_rating < 1 or new_rating > 5:
            return False

        ride_count = len(self.ride_history)
        if ride_count == 1:
            self.rating = float(new_rating)
        else:
            self.rating = round((self.rating * (ride_count - 1) + new_rating) / ride_count, 1)

        drivers = Driver.load_drivers()
        for i, driver in enumerate(drivers):
            if driver.driver_id == self.driver_id:
                drivers[i] = self
                Driver.save_drivers(drivers)
                return True
        return False

    @staticmethod
    def driver_report():
        """Формує та виводить звіт про водія"""
        print("\nЗвіт водія")
        driver_id_input = input("Введіть ID водія: ")

        try:
            driver_id = int(driver_id_input)
        except ValueError:
            print("ID водія повинен бути числом")
            return

        driver = Driver.find_by_id(driver_id)
        if not driver:
            print("Водія з таким ID не знайдено")
            return

        print(f"\nЗвіт водія: {driver.driver_name}")
        print(f"Авто: {driver.car}")
        print(f"Телефон: {driver.phone}")
        print(f"Рейтинг: {driver.rating:.1f}")

        if not driver.ride_history:
            print("\nІсторія поїздок порожня")
            return

        print("\nІсторія поїздок:")
        from program_clases.ride import Ride
        rides = Ride.load_rides()

        total_earnings = 0
        ride_count = 0

        for ride in rides:
            if ride.ride_id in driver.ride_history:
                print(f"Поїздка {ride.ride_id}:")
                print(f"  Маршрут: {ride.start_location} -> {ride.end_location}")
                print(f"  Час: {ride.start_time} - {ride.end_time if ride.end_time else 'В процесі'}")
                print(f"  Ціна: {ride.price} грн")
                print("-" * 30)

                total_earnings += float(ride.price)
                ride_count += 1

        print(f"\nВсього поїздок: {ride_count}")
        print(f"Загальний заробіток: {total_earnings} грн")