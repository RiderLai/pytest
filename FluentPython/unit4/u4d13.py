from unicodedata import normalize


def nfc_equal(str1, str2):
    """nfc格式化对比"""
    return normalize('NFC', str1) == normalize('NFC', str2)


def fold_equal(str1, str2):
    """大小写折叠对比"""
    return normalize('NFC', str1).casefold() == normalize('NFC', str2).casefold()


print(fold_equal('A', 'a'))