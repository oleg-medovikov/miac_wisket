import pandas as pd


def write_styling_excel_file(path: str, df: pd.DataFrame, sheet_name: str, index=False):
    "Функция записывает файл, атоматически расширяя столбцы до 45"

    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index, na_rep='NaN')

        # автонастройка ширины колонок
        # решил что больше ничего и не нужно
        for column in df:
            width = max(df[column].astype(str).map(len).max(), len(column))
            width += 5
            if width > 45:
                width = 45

            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, width)

        if index:
            for _ in df.index.names:
                col_idx = df.index.names.index(_)
                width = 35
                writer.sheets[sheet_name].set_column(col_idx, col_idx, width)

        writer.save()
