def str_to_dec(data):
    """Converts a string to a list of decimal values.

    The string must be codified as bytes.
    
    Example:

        >>> str_to_hex(b'UUU')
        [85, 85, 85]
        >>> str_to_hex(b'01234')
        [48, 49, 50, 51, 52]

    Parameters
    ----------
        data : list or bytes
            String to be converted

    Returns
    -------
    list
        List with the converted values.
    
    """
    data_hex = [int(hex(d), 16) for d in data]

    return data_hex


def u8_to_u32(d, msb=False):
    """Converts a list of bytes to a 32-bit value.

    Example: 
        >>> data = u8_to_u32([0x11, 0x22, 0x33, 0x44])
        >>> data
        287454020
        >>> hex(data)
        '0x11223344'
        >>> data = u8_to_u32(b'UUUU')
        >>> hex(data)
        '0x55555555'
        
    Parameters
    ----------
    d : list or str
        List or binary string with the values to be converted. In either
        case, the list or string must contain at least 4 elements or
        characters; respectively.

    msb : bool
        Defines if the first element is the most significant byte. By
        default, it is `False`.

    Returns
    -------
    int, list
        Converted value.

    """
    if msb is True:
        d = d[::-1]

    n = int( len(d) / 4 )

    c = [0] * n
    for i in range(n):
        j = 4 * i
        c[i] = (d[j + 3] << 24) + (d[j + 2] << 16) + (d[j + 1] << 8) + d[0]

    if len(c) == 1:
        c = c[0]
        
    return c


def u8_to_u16(d, msb=False):
    """Converts a list of bytes or a string to a 16-bit value.

    Example: 
        >>> data = u8_to_u16([0x11, 0x22])
        >>> data
        4386
        >>> hex(data)
        '0x1122'
        >>> data = u8_to_u16(b'UU')
        >>> hex(data)
        '0x5555'

    Parameters
    ----------
    d : list or str
        List or binary string with the values to be converted. In either
        case, the list or string must contain at least 2 elements or
        characters; respectively.

    msb : bool
        Defines if the first element is the most significant byte. By
        default, it is `False`.
    
    Returns
    -------
    int
        Converted value.

    """
    if msb is True:
        d = d[::-1]

    n = int( len(d) / 2 )

    c = [0] * n
    for i in range(n):
        c[i] = (d[2 * i + 1] << 8) + d[2 * i]

    if len(c) == 1:
        c = c[0]
    
    return c



def u32_to_u8(d, msb=False):
    """Converts a 32-bit value to a list with 4 bytes.

    Parameters
    ----------
    d : int
        32-bit value.
        
    msb : bool
        Defines if the first element of the resulting list should be the most
        significant byte. By default, it is `False`.
    
    Returns
    -------
    list
        List with decimals.
        
    """
    if type(d) is int:
        d = [d]
    
    if msb is False:
        data = [[(i >> (8 * k)) & 0xFF for k in range(4)] for i in d]
    else:
        data = [[(i >> (8 * (3-k))) & 0xFF for k in range(4)] for i in d]

    if len(data) == 1:
        data = data[0]
    
    return data


def u16_to_u8(d, msb=False):
    """Converts a 16-bit value to a list with 2 bytes.

    Parameters
    ----------
    d : int, list
        16-bit value.
        
    msb : bool
        Defines if the first element of the resulting list should be the most
        significant byte. By default, it is `False`.
        
    Returns
    -------
    list
        List with decimals.
        
    """
    if type(d) is int:
        d = [d]
    
    if msb is False:
        data = [[(i >> (8 * k)) & 0xFF for k in range(2)] for i in d]
    else:
        data = [[(i >> (8 * (1-k))) & 0xFF for k in range(2)] for i in d]

    if len(data) == 1:
        data = data[0]
    
    return data
