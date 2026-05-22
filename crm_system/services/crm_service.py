from typing import Dict
from models import Product, Employee, Customer, Warehouse, WarehouseCell, SalesPoint, Order
from services.data_manager import DataManager


class CRMService:
    """Основной сервис бизнес-логики."""

    def __init__(self):
        self.catalog: Dict[str, Product] = {}
        self.employees: Dict[str, Employee] = {}
        self.customers: Dict[str, Customer] = {}
        self.warehouses: Dict[str, Warehouse] = {}
        self.sales_points: Dict[str, SalesPoint] = {}
        self.orders: Dict[str, Order] = {}
        DataManager.load_data(self)

    def save_data(self):
        """Сохраняет данные."""

        DataManager.save_data(self)

    def register_product_in_catalog(self, product: Product):
        """Регистрирует товар в каталоге.

        Args:
            product (Product): Товар.
        """

        if product.number in self.catalog:
            print("[Ошибка] Товар с таким артикулом уже зарегистрирован.")

            return

        self.catalog[product.number] = product

        print(f"Товар {product.name} успешно внесен в глобальный справочник.")

    def open_warehouse(self, warehouse: Warehouse):
        """Открывает новый склад.

        Args:
            warehouse (Warehouse): Склад.
        """

        self.warehouses[warehouse.warehouse_id] = warehouse

        print(f"Склад '{warehouse.name}' успешно открыт.")

    def open_warehouse_by_id(self, warehouse_id: str):
        """Открывает существующий склад.

        Args:
            warehouse_id (str): ID склада.
        """

        wh = self.warehouses.get(warehouse_id)

        if wh:
            wh.set_open(True)
            print(f"Склад {wh.name} открыт.")
        else:
            print("[Ошибка] Склад не найден.")

    def close_warehouse(self, warehouse_id: str):
        """Закрывает склад.

        Args:
            warehouse_id (str): ID склада.
        """

        wh = self.warehouses.get(warehouse_id)

        if wh:
            wh.set_open(False)
            print(f"Склад {wh.name} закрыт.")
        else:
            print("[Ошибка] Склад не найден.")

    def add_cell_to_warehouse(self, warehouse_id: str, cell: WarehouseCell):
        """Добавляет ячейку на склад.

        Args:
            warehouse_id (str): ID склада.
            cell (WarehouseCell): Ячейка.
        """

        warehouse = self.warehouses.get(warehouse_id)

        if not warehouse:
            print("[Ошибка] Склад не найден.")

            return

        if cell.cell_id in warehouse._cells:
            print("[Ошибка] Ячейка с таким ID на этом складе уже есть.")

            return

        warehouse._cells[cell.cell_id] = cell

        print(f"Ячейка {cell.cell_id} добавлена на склад {warehouse.name}.")

    def change_warehouse_manager(self, warehouse_id: str, employee_id: str):
        """Меняет менеджера склада.

        Args:
            warehouse_id (str): ID склада.
            employee_id (str): ID нового менеджера.
        """

        warehouse = self.warehouses.get(warehouse_id)
        employee = self.employees.get(employee_id)

        if not warehouse or not employee:
            print("[Ошибка] Склад или сотрудник не найден.")

            return

        if not employee.is_working:
            print("[Ошибка] Нельзя назначить уволенного сотрудника.")

            return

        warehouse.manager = employee

        print(f"Новый ответственный за склад {warehouse.name}: {employee.get_full_name()}")

    def purchase_product(self, warehouse_id: str, cell_id: str, product_number: str, quantity: int):
        """Закупает товар и размещает на складе.

        Args:
            warehouse_id (str): ID склада.
            cell_id (str): ID ячейки.
            product_number (str): Артикул.
            quantity (int): Количество.
        """

        warehouse = self.warehouses.get(warehouse_id)

        if not warehouse or not warehouse.is_open:
            print("[Ошибка] Склад не найден или закрыт.")

            return

        if product_number not in self.catalog:
            print("[Ошибка] Сначала зарегистрируйте товар в каталоге.")

            return

        cell = warehouse._cells.get(cell_id)

        if not cell:
            print("[Ошибка] Ячейка не найдена на данном складе.")

            return

        product = self.catalog[product_number]

        if cell.add_product(product_number, quantity):
            warehouse.expenses += product.cost * quantity
            print(f"Закупка проведена. {quantity} шт. размещено в ячейку {cell_id}.")
        else:
            print("Ошибка Не удалось разместить товар. Превышена емкость ячейки.")

    def transfer_product(self, from_wh_id: str, from_cell_id: str, to_wh_id: str, to_cell_id: str,
                         product_number: str, quantity: int):
        """Перемещает товар между складами.

        Args:
            from_wh_id (str): Склад-отправитель.
            from_cell_id (str): Ячейка-отправитель.
            to_wh_id (str): Склад-получатель.
            to_cell_id (str): Ячейка-получатель.
            product_number (str): Артикул.
            quantity (int): Количество.
        """

        wh_source = self.warehouses.get(from_wh_id)
        wh_dest = self.warehouses.get(to_wh_id)

        if not wh_source or not wh_dest or not wh_source.is_open or not wh_dest.is_open:
            print("[Ошибка] Ошибка доступа к складам перемещения.")

            return

        cell_source = wh_source._cells.get(from_cell_id)
        cell_dest = wh_dest._cells.get(to_cell_id)

        if not cell_source or not cell_dest:
            print("[Ошибка] Ячейка отправителя или получателя не найдена.")

            return

        if product_number not in self.catalog:
            print("[Ошибка] Товар не зарегистрирован в каталоге.")

            return

        if cell_dest.get_current_load() + quantity > cell_dest.max_capacity:
            print("[Ошибка] Ячейка назначения переполнена.")

            return

        if cell_source.remove_product(product_number, quantity):
            cell_dest.add_product(product_number, quantity)
            print("Перемещение успешно выполнено.")
        else:
            print("[Ошибка] Недостаточно товара в исходной ячейке.")

    def open_sales_point(self, sales_point: SalesPoint):
        """Открывает новую торговую точку.

        Args:
            sales_point (SalesPoint): Точка продаж.
        """

        self.sales_points[sales_point.sales_point_id] = sales_point
        print(f"Точка розничных продаж '{sales_point.name}' открыта.")

    def open_sales_point_by_id(self, sales_point_id: str):
        """Открывает существующую точку.

        Args:
            sales_point_id (str): ID точки.
        """

        sp = self.sales_points.get(sales_point_id)

        if sp:
            sp.set_open(True)
            print(f"Точка {sp.name} открыта.")
        else:
            print("[Ошибка] Точка продаж не найдена.")

    def close_sales_point(self, sales_point_id: str):
        """Закрывает точку продаж.

        Args:
            sales_point_id (str): ID точки.
        """

        sp = self.sales_points.get(sales_point_id)

        if sp:
            sp.set_open(False)
            print(f"Точка {sp.name} закрыта.")
        else:
            print("[Ошибка] Точка продаж не найдена.")

    def supply_sales_point_from_warehouse(self, warehouse_id: str, cell_id: str, sales_point_id: str,
                                          product_number: str, quantity: int):
        """Поставляет товар со склада в точку продаж.

        Args:
            warehouse_id (str): ID склада.
            cell_id (str): ID ячейки.
            sales_point_id (str): ID точки.
            product_number (str): Артикул.
            quantity (int): Количество.
        """

        warehouse = self.warehouses.get(warehouse_id)
        sp = self.sales_points.get(sales_point_id)

        if not warehouse or not sp or not warehouse.is_open or not sp.is_open:
            print("[Ошибка] Склад или магазин недоступны/закрыты.")

            return

        cell = warehouse._cells.get(cell_id)

        if not cell:
            print("[Ошибка] Ячейка склада не найдена.")

            return

        if product_number not in self.catalog:
            print("[Ошибка] Товар не зарегистрирован в каталоге.")

            return

        if cell.remove_product(product_number, quantity):
            sp._products[product_number] = sp._products.get(product_number, 0) + quantity
            print(f"Товар доставлен на витрину магазина {sp.name}.")
        else:
            print("[Ошибка] Недостаточно запасов в указанной ячейке.")

    def create_order(self, order_id: str, customer_id: str, sales_point_id: str, product_number: str, quantity: int):
        """Создаёт заказ на продажу.

        Args:
            order_id (str): ID заказа.
            customer_id (str): ID клиента.
            sales_point_id (str): ID точки.
            product_number (str): Артикул.
            quantity (int): Количество.
        """

        customer = self.customers.get(customer_id)
        sp = self.sales_points.get(sales_point_id)

        if not customer or not sp:
            print("[Ошибка] Клиент или торговая точка не зарегистрированы.")

            return

        if not sp.is_open:
            print("[Ошибка] Данная торговая точка закрыта.")

            return

        available = sp._products.get(product_number, 0)

        if available < quantity:
            print(f"[Ошибка] На витринах магазина нет нужного количества. Доступно: {available}")

            return

        product = self.catalog.get(product_number)

        if not product:
            print("[Ошибка] Товар не найден в каталоге.")

            return

        total_price = product.cost * 1.3 * quantity
        sp._products[product_number] -= quantity
        sp.income += total_price
        new_order = Order(order_id, customer, product_number, quantity, total_price)
        self.orders[order_id] = new_order

        print(f"Заказ оформлен! Сумма: {total_price} руб.")

    def return_product(self, sales_point_id: str, product_number: str, quantity: int):
        """Оформляет возврат товара.

        Args:
            sales_point_id (str): ID точки.
            product_number (str): Артикул.
            quantity (int): Количество.
        """

        sp = self.sales_points.get(sales_point_id)

        if not sp or not sp.is_open:
            print("[Ошибка] Магазин не найден или закрыт.")

            return

        product = self.catalog.get(product_number)

        if not product:
            print("[Ошибка] Неизвестный товар.")

            return

        available = sp._products.get(product_number, 0)

        if quantity > available:
            print(f"[Ошибка] Нельзя вернуть больше, чем есть на витрине. Доступно: {available}")

            return

        sp._products[product_number] = sp._products.get(product_number, 0) + quantity
        sp.income -= (product.cost * 1.3 * quantity)

        print("Возврат успешно проведен.")

    def hire_employee(self, employee: Employee):
        """Нанимает сотрудника.

        Args:
            employee (Employee): Сотрудник.
        """

        self.employees[employee.employee_id] = employee

        print(f"Сотрудник {employee.get_full_name()} успешно оформлен в штат.")

    def dismiss_employee(self, employee_id: str):
        """Увольняет сотрудника.

        Args:
            employee_id (str): ID сотрудника.
        """

        employee = self.employees.get(employee_id)

        if employee:
            employee.dismiss()
            print(f"Сотрудник {employee.get_full_name()} официально уволен.")
        else:
            print("[Ошибка] Сотрудник не найден.")

    def add_customer(self, customer: Customer):
        """Добавляет клиента.

        Args:
            customer (Customer): Клиент.
        """

        if customer.customer_id in self.customers:
            print("[Ошибка] Клиент с таким ID уже существует.")

            return

        self.customers[customer.customer_id] = customer

        print(f"Клиент {customer.get_full_name()} успешно добавлен в базу.")

    def show_warehouse_info(self, warehouse_id: str):
        """Показывает информацию о складе.

        Args:
            warehouse_id (str): ID склада.
        """

        warehouse = self.warehouses.get(warehouse_id)

        if not warehouse:
            print("[Ошибка] Склад не найден.")

            return

        print(f"\n--- {warehouse.get_info()} (Статус открытия: {'открыт' if warehouse.is_open else 'закрыт'}) ---")

        print("Заполненность по ячейкам:")

        for cell in warehouse._cells.values():
            print(f"  * {cell.get_info()}")
            for p_num, qty in cell.products.items():
                product = self.catalog.get(p_num)
                p_name = product.name if product else "НЕИЗВЕСТНЫЙ ТОВАР"

                print(f"    - Товар [{p_num}] {p_name}: {qty} шт.")

    def show_sales_point_info(self, sales_point_id: str):
        """Показывает информацию о точке продаж.

        Args:
            sales_point_id (str): ID точки.
        """

        sp = self.sales_points.get(sales_point_id)

        if not sp:
            print("[Ошибка] Точка продаж не найдена.")

            return

        print(f"\n--- {sp.get_info()} (Статус: {'открыт' if sp.is_open else 'закрыт'}) ---")

        print("Товары на витрине:")

        for p_num, qty in sp._products.items():
            product = self.catalog.get(p_num)
            p_name = product.name if product else "НЕИЗВЕСТНЫЙ ТОВАР"

            print(f"    - [{p_num}] {p_name}: {qty} шт.")

    def show_out_of_stock_products(self):
        """Показывает товары, отсутствующие на складах."""

        print("\n=== ТОВАРЫ, ТРЕБУЮЩИЕ ЗАКУПКИ ===")

        found = False

        for p_num, product in self.catalog.items():
            total_qty = 0
            for wh in self.warehouses.values():
                total_qty += wh.get_product_quantity(p_num)
            if total_qty == 0:
                print(f"  * {product.get_info()} - Закончился на всех складах!")
                found = True

        if not found:
            print("Все зарегистрированные товары присутствуют на складах.")

    def show_financial_report(self):
        """Показывает финансовый отчёт."""

        print("\n=== ФИНАНСОВЫЙ ОТЧЕТ ПРЕДПРИЯТИЯ ===")

        total_wh_profit = 0.0
        total_sp_income = 0.0

        print("Склады:")

        for w in self.warehouses.values():
            profit = w.calculate_profit()
            print(f"  * {w.name}: Расходы на закупку={w.expenses}, Прибыль={profit}")
            total_wh_profit += profit

        print("Розничные точки:")

        for s in self.sales_points.values():
            print(f"  * {s.name}: Оборот (Доход)={s.income}")
            total_sp_income += s.income

        print("-" * 30)

        print(f"Итоговый финансовый результат сети: {total_wh_profit + total_sp_income} руб.")