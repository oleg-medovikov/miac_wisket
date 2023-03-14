from pandas import DataFrame
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def create_tabel(WDS: list) -> 'DataFrame':
    FIOs = ['', '']
    event = ['день недели', '']

    for WD in WDS:
        FIO = WD.name + ' ' + WD.first_name[0] + '. ' + WD.mid_name[0] + '.'
        if FIO not in FIOs:
            FIOs.append(FIO)
            FIOs.append(FIO)
            event.append('время прихода')
            event.append('время ухода')

    df = DataFrame(index=[FIOs, event])
    df.index.names = ['сотрудник', 'событие']

    for WD in WDS:
        FIO = WD.name + ' ' + WD.first_name[0] + '. ' + WD.mid_name[0] + '.'
        DAY = WD.day.strftime('%d.%m.%Y')
        df.loc[('', 'день недели'),    DAY] = WD.day.strftime('%A')
        df.loc[(FIO, 'время прихода'), DAY] = WD.time_start
        df.loc[(FIO, 'время ухода'),   DAY] = WD.time_stop

    df = df.fillna('')

    return df
