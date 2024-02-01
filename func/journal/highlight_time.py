import pandas as pd


def highlight_time(val):
    """
    Функция для выделения ячеек со временем:
    - красным, если время больше 09:00 и меньше 17:30
    """
    start = pd.to_datetime("09:00", format="%H:%M").time()
    end = pd.to_datetime("17:30", format="%H:%M").time()
    try:
        val = pd.to_datetime(val, format="%H:%M:%S").time()
    except ValueError:
        return "background-color: #ffcccc"

    color = "red" if start < val < end else "green"
    return "color: %s" % color
