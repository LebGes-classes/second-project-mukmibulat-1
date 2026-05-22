import json
import os
from models import Product, Employee, Customer, Warehouse, SalesPoint, Order

class DataManager:
    FILE_PATH = "database.json"

    @staticmethod
    def save_data(crm):
        """Сохраняет все данные в JSON файл.

        Args:
            crm: Экземпляр CRMService.
        """

        data = {
            "catalog": [p.to_dict() for p in crm.catalog.values()],
            "employees": [e.to_dict() for e in crm.employees.values()],
            "customers": [c.to_dict() for c in crm.customers.values()],
            "warehouses": [w.to_dict() for w in crm.warehouses.values()],
            "sales_points": [s.to_dict() for s in crm.sales_points.values()],
            "orders": [o.to_dict() for o in crm.orders.values()]
        }
        with open(DataManager.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Данные сохранены в database.json")

    @staticmethod
    def load_data(crm):
        """Загружает данные из JSON файла.

        Args:
            crm: Экземпляр CRMService.
        """

        if not os.path.exists(DataManager.FILE_PATH):
            return
        try:
            with open(DataManager.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, IOError):
            return

        crm.catalog.clear()
        crm.employees.clear()
        crm.customers.clear()
        crm.warehouses.clear()
        crm.sales_points.clear()
        crm.orders.clear()

        for item in data.get("catalog", []):
            p = Product.from_dict(item)
            crm.catalog[p.number] = p

        for item in data.get("employees", []):
            e = Employee.from_dict(item)
            crm.employees[e.employee_id] = e

        for item in data.get("customers", []):
            c = Customer.from_dict(item)
            crm.customers[c.customer_id] = c

        for item in data.get("warehouses", []):
            w = Warehouse.from_dict(item)
            crm.warehouses[w.warehouse_id] = w

        for item in data.get("sales_points", []):
            s = SalesPoint.from_dict(item)
            crm.sales_points[s.sales_point_id] = s

        for item in data.get("orders", []):
            o = Order.from_dict(item)
            crm.orders[o.order_id] = o