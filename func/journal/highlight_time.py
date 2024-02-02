import pandas as pd


def highlight_time(val):
    """
    Функция для выделения ячеек со временем:
    - красным, если время больше 09:00 и меньше 17:30
    """
    start = pd.to_datetime("09:00", format="%H:%M").time()
    start_range = pd.to_datetime("09:30", format="%H:%M").time()
    end = pd.to_datetime("17:30", format="%H:%M").time()
    end_range = pd.to_datetime("17:00", format="%H:%M").time()
    try:
        val = pd.to_datetime(val, format="%H:%M").time()
    except ValueError:
        return "background-color: #fdd"

    color = {
        start_range < val < end_range: "red",
        start < val < start_range: "#FF9900",
        end_range < val < end: "#ff9900",
    }.get(True, "green")

    return "color: %s" % color
