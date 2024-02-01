from pandas.io.formats.style import Styler
from openpyxl.styles import Alignment
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

column_widths = {1: 10, 2: 60, 3: 20, 4: 25, 5: 15}


def write_file(df: Styler, filename: str):
    # Сохраняем стилизованный DataFrame в файл Excel
    df.to_excel(filename, sheet_name="tabel", engine="openpyxl")

    # Загружаем рабочий лист
    wb = load_workbook(filename)
    ws = wb["tabel"]

    for cell in ws["B"]:
        cell.alignment = Alignment(
            wrap_text=True, vertical="center", horizontal="center"
        )

    for k, v in column_widths.items():
        ws.column_dimensions[get_column_letter(k)].width = v

    # Устанавливаем фиксированную ширину для остальных колонок
    for i in range(len(column_widths) + 1, len(df.columns) + len(column_widths) + 1):
        ws.column_dimensions[get_column_letter(i)].width = 17  # Фиксированная ширина 20

    # Сохраняем изменения
    wb.save(filename)
