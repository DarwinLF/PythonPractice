import re
    
def validateRnc(rnc):
    pattern = r'^\d{3}-?\d{7}-?\d{1}$'

    if re.match(pattern, rnc):
        return True
    else:
        return False
    
def validateIsbn13(isbn):
    pattern = r'^\d{3}-?\d{1}-?\d{3}-?\d{5}-?\d{1}$'

    if re.match(pattern, isbn):
        return True
    else:
        return False