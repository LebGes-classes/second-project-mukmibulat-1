def safe_positive_int(msg: str) -> int:
    """Запрашивает целое положительное число.

    Args:
        msg (str): Сообщение для ввода.

    Returns:
        int: Введённое неотрицательное число.
    """

    while True:
        try:
            val = int(input(msg))
            if val < 0:
                print("Число не может быть отрицательным. Повторите ввод.")
                continue

            return val

        except ValueError:
            print("Ошибка ввода! Введите целое число.")

def safe_positive_float(msg: str) -> float:
    """Запрашивает вещественное положительное число.

    Args:
        msg (str): Сообщение для ввода.

    Returns:
        float: Введённое неотрицательное число.
    """

    while True:
        try:
            val = float(input(msg))
            if val < 0:
                print("Число не может быть отрицательным. Повторите ввод.")
                continue

            return val

        except ValueError:
            print("Ошибка ввода! Введите число (целое или дробное).")