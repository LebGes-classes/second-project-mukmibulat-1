class Person:
    """Базовый класс для описания человека.

    Args:
        first_name (str): Имя.
        last_name (str): Фамилия.
        age (int): Возраст.
        phone (str): Телефон.
        email (str): Email.
    """

    def __init__(self, first_name: str, last_name: str, age: int, phone: str, email: str):
        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self._phone = phone
        self._email = email

    @property
    def first_name(self) -> str:
        """Возвращает имя.

        Returns:
            str: Имя.
        """

        return self._first_name

    @property
    def last_name(self) -> str:
        """Возвращает фамилию.

        Returns:
            str: Фамилия.
        """

        return self._last_name

    @property
    def age(self) -> int:
        """Возвращает возраст.

        Returns:
            int: Возраст.
        """

        return self._age

    @age.setter
    def age(self, value: int):
        """Устанавливает возраст с проверкой.

        Args:
            value (int): Новый возраст.

        Raises:
            ValueError: Если возраст отрицательный.
        """

        if value < 0:
            raise ValueError("Возраст не может быть отрицательным")
        self._age = value

    @property
    def phone(self) -> str:
        """Возвращает телефон.

        Returns:
            str: Телефон.
        """

        return self._phone

    @property
    def email(self) -> str:
        """Возвращает email.

        Returns:
            str: Email.
        """

        return self._email

    def get_full_name(self) -> str:
        """Возвращает полное имя.

        Returns:
            str: Имя и фамилия через пробел.
        """

        return f"{self._first_name} {self._last_name}"

    def get_info(self) -> str:
        """Возвращает базовую информацию.

        Returns:
            str: Строка с именем, возрастом, телефоном и email.
        """

        return f"Имя: {self.get_full_name()}, Возраст: {self._age}, Тел: {self._phone}, Email: {self._email}"