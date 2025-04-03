import string

# Base62 characters (0-9, a-z, A-Z)
BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode_base62(num: int) -> str:
    """
    Convert number to base62 string.
    
    Args:
        num (int): Number to convert
        
    Returns:
        str: Base62 encoded string
    """
    if num == 0:
        return BASE62[0]
    
    arr = []
    base = len(BASE62)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62[rem])
    arr.reverse()
    return ''.join(arr)
