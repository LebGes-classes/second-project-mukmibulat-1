from models.person import Person


class Employee(Person):
    """Класс сотрудника компании.

    Args:
        first_name (str): Имя.
        last_name (str): Фамилия.
        age (int): Возраст.
        phone (str): Телефон.
        email (str): Email.
        employee_id (str): Табельный номер.
        position (str): Должность.
        salary (float): Оклад.
        is_working (bool): Работает ли сейчас.
    """

    def __init__(self, first_name: str, last_name: str, age: int, phone: str, email: str,
                 employee_id: str, position: str, salary: float, is_working: bool = True):
        super().__init__(first_name, last_name, age, phone, email)
        self._employee_id = employee_id
        self._position = position
        self._salary = salary
        self._is_working = is_working

    @property
    def employee_id(self) -> str:
        """Возвращает ID сотрудника.

        Returns:
            str: ID сотрудника.
        """

        return self._employee_id

    @property
    def position(self) -> str:
        """Возвращает должность.

        Returns:
            str: Должность.
        """

        return self._position

    @property
    def salary(self) -> float:
        """Возвращает оклад.

        Returns:
            float: Оклад.
        """

        return self._salary

    @property
    def is_working(self) -> bool:
        """Работает ли сотрудник.

        Returns:
            bool: True если работает.
        """

        return self._is_working

    def dismiss(self):
        """Увольняет сотрудника."""

        self._is_working = False

    def get_info(self) -> str:
        """Возвращает полную информацию о сотруднике.

        Returns:
            str: Строка со всеми данными.
        """

        status = "Работает" if self._is_working else "Уволен"

        return f"{super().get_info()}, ID: {self._employee_id}, Должность: {self._position}, Зарплата: {self._salary}, Статус: {status}"

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
            "employee_id": self._employee_id,
            "position": self._position,
            "salary": self._salary,
            "is_working": self._is_working
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            Employee: Новый экземпляр.
        """

        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            phone=data["phone"],
            email=data["email"],
            employee_id=data["employee_id"],
            position=data["position"],
            salary=data["salary"],
            is_working=data.get("is_working", True)
        )