class Product:
    """Класс товара.

    Args:
        number (str): Артикул.
        card_id (str): ID карточки.
        name (str): Название.
        supplier (str): Поставщик.
        manufacturer (str): Производитель.
        cost (float): Себестоимость.
    """

    def __init__(self, number: str, card_id: str, name: str, supplier: str, manufacturer: str, cost: float):
        self._number = number
        self._card_id = card_id
        self._name = name
        self._supplier = supplier
        self._manufacturer = manufacturer
        self._cost = max(0.0, cost)

    @property
    def number(self) -> str:
        """Возвращает артикул.

        Returns:
            str: Артикул.
        """

        return self._number

    @property
    def name(self) -> str:
        """Возвращает название.

        Returns:
            str: Название.
        """

        return self._name

    @property
    def cost(self) -> float:
        """Возвращает себестоимость.

        Returns:
            float: Себестоимость.
        """

        return self._cost

    def get_info(self) -> str:
        """Возвращает информацию о товаре.

        Returns:
            str: Строка с артикулом, названием, производителем и ценой.
        """

        return f"[{self._number}] {self._name} (Производитель: {self._manufacturer}), Цена: {self._cost} руб."

    def to_dict(self) -> dict:
        """Преобразует объект в словарь.

        Returns:
            dict: Данные для сериализации.
        """

        return {
            "number": self._number,
            "card_id": self._card_id,
            "name": self._name,
            "supplier": self._supplier,
            "manufacturer": self._manufacturer,
            "cost": self._cost
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            Product: Новый экземпляр.
        """

        return cls(
            number=data["number"],
            card_id=data["card_id"],
            name=data["name"],
            supplier=data["supplier"],
            manufacturer=data["manufacturer"],
            cost=data["cost"]
        )