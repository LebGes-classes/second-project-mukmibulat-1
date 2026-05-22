from typing import Dict


class SalesPoint:
    """Класс розничной точки продаж.

    Args:
        sales_point_id (str): ID точки.
        name (str): Название.
        address (str): Адрес.
        income (float): Доход.
        is_open (bool): Открыта ли точка.
    """

    def __init__(self, sales_point_id: str, name: str, address: str, income: float = 0.0, is_open: bool = True):
        self._sales_point_id = sales_point_id
        self._name = name
        self._address = address
        self._income = max(0.0, income)
        self._is_open = is_open
        self._products: Dict[str, int] = {}

    @property
    def sales_point_id(self) -> str:
        """Возвращает ID точки.

        Returns:
            str: ID точки.
        """

        return self._sales_point_id

    @property
    def name(self) -> str:
        """Возвращает название.

        Returns:
            str: Название.
        """

        return self._name

    @property
    def is_open(self) -> bool:
        """Открыта ли точка.

        Returns:
            bool: True если открыта.
        """

        return self._is_open

    def set_open(self, open_status: bool):
        """Открыть или закрыть точку.

        Args:
            open_status (bool): Новый статус.
        """

        self._is_open = open_status

    @property
    def income(self) -> float:
        """Возвращает доход.

        Returns:
            float: Доход.
        """

        return self._income

    @income.setter
    def income(self, value: float):
        """Устанавливает доход.

        Args:
            value (float): Новое значение.
        """

        self._income = max(0.0, value)

    @property
    def products(self) -> Dict[str, int]:
        """Возвращает копию словаря товаров.

        Returns:
            Dict[str, int]: Товары на витрине.
        """

        return self._products.copy()

    def get_info(self) -> str:
        """Возвращает информацию о точке.

        Returns:
            str: Строка с данными.
        """

        return f"Магазин: {self._name}, Адрес: {self._address}, Текущий оборот: {self._income} руб."

    def to_dict(self) -> dict:
        """Преобразует объект в словарь.

        Returns:
            dict: Данные для сериализации.
        """

        return {
            "sales_point_id": self._sales_point_id,
            "name": self._name,
            "address": self._address,
            "income": self._income,
            "is_open": self._is_open,
            "products": self._products
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            SalesPoint: Новый экземпляр.
        """

        sp = cls(
            sales_point_id=data["sales_point_id"],
            name=data["name"],
            address=data["address"],
            income=data.get("income", 0.0),
            is_open=data.get("is_open", True)
        )
        sp._products = data.get("products", {})

        return sp