import re
    
def validateRnc(rnc):
    pattern = r'^\d{3}-?\d{7}-?\d{1}$'

    if re.match(pattern, rnc):
        return True
    else:
        return False