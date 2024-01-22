from conf import svup_sql
from func import write_styling_excel


async def get_svup_worker() -> str:
    """Вытаскиваем всех пользователей и возвращаем путь до файла"""
    sql = "select ID, Name, FirstName, MidName from dbo.pList"

    df = svup_sql(sql)
    if not len(df):
        return ""

    filename = "/tmp/SVUP_Worker.xlsx"
    write_styling_excel(filename, df, "svup")
    return filename
