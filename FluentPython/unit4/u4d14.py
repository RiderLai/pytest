import unicodedata
import string


def shave_marks(txt):
    """去掉全部变暗符号"""
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)


a1 = unicodedata.normalize('NFC', 'e\u0301')
print(a1)
print(shave_marks(a1))