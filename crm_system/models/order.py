from datetime import datetime
from models.customer import Customer


class Order:
    """Класс заказа.

    Args:
        order_id (str): ID заказа.
        customer (Customer): Покупатель.
        product_number (str): Артикул товара.
        quantity (int): Количество.
        total_price (float): Общая стоимость.
    """

    def __init__(self, order_id: str, customer: Customer, product_number: str, quantity: int, total_price: float):
        self._order_id = order_id
        self._customer = customer
        self._product_number = product_number
        self._quantity = max(0, quantity)
        self._total_price = max(0.0, total_price)
        self._created_at = str(datetime.now())
        self._status = "Завершен"

    @property
    def order_id(self) -> str:
        """Возвращает ID заказа.

        Returns:
            str: ID заказа.
        """

        return self._order_id

    def get_info(self) -> str:
        """Возвращает информацию о заказе.

        Returns:
            str: Строка с данными.
        """

        return f"Заказ: {self._order_id}, Покупатель: {self._customer.get_full_name()}, Сумма: {self._total_price} руб."

    def to_dict(self) -> dict:
        """Преобразует объект в словарь.

        Returns:
            dict: Данные для сериализации.
        """

        return {
            "order_id": self._order_id,
            "customer": self._customer.to_dict(),
            "product_number": self._product_number,
            "quantity": self._quantity,
            "total_price": self._total_price,
            "created_at": self._created_at,
            "status": self._status
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            Order: Новый экземпляр.
        """

        customer = Customer.from_dict(data["customer"])
        order = cls(
            order_id=data["order_id"],
            customer=customer,
            product_number=data["product_number"],
            quantity=data["quantity"],
            total_price=data["total_price"]
        )
        order._created_at = data.get("created_at", str(datetime.now()))
        order._status = data.get("status", "Завершен")

        return order