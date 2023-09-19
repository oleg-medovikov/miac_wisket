def to_rus(STRING) -> str:
    d = {}
    ANG = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''
    RUS = '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'''

    for c1, c2 in zip(ANG, RUS):
        d[c1] = c2

    return STRING.translate(str.maketrans(d))
