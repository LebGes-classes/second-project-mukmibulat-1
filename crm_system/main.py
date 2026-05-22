from services import CRMService
from models import Employee, Customer, Product, Warehouse, WarehouseCell, SalesPoint
from utils import safe_positive_int, safe_positive_float

def show_menu():
    """Отображает главное меню."""
    print("\n" + "=" * 10 + " МЕНЮ УПРАВЛЕНИЯ CRM/WMS " + "=" * 10)
    print("1.  Внести новый тип товара в каталог")
    print("2.  Зарегистрировать (открыть) склад")
    print("3.  Добавить ячейку хранения на склад")
    print("4.  Сделать закупку товара (Поставка на склад)")
    print("5.  Переместить товар между ячейками/складами")
    print("6.  Зарегистрировать пункт розничных продаж")
    print("7.  Переместить товар со склада в пункт продаж")
    print("8.  Оформить продажу клиенту (Создать заказ)")
    print("9.  Оформить возврат от покупателя")
    print("10. Изменить ответственное лицо (менеджера) склада")
    print("11. Изменить статус работы (закрыть/открыть) склад или точку")
    print("12. Показать информацию о конкретном складе")
    print("13. Показать информацию о конкретном пункте продаж")
    print("14. Показать товары, доступные к закупке (закончившиеся)")
    print("15. Финансовая аналитика доходности компании")
    print("16. Нанять нового сотрудника")
    print("17. Уволить сотрудника")
    print("18. Добавить клиента в базу")
    print("19. Вывести справочные списки (Товары, Персонал, Клиенты)")
    print("20. Сохранить изменения")
    print("0.  Выход из системы")

def main():
    """Точка входа в приложение."""
    crm = CRMService()

    while True:
        show_menu()
        choice = input("\nВыберите номер действия: ")

        match choice:
            case "1":
                p = Product(
                    number=input("Уникальный артикул: "),
                    card_id=input("ID карточки товара: "),
                    name=input("Название: "),
                    supplier=input("Поставщик: "),
                    manufacturer=input("Производитель: "),
                    cost=safe_positive_float("Закупочная себестоимость: ")
                )
                crm.register_product_in_catalog(p)

            case "2":
                emp_id = input("ID сотрудника-менеджера: ")
                manager = crm.employees.get(emp_id)
                if not manager:
                    print("Сотрудник не найден в базе данных системы! Сначала наймите сотрудника (пункт 16).")
                    continue
                wh = Warehouse(
                    warehouse_id=input("ID нового склада: "),
                    name=input("Название: "),
                    address=input("Адрес: "),
                    manager=manager
                )
                crm.open_warehouse(wh)

            case "3":
                wh_id = input("ID склада: ")
                cell = WarehouseCell(
                    cell_id=input("Номер/ID ячейки: "),
                    max_capacity=safe_positive_int("Максимальная вместимость (шт): ")
                )
                crm.add_cell_to_warehouse(wh_id, cell)

            case "4":
                crm.purchase_product(
                    warehouse_id=input("ID склада: "),
                    cell_id=input("ID ячейки: "),
                    product_number=input("Артикул товара: "),
                    quantity=safe_positive_int("Количество единиц: ")
                )

            case "5":
                crm.transfer_product(
                    from_wh_id=input("Из склада (ID): "),
                    from_cell_id=input("Из ячейки (ID): "),
                    to_wh_id=input("В склад (ID): "),
                    to_cell_id=input("В ячейку (ID): "),
                    product_number=input("Артикул товара: "),
                    quantity=safe_positive_int("Количество для перемещения: ")
                )

            case "6":
                sp = SalesPoint(
                    sales_point_id=input("ID торговой точки: "),
                    name=input("Название магазина: "),
                    address=input("Адрес: ")
                )
                crm.open_sales_point(sp)

            case "7":
                crm.supply_sales_point_from_warehouse(
                    warehouse_id=input("ID склада: "),
                    cell_id=input("ID ячейки: "),
                    sales_point_id=input("ID торговой точки: "),
                    product_number=input("Артикул товара: "),
                    quantity=safe_positive_int("Количество к отправке в магазин: ")
                )

            case "8":
                crm.create_order(
                    order_id=input("Задайте ID заказа: "),
                    customer_id=input("ID покупателя: "),
                    sales_point_id=input("ID магазина продажи: "),
                    product_number=input("Артикул товара: "),
                    quantity=safe_positive_int("Количество шт: ")
                )

            case "9":
                crm.return_product(
                    sales_point_id=input("ID магазина: "),
                    product_number=input("Артикул товара: "),
                    quantity=safe_positive_int("Количество возвращаемых единиц: ")
                )

            case "10":
                crm.change_warehouse_manager(
                    warehouse_id=input("ID склада: "),
                    employee_id=input("ID нового сотрудника: ")
                )

            case "11":
                t = input("Что меняем? (1 - склад, 2 - магазин): ")
                obj_id = input("Введите ID объекта: ")
                action = input("Что сделать? (1 - закрыть, 2 - открыть): ")

                if t == "1":
                    if action == "1":
                        crm.close_warehouse(obj_id)
                    elif action == "2":
                        crm.open_warehouse_by_id(obj_id)
                    else:
                        print("Неверное действие")

                elif t == "2":
                    if action == "1":
                        crm.close_sales_point(obj_id)
                    elif action == "2":
                        crm.open_sales_point_by_id(obj_id)
                    else:
                        print("Неверное действие")
                else:
                    print("Неверный тип объекта")

            case "12":
                crm.show_warehouse_info(input("ID склада: "))

            case "13":
                crm.show_sales_point_info(input("ID магазина: "))

            case "14":
                crm.show_out_of_stock_products()

            case "15":
                crm.show_financial_report()

            case "16":
                emp = Employee(
                    first_name=input("Имя: "),
                    last_name=input("Фамилия: "),
                    age=safe_positive_int("Возраст: "),
                    phone=input("Телефон: "),
                    email=input("Email: "),
                    employee_id=input("ID сотрудника: "),
                    position=input("Должность: "),
                    salary=safe_positive_float("Оклад: ")
                )
                crm.hire_employee(emp)

            case "17":
                crm.dismiss_employee(input("ID сотрудника для увольнения: "))

            case "18":
                cust = Customer(
                    first_name=input("Имя: "),
                    last_name=input("Фамилия: "),
                    age=safe_positive_int("Возраст: "),
                    phone=input("Телефон: "),
                    email=input("Email: "),
                    customer_id=input("Задайте ID клиента: ")
                )
                crm.add_customer(cust)

            case "19":
                sub_choice = input("Показать: 1 - Каталог, 2 - Сотрудников, 3 - Клиентов: ")

                if sub_choice == "1":
                    for p in crm.catalog.values():
                        print(p.get_info())

                elif sub_choice == "2":
                    for e in crm.employees.values():
                        print(e.get_info())

                elif sub_choice == "3":
                    for c in crm.customers.values():
                        print(c.get_info())
                else:
                    print("Неверный выбор")

            case "20":
                crm.save_data()
                print("Изменения сохранены.")

            case "0":
                crm.save_data()
                print("Данные сохранены. Работа программы успешно завершена.")
                break

            case _:
                print("Команда не распознана, попробуйте снова.")

if __name__ == "__main__":
    main()