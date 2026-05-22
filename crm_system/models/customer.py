from models.person import Person


class Customer(Person):
    """Класс розничного покупателя.

    Args:
        first_name (str): Имя.
        last_name (str): Фамилия.
        age (int): Возраст.
        phone (str): Телефон.
        email (str): Email.
        customer_id (str): ID клиента.
    """

    def __init__(self, first_name: str, last_name: str, age: int, phone: str, email: str, customer_id: str):
        super().__init__(first_name, last_name, age, phone, email)
        self._customer_id = customer_id

    @property
    def customer_id(self) -> str:
        """Возвращает ID клиента.

        Returns:
            str: ID клиента.
        """

        return self._customer_id

    def get_info(self) -> str:
        """Возвращает информацию о клиенте.

        Returns:
            str: Строка с данными.
        """

        return f"{super().get_info()}, ID Клиента: {self._customer_id}"

    def to_dict(self) -> dict:
        """Преобразует объект в словарь.

        Returns:
            dict: Данные для сериализации.
        """

        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "phone": self.phone,
            "email": self.email,
            "customer_id": self._customer_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            Customer: Новый экземпляр.
        """

        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            phone=data["phone"],
            email=data["email"],
            customer_id=data["customer_id"]
        )