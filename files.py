import json
from abc import abstractmethod, ABC

class Files(ABC):
    @classmethod
    def load_from_file(cls, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                objects = []
                for obj in data:
                    objects.append(cls.from_dict(obj))
                return objects
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def save_to_file(cls, objects, filename):
        data = []
        for obj in objects:
            data.append(obj.to_dict())

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @staticmethod
    @abstractmethod
    def from_dict(data):
        """Створює об'єкт із словника"""
        pass

    @staticmethod
    @abstractmethod
    def to_dict(data):
        """Повертає словник із даних об'єкта"""
        raise NotImplementedError("Метод to_dict має бути реалізований у підкласі")