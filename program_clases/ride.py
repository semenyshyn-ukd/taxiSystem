from datetime import datetime
from files import Files

class Ride(Files):
    __RIDE_ID = 1

    def __init__(self, start_location, end_location, price, start_time, end_time, user_id, driver_id):
        self.ride_id = Ride.__RIDE_ID
        self.start_location = start_location
        self.end_location = end_location
        self.price = price
        self.start_time = start_time
        self.end_time = end_time
        self.user_id = user_id
        self.driver_id = driver_id
        Ride.increment_ride_id()

    @classmethod
    def increment_ride_id(cls):
        """Лічильник індексів, робить їх унікальними"""
        cls.__RIDE_ID += 1

    def to_dict(self):
        """Перетворення об'єкта в словник"""
        return {
            "ride_id": self.ride_id,
            "start_location": self.start_location,
            "end_location": self.end_location,
            "price": self.price,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "user_id": self.user_id,
            "driver_id": self.driver_id
        }

    @staticmethod
    def from_dict(ride_dict):
        """Створює новий об'єкт з словника"""
        ride = Ride(
            ride_dict["start_location"],
            ride_dict["end_location"],
            ride_dict["price"],
            ride_dict["start_time"],
            ride_dict.get("end_time"),
            ride_dict["user_id"],
            ride_dict["driver_id"]
        )
        ride.ride_id = ride_dict["ride_id"]
        return ride

    @staticmethod
    def calculate_price():
        """Встановлює вартість поїздки"""
        base_fare = 100.0
        return base_fare

    @staticmethod
    def find_by_id(ride_id):
        """Пошук за ід"""
        rides = Ride.load_from_file("rides.json")
        for ride in rides:
            if ride.ride_id == ride_id:
                return ride
        return None

    @staticmethod
    def complete_ride():
        """Завершити активну поїздку"""
        print("\nЗавершення поїздки")
        ride_id_input = input("Введіть ID поїздки: ")

        try:
            ride_id = int(ride_id_input)
        except ValueError:
            print("ID поїздки повинен бути числом")
            return

        ride = Ride.find_by_id(ride_id)
        if not ride:
            print("Поїздки з таким ID не знайдено")
            return

        if ride.end_time:
            print("Ця поїздка вже завершена")
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ride.end_time = current_time

        rides = Ride.load_from_file("rides.json")
        for i, r in enumerate(rides):
            if r.ride_id == ride_id:
                rides[i] = ride
                break

        Ride.save_to_file(rides, "rides.json")

        from program_clases.user import User
        from program_clases.driver import Driver
        from program_clases.order import Order

        user = User.find_by_id(ride.user_id)
        if user:
            user.add_ride(ride_id)

        driver = Driver.find_by_id(ride.driver_id)
        if driver:
            driver.add_ride(ride_id)

            try:
                rating = float(input("Оцініть водія від 1 до 5: "))
                if 1 <= rating <= 5:
                    driver.update_rating(rating)
                    print(f"Рейтинг водія оновлено до {driver.rating}")
                else:
                    print("Оцінка має бути від 1 до 5")
            except ValueError:
                print("Введіть числове значення для оцінки")

        Order.update_order_status_by_ride(ride_id, Order.STATUS_COMPLETED)

        print("Поїздку успішно завершено!")