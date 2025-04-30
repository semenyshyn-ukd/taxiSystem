import json
from datetime import datetime

class Order:
    __ORDER_ID = 1

    STATUS_NEW = "новий"
    STATUS_IN_PROGRESS = "в процесі"
    STATUS_COMPLETED = "завершений"
    STATUS_CANCELLED = "скасований"

    def __init__(self, user_id, start_location, end_location, order_time, status=STATUS_NEW,
                 assigned_driver_id=None, ride_id=None):
        self.order_id = Order.__ORDER_ID
        self.user_id = user_id
        self.start_location = start_location
        self.end_location = end_location
        self.order_time = order_time
        self.status = status
        self.assigned_driver_id = assigned_driver_id
        self.ride_id = ride_id
        Order.increment_order_id()

    @classmethod
    def increment_order_id(cls):
        cls.__ORDER_ID += 1

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "start_location": self.start_location,
            "end_location": self.end_location,
            "order_time": self.order_time,
            "status": self.status,
            "assigned_driver_id": self.assigned_driver_id,
            "ride_id": self.ride_id
        }

    @staticmethod
    def from_dict(order_dict):
        order = Order(
            order_dict["user_id"],
            order_dict["start_location"],
            order_dict["end_location"],
            order_dict["order_time"],
            order_dict.get("status", Order.STATUS_NEW),
            order_dict.get("assigned_driver_id"),
            order_dict.get("ride_id")
        )
        order.order_id = order_dict["order_id"]
        return order

    @staticmethod
    def load_orders():
        try:
            with open("orders.json", "r", encoding="utf-8") as file:
                orders_data = json.load(file)
                orders = []
                for order_dict in orders_data:
                    order = Order.from_dict(order_dict)
                    orders.append(order)
                return orders
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_orders(orders):
        orders_data = []
        for order in orders:
            orders_data.append(order.to_dict())

        with open("orders.json", "w", encoding="utf-8") as file:
            json.dump(orders_data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def create_order():
        from program_clases.user import User

        print("\nЗамовлення таксі")

        users = User.load_users()
        if not users:
            print("Немає зареєстрованих користувачів. Спочатку зареєструйте користувача.")
            return

        print("\nДоступні користувачі:")
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.name} - {user.phone}")

        try:
            user_index = int(input("\nВиберіть номер користувача: ")) - 1
            if user_index < 0 or user_index >= len(users):
                print("Невірний вибір користувача")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        user = users[user_index]

        start_location = input("Введіть початкову адресу: ")
        end_location = input("Введіть кінцеву адресу: ")

        if not start_location or not end_location:
            print("Адреси не можуть бути порожніми")
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"Час замовлення: {current_time}")

        orders = Order.load_orders()
        new_order = Order(user.user_id, start_location, end_location, current_time)
        orders.append(new_order)
        Order.save_orders(orders)

        print(f"Замовлення таксі для {user.name} успішно створено!")
        print(f"ID замовлення: {new_order.order_id}")

    @staticmethod
    def update_order_status():
        from program_clases.user import User
        from program_clases.driver import Driver

        print("\nОновлення статусу замовлення")

        orders = Order.load_orders()
        active_orders = []
        for o in orders:
            if o.status != Order.STATUS_COMPLETED and o.status != Order.STATUS_CANCELLED:
                active_orders.append(o)

        if not active_orders:
            print("Немає активних замовлень")
            return

        print("\nДоступні замовлення:")
        for i, order in enumerate(active_orders, 1):
            status_text = order.status if order.status else "Невідомо"
            print(f"{i}. {order.start_location} -> {order.end_location} (Статус: {status_text})")

        try:
            order_index = int(input("\nВиберіть номер замовлення: ")) - 1
            if order_index < 0 or order_index >= len(active_orders):
                print("Невірний вибір замовлення")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        order = active_orders[order_index]

        print("\nДоступні статуси:")
        print(f"1. {Order.STATUS_NEW}")
        print(f"2. {Order.STATUS_IN_PROGRESS}")
        print(f"3. {Order.STATUS_COMPLETED}")
        print(f"4. {Order.STATUS_CANCELLED}")

        try:
            status_choice = int(input("\nВиберіть новий статус: "))
            if status_choice < 1 or status_choice > 4:
                print("Невірний вибір статусу")
                return
        except ValueError:
            print("Введіть числове значення")
            return

        statuses = [Order.STATUS_NEW, Order.STATUS_IN_PROGRESS, Order.STATUS_COMPLETED, Order.STATUS_CANCELLED]
        new_status = statuses[status_choice - 1]

        if order.status == new_status:
            print(f"Замовлення вже має статус '{new_status}'")
            return

        if new_status == Order.STATUS_IN_PROGRESS and not order.assigned_driver_id:
            drivers = Driver.load_drivers()
            if not drivers:
                print("Немає доступних водіїв. Спочатку зареєструйте водія.")
                return

            print("\nДоступні водії:")
            for i, driver in enumerate(drivers, 1):
                print(f"{i}. {driver.driver_name} - {driver.car} (Рейтинг: {driver.rating})")

            try:
                driver_index = int(input("\nВиберіть номер водія: ")) - 1
                if driver_index < 0 or driver_index >= len(drivers):
                    print("Невірний вибір водія")
                    return
            except ValueError:
                print("Введіть числове значення")
                return

            driver = drivers[driver_index]
            order.assigned_driver_id = driver.driver_id

            from program_clases.ride import Ride
            price = Ride.calculate_price()

            user = User.find_by_id(order.user_id)
            if not user:
                print("Користувача не знайдено")
                return

            if not user.can_pay(price):
                print(f"Недостатньо коштів на балансі користувача ({user.balance} грн). Потрібно {price} грн.")
                return

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            rides = Ride.load_rides()
            new_ride = Ride(
                order.start_location,
                order.end_location,
                price,
                current_time,
                None,
                order.user_id,
                driver.driver_id
            )

            rides.append(new_ride)
            Ride.save_rides(rides)

            order.ride_id = new_ride.ride_id

            if user.process_payment(price):
                print(f"З рахунку користувача знято {price} грн")
            else:
                print("Помилка при обробці платежу")
                return

            print(f"Створено нову поїздку з ID: {new_ride.ride_id}")

        for i, o in enumerate(orders):
            if o.order_id == order.order_id:
                orders[i] = order
                orders[i].status = new_status
                Order.save_orders(orders)
                print(f"Статус замовлення успішно оновлено до '{new_status}'!")
                return

    @staticmethod
    def update_order_status_by_ride(ride_id, new_status):
        from program_clases.ride import Ride

        ride = Ride.find_by_id(ride_id)
        if not ride:
            return False

        orders = Order.load_orders()
        for i, order in enumerate(orders):
            if order.ride_id == ride_id:
                orders[i].status = new_status
                Order.save_orders(orders)
                return True
        return False

    @staticmethod
    def find_by_id(order_id):
        orders = Order.load_orders()
        for order in orders:
            if order.order_id == order_id:
                return order
        return None