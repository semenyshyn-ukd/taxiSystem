import json
from datetime import datetime

class Ride:
    def __init__(self, ride_id, start_location, end_location, price, start_time, end_time, user_id, driver_id):
        self.ride_id = ride_id
        self.start_location = start_location
        self.end_location = end_location
        self.price = price
        self.start_time = start_time
        self.end_time = end_time
        self.user_id = user_id
        self.driver_id = driver_id

    def to_dict(self):
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
        return Ride(
            ride_dict["ride_id"],
            ride_dict["start_location"],
            ride_dict["end_location"],
            ride_dict["price"],
            ride_dict["start_time"],
            ride_dict.get("end_time"),
            ride_dict["user_id"],
            ride_dict["driver_id"]
        )

    @staticmethod
    def load_rides():
        try:
            with open("rides.json", "r", encoding="utf-8") as file:
                rides_data = json.load(file)
                rides = []
                for ride_dict in rides_data:
                    ride = Ride.from_dict(ride_dict)
                    rides.append(ride)
                return rides
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_rides(rides):
        rides_data = []
        for ride in rides:
            rides_data.append(ride.to_dict())

        with open("rides.json", "w", encoding="utf-8") as file:
            json.dump(rides_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def calculate_price(start_location, end_location):
        base_fare = 100.0
        return base_fare

    @staticmethod
    def find_by_id(ride_id):
        rides = Ride.load_rides()
        for ride in rides:
            if ride.ride_id == ride_id:
                return ride
        return None

    @staticmethod
    def complete_ride():
        print("\nЗавершення поїздки")
        ride_id = input("Введіть ID поїздки: ")

        rides = Ride.load_rides()
        ride = None
        ride_index = -1

        for i, r in enumerate(rides):
            if r.ride_id == ride_id:
                ride = r
                ride_index = i
                break

        try:
            ride_id = int(ride_id)
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

        from program_clases.user import User
        from program_clases.driver import Driver
        from program_clases.order import Order

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        ride.end_time = current_time

        rides[ride_index] = ride
        Ride.save_rides(rides)

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