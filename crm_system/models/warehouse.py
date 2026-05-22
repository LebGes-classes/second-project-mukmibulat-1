from typing import Dict
from models.employee import Employee
from models.warehouse_cell import WarehouseCell


class Warehouse:
    """Класс склада.

    Args:
        warehouse_id (str): ID склада.
        name (str): Название.
        address (str): Адрес.
        manager (Employee): Ответственный сотрудник.
        income (float): Доходы.
        expenses (float): Расходы.
        is_open (bool): Открыт ли склад.
    """

    def __init__(self, warehouse_id: str, name: str, address: str, manager: Employee,
                 income: float = 0.0, expenses: float = 0.0, is_open: bool = True):
        self._warehouse_id = warehouse_id
        self._name = name
        self._address = address
        self._manager = manager
        self._income = max(0.0, income)
        self._expenses = max(0.0, expenses)
        self._is_open = is_open
        self._cells: Dict[str, WarehouseCell] = {}

    @property
    def warehouse_id(self) -> str:
        """Возвращает ID склада.

        Returns:
            str: ID склада.
        """

        return self._warehouse_id

    @property
    def name(self) -> str:
        """Возвращает название склада.

        Returns:
            str: Название.
        """

        return self._name

    @property
    def is_open(self) -> bool:
        """Открыт ли склад.

        Returns:
            bool: True если открыт.
        """

        return self._is_open

    def set_open(self, open_status: bool):
        """Открыть или закрыть склад.

        Args:
            open_status (bool): Новый статус.
        """

        self._is_open = open_status

    @property
    def manager(self) -> Employee:
        """Возвращает менеджера склада.

        Returns:
            Employee: Менеджер.
        """

        return self._manager

    @manager.setter
    def manager(self, value: Employee):
        """Устанавливает менеджера склада.

        Args:
            value (Employee): Новый менеджер.

        Raises:
            ValueError: Если сотрудник уволен.
        """

        if value.is_working:
            self._manager = value
        else:
            raise ValueError("Нельзя назначить уволенного сотрудника")

    @property
    def cells(self) -> Dict[str, WarehouseCell]:
        """Возвращает копию словаря ячеек.

        Returns:
            Dict[str, WarehouseCell]: Ячейки склада.
        """

        return self._cells.copy()

    @property
    def income(self) -> float:
        """Возвращает доходы.

        Returns:
            float: Доходы.
        """

        return self._income

    @income.setter
    def income(self, value: float):
        """Устанавливает доходы.

        Args:
            value (float): Новое значение.
        """

        self._income = max(0.0, value)

    @property
    def expenses(self) -> float:
        """Возвращает расходы.

        Returns:
            float: Расходы.
        """

        return self._expenses

    @expenses.setter
    def expenses(self, value: float):
        """Устанавливает расходы.

        Args:
            value (float): Новое значение.
        """

        self._expenses = max(0.0, value)

    def calculate_profit(self) -> float:
        """Вычисляет прибыль склада.

        Returns:
            float: Доходы минус расходы.
        """

        return self._income - self._expenses

    def get_product_quantity(self, product_number: str) -> int:
        """Суммарное количество товара на всех ячейках.

        Args:
            product_number (str): Артикул.

        Returns:
            int: Общее количество.
        """

        total = 0

        for cell in self._cells.values():
            total += cell.products.get(product_number, 0)

        return total

    def get_info(self) -> str:
        """Возвращает информацию о складе.

        Returns:
            str: Строка с данными.
        """

        return f"Склад: {self._name}, Адрес: {self._address}, Ответственный: {self._manager.get_full_name()}, Текущая прибыль: {self.calculate_profit()} руб."

    def to_dict(self) -> dict:
        """Преобразует объект в словарь.

        Returns:
            dict: Данные для сериализации.
        """

        return {
            "warehouse_id": self._warehouse_id,
            "name": self._name,
            "address": self._address,
            "manager": self._manager.to_dict(),
            "income": self._income,
            "expenses": self._expenses,
            "is_open": self._is_open,
            "cells": [c.to_dict() for c in self._cells.values()]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            Warehouse: Новый экземпляр.
        """

        manager = Employee.from_dict(data["manager"])
        warehouse = cls(
            warehouse_id=data["warehouse_id"],
            name=data["name"],
            address=data["address"],
            manager=manager,
            income=data.get("income", 0.0),
            expenses=data.get("expenses", 0.0),
            is_open=data.get("is_open", True)
        )

        for cell_data in data.get("cells", []):
            cell = WarehouseCell.from_dict(cell_data)
            warehouse._cells[cell.cell_id] = cell

        return warehouse
