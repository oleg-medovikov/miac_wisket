import pandas as pd


def highlight_time(val):
    """
    Функция для выделения ячеек со временем:
    если : внутри времени то это приход или уход:
    - красным, если время больше 09:00 и меньше 17:30
    если ; внутри времени то это время работы
    - красным если меньше 8 часов
    если . внутри времени то это время вне миац
    - красным если больше часа
    """
    if val == "":
        return "background-color: #fdd"
    elif ":" in val:
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

    elif ";" in val:
        smena = pd.to_datetime("08:30", format="%H:%M").time()
        smena_range = pd.to_datetime("08:00", format="%H:%M").time()
        try:
            val = pd.to_datetime(val, format="%H;%M").time()
        except ValueError:
            return "background-color: #fdd"
        color = {
            val < smena_range: "red",
            smena_range <= val < smena: "#FF9900",
            val >= smena: "green",
        }.get(True, "green")
        return "color: %s" % color

    elif "." in val:
        lanch = pd.to_datetime("00:30", format="%H:%M").time()
        big_lanch = pd.to_datetime("01:00", format="%H:%M").time()
        try:
            val = pd.to_datetime(val, format="%H.%M").time()
        except ValueError:
            return "background-color: #fdd"
        color = {
            val > big_lanch: "red",
            lanch < val <= big_lanch: "#FF9900",
            val <= lanch: "green",
        }.get(True, "green")
        return "color: %s" % color
    else:
        return "background-color: #fdd"
