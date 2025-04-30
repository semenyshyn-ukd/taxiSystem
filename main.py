import os
import json
from program_clases.user import User
from program_clases.driver import Driver
from program_clases.ride import Ride
from program_clases.order import Order

def initialize_files():
    files = ["users.json", "drivers.json", "orders.json", "rides.json"]

    for file in files:
        if not os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f:
                json.dump([], f)


def main():
    initialize_files()

    while True:
        print("\nМеню системи замовлень таксі")
        print("1. Зареєструвати користувача")
        print("2. Зареєструвати водія")
        print("3. Створити замовлення")
        print("4. Змінити статус замовлення")
        print("5. Завершити поїздку")
        print("6. Переглянути звіт водія")
        print("7. Переглянути звіт користувача")
        print("0. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            User.register_user()
        elif choice == "2":
            Driver.register_driver()
        elif choice == "3":
            Order.create_order()
        elif choice == "4":
            Order.update_order_status()
        elif choice == "5":
            Ride.complete_ride()
        elif choice == "6":
            Driver.driver_report()
        elif choice == "7":
            User.user_report()
        elif choice == "0":
            print("Програму завершено!")
            break
        else:
            print("Невірна опція. Спробуйте ще раз.")


if __name__ == "__main__":
    main()