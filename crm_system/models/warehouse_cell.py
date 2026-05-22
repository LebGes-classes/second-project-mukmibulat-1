from typing import Dict

class WarehouseCell:
    """Класс ячейки склада.

    Args:
        cell_id (str): ID ячейки.
        max_capacity (int): Максимальная вместимость (штук).
    """

    def __init__(self, cell_id: str, max_capacity: int):
        self._cell_id = cell_id
        self._max_capacity = max(0, max_capacity)
        self._products: Dict[str, int] = {}

    @property
    def cell_id(self) -> str:
        """Возвращает ID ячейки.

        Returns:
            str: ID ячейки.
        """

        return self._cell_id

    @property
    def max_capacity(self) -> int:
        """Возвращает максимальную вместимость.

        Returns:
            int: Вместимость.
        """

        return self._max_capacity

    @property
    def products(self) -> Dict[str, int]:
        """Возвращает копию словаря товаров.

        Returns:
            Dict[str, int]: Товары в ячейке.
        """

        return self._products.copy()

    def get_current_load(self) -> int:
        """Текущая загруженность ячейки.

        Returns:
            int: Суммарное количество товаров.
        """

        return sum(self._products.values())

    def add_product(self, product_number: str, quantity: int) -> bool:
        """Добавляет товар в ячейку.

        Args:
            product_number (str): Артикул.
            quantity (int): Количество.

        Returns:
            bool: True, если добавление успешно.
        """

        quantity = max(0, quantity)

        if self.get_current_load() + quantity > self._max_capacity:
            return False

        self._products[product_number] = self._products.get(product_number, 0) + quantity

        return True

    def remove_product(self, product_number: str, quantity: int) -> bool:
        """Удаляет товар из ячейки.

        Args:
            product_number (str): Артикул.
            quantity (int): Количество.

        Returns:
            bool: True, если удаление успешно.
        """

        quantity = max(0, quantity)

        if product_number not in self._products or self._products[product_number] < quantity:
            return False

        self._products[product_number] -= quantity

        if self._products[product_number] == 0:
            del self._products[product_number]

        return True

    def get_info(self) -> str:
        """Возвращает информацию о ячейке.

        Returns:
            str: Строка с ID и загруженностью.
        """

        return f"Ячейка: {self._cell_id}, Заполненность: {self.get_current_load()}/{self._max_capacity}"

    def to_dict(self) -> dict:
        """Преобразует объект в словарь.

        Returns:
            dict: Данные для сериализации.
        """

        return {
            "cell_id": self._cell_id,
            "max_capacity": self._max_capacity,
            "products": self._products
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            WarehouseCell: Новый экземпляр.
        """

        cell = cls(data["cell_id"], data["max_capacity"])
        cell._products = data.get("products", {})

        return cell