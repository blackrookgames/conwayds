__all__ = [\
    'LifeSerial',]

from io import\
    StringIO as _StringIO

from ..data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ..data.mod_DataError import\
    DataError as _DataError
from ..data.mod_SerialError import\
    SerialError as _SerialError
from ..data.mod_SerialParse import\
    SerialParse as _SerialParse
from ..data.mod_StringReader import\
    StringReader as _StringReader
from ..helper.mod_const import\
    U32_MAX as _U32_MAX
from ..helper.mod_BadOpError import\
    BadOpError as _BadOpError
from ..img.mod_Img import\
    Img as _Img
from ..img.mod_ImgColor import\
    ImgColor as _ImgColor
from .mod_LifePattern import\
    LifePattern as _LifePattern
from .mod_LifePatternRule import\
    LifePatternRule as _LifePatternRule

class LifeSerial:
    """
    Serialization utility
    """

    #region pattern rle

    @classmethod
    def pattern_from_rle(cls, string:str):
        """
        Deserializes LifePattern data from a str containing RLE data
        
        :param string:
            Input str
        :return:
            Created LifePattern
        :raise SerialError:
            An error occurred during deserialization
        """
        # TODO: Clean up
        def _tempkill():
            return _SerialError("ERROR: Could not deserialize data.")
        def _parsehdrdef(\
                _hdrdefs:dict[str, str],\
                _reader:_StringReader,\
                _stop:int):
            # Leading whitespace; this also checks if there is only whitespace
            while True:
                if _reader.pos >= _stop:
                    return True
                if not _reader.white:
                    break
                _reader.next()
            #region Parse name
            _name_beg = _reader.pos
            while True:
                if _reader.pos >= _stop:
                    raise _SerialError(_reader.error("Equals sign expected"))
                    return False
                if _reader.white or _reader.chr == '=':
                    name = _reader.string[_name_beg:_reader.pos]
                    break
                _reader.next()
            # Name sure name is specified
            if name == '':
                raise _SerialError(_reader.error("Name must precede equals sign"))
                return False
            # Skip over whitespace and equals sign
            while True:
                if _reader.pos >= _stop:
                    raise _SerialError(_reader.error("Equals sign expected"))
                    return False
                if _reader.chr == '=':
                    _reader.next()
                    break
                if not _reader.white:
                    raise _SerialError(_reader.error_unex_char())
                    return False
                _reader.next()
            #endregion
            # Parse value
            while _reader.pos < _stop:
                if not _reader.white:
                    break
                _reader.next()
            _value_beg = _reader.pos
            while _reader.pos < _stop:
                if _reader.white:
                    break
                _reader.next()
            value = _reader.string[_value_beg:_reader.pos]
            # Trailing whitespace
            while _reader.pos < _stop:
                if not _reader.white:
                    raise _SerialError(_reader.error_unex_char())
                    return False
                _reader.next()
            # Add definition
            _hdrdefs[name.lower()] = value
            # Success!!!
            return True
        def _parsexy(_value:str, _name:str):
            _v = _SerialParse.to_int(_value)
            if _v < 0:
                raise _SerialError(f"ERROR: {_name} cannot be negative")
            return True, _v
        def _parserule(_value:str, _name:str):
            def __invalid(__value):
                raise _SerialError(f"{__value} is not a valid pattern rule.")
                return False, _LifePatternRule()
            if len(_value) == 0:
                return __invalid(_value)
            # b
            _char = _value[0]
            if _char == 'B' or _char == 'b':
                _i = 1
            elif _char >= '0' and _char <= '9':
                _i = 0
            else:
                return __invalid(_value)
            _b = []
            while True:
                if _i == len(_value):
                    return __invalid(_value)
                _char = _value[_i]
                _i += 1
                if _char == '/':
                    break
                if _char < '0' or _char > '8':
                    return __invalid(_value)
                _b.append(int(_char))
            if len(_b) == 0:
                return __invalid(_value)
            # s
            _char = _value[_i]
            if _char == 'S' or _char == 's':
                _i += 1
            elif _char < '0' or _char > '9':
                return __invalid(_value)
            _s = []
            while _i < len(_value):
                _char = _value[_i]
                _i += 1
                if _char < '0' or _char > '8':
                    return __invalid(_value)
                _s.append(int(_char))
            if len(_s) == 0:
                return __invalid(_value)
            # Success!!!
            return True, _LifePatternRule(b = tuple(_b), s = tuple(_s))
        def _parsedata(\
                _pattern:_LifePattern,\
                _reader:_StringReader):
            def __inc(\
                    __reader:_StringReader,\
                    __i:int,\
                    __size:int,\
                    __count:int):
                __i += __count
                if __i > __size:
                    raise _SerialError(__reader.error("Exceeded cell count"))
                    return -1
                return __i
            def __writecell(
                    __pattern:_LifePattern,\
                    __i:int,\
                    __value:bool,\
                    __reader:_StringReader,\
                    __size:int):
                # Increment first
                __j = __inc(__reader, __i, __size, 1)
                if __j == -1: return -1
                # Then set value
                __pattern[__i % __pattern.width, __i // __pattern.width] = __value
                return __j
            def __cellvalue(__chr):
                if __chr == 'O' or __chr == 'o':
                    return 1
                if __chr == 'B' or __chr == 'b':
                    return 0
                return -1
            def __nextrow(
                    __pattern:_LifePattern,\
                    __i:int,\
                    __count:int,\
                    __reader:_StringReader,\
                    __size:int):
                # Get X-coordinate
                __x = __i % __pattern.width
                # If at end of line, ignore 1 of them
                if __i > 0 and __x == 0:
                    __count -= 1
                # Next line
                if __count == 0:
                    return __i
                return __inc(__reader, __i, __size, __pattern.width * __count - __x)
            _size = _pattern.width * _pattern.height
            _i = 0
            if _size > 0:
                while True:
                    # End of file (FAIL)?
                    if _reader.eof:
                        raise _SerialError(_reader.error_unex_end())
                        return False
                    # Comment?
                    elif _reader.chr == '#':
                        _reader.skip_line()
                        continue
                    # Whitespace?
                    elif _reader.white:
                        pass
                    # End of data?
                    elif _reader.chr == '!':
                        break
                    # End of line?
                    elif _reader.chr == '$':
                        # Find following
                        _count = 1
                        while True:
                            _chr = _reader.peek()
                            if _chr == '':
                                raise _SerialError(_reader.error_unex_end())
                                return False
                            if _chr == '$':
                                _count += 1
                            elif _chr > ' ':
                                break
                            _reader.next()
                        # Next rows
                        _i = __nextrow(_pattern, _i, _count, _reader, _size)
                        if _i == -1: return False
                    # Cell values (or multiple new rows)?
                    else:
                        # One cell?
                        _cellvalue = __cellvalue(_reader.chr)
                        if _cellvalue != -1:
                            _i = __writecell(_pattern, _i, _cellvalue == 1, _reader, _size)
                            if _i == -1: return False
                        # Multiple?
                        elif _reader.chr >= '0' and _reader.chr <= '9':
                            _count = int(_reader.chr)
                            # Extract rest of number
                            _reader.next()
                            while True:
                                if _reader.eof:
                                    raise _SerialError(_reader.error_unex_end())
                                    return False
                                if _reader.chr < '0' or _reader.chr > '9':
                                    break
                                _count *= 10
                                _count += int(_reader.chr)
                                _reader.next()
                            # Cell?
                            _reader.skip_white()
                            _cellvalue = __cellvalue(_reader.chr)
                            if _cellvalue != -1:
                                while _count > 0:
                                    _i = __writecell(_pattern, _i, _cellvalue == 1, _reader, _size)
                                    if _i == -1: return False
                                    _count -= 1
                            # New rows?
                            elif _reader.chr == '$':
                                _i = __nextrow(_pattern, _i, _count, _reader, _size)
                                if _i == -1: return False
                            # Unexpected (FAIL)?
                            else:
                                raise _SerialError(_reader.error_unex_char())
                                return False
                        # Unexpected (FAIL)?
                        else:
                            raise _SerialError(_reader.error_unex_char())
                            return False
                    # Next
                    _reader.next()
            else:
                if _reader.chr != '!':
                    raise _SerialError(_reader.error("Exceeded cell count"))
                    return False
            # Success!!!
            return True
        # Begin parsing
        reader = _StringReader(string)
        # Find header
        while True:
            # End of file?
            if reader.eof:
                raise _SerialError(reader.error_unex_end())
            # Whitespace?
            if reader.white:
                reader.next()
                continue
            # Comment?
            if reader.chr == '#':
                reader.skip_line()
                continue
            # Header found!
            break
        # Parse header
        _hdrreader = _StringReader(reader)
        hdrdefs:dict[str, str] = {}
        while True:
            # End of line?
            if reader.eol:
                if not _parsehdrdef(hdrdefs, _hdrreader, reader.pos):
                    raise _tempkill()
                break
            # Comment?
            if reader.chr == '#':
                if not _parsehdrdef(hdrdefs, _hdrreader, reader.pos):
                    raise _tempkill()
                reader.skip_eol()
                break
            # Comma?
            if reader.chr == ',':
                if not _parsehdrdef(hdrdefs, _hdrreader, reader.pos):
                    raise _tempkill()
                _hdrreader.next()
                reader.next()
                continue
            # Next
            reader.next()
        reader.next()
        # Look thru defs
        hdr_x = None
        hdr_y = None
        hdr_rule = None
        for _n, _v in hdrdefs.items():
            match _n:
                case 'x':
                    _r, hdr_x = _parsexy(_v, _n)
                    if not _r: raise _tempkill()
                case 'y':
                    _r, hdr_y = _parsexy(_v, _n)
                    if not _r: raise _tempkill()
                case 'rule':
                    _r, hdr_rule = _parserule(_v, _n)
                    if not _r: raise _tempkill()
        if hdr_x is None:
            raise _SerialError("ERROR: Required parameter x has not been defined.")
        if hdr_y is None:
            raise _SerialError("ERROR: Required parameter y has not been defined.")
        if hdr_rule is None:
            hdrdefs = _LifePatternRule() # type: ignore
        # Init pattern
        pattern = _LifePattern(\
            width = hdr_x,\
            height = hdr_y,\
            rule = hdr_rule) # type: ignore
        # Parse data
        if not _parsedata(pattern, reader):
            raise _tempkill()
        # Success!!!
        return pattern

    @classmethod
    def pattern_to_rle(cls, pattern:_LifePattern):
        """
        Serializes LifePattern data to a str containing RLE data
        
        :param pattern:
            Input LifePattern
        :return:
            Created string
        """
        def _writevalue(
                _strio:_StringIO,\
                _value:bool,\
                _count:int):
            if _count == 0: return
            if _count > 1: _strio.write(str(_count))
            _strio.write('o' if _value else 'b')
        with _StringIO() as strio:
            # Header
            strio.write(f"x = {pattern.width}, y = {pattern.height}, rule = {pattern.rule}\n")
            # Data
            for y in range(pattern.height):
                value = False
                count = 0
                for x in range(pattern.width):
                    if pattern[x, y] == value:
                        count += 1
                    else:
                        _writevalue(strio, value, count)
                        value = not value
                        count = 1
                _writevalue(strio, value, count)
                if (y + 1) < pattern.height:
                    strio.write("$")
            strio.write("!\n")
            # Save
            return strio.getvalue()

    #endregion
    
    #region pattern txt

    @classmethod
    def pattern_from_txt(cls, string:str):
        """
        Deserializes LifePattern data from a str containing plain text data
        
        :param string:
            Input str
        :return:
            Created LifePattern
        :raise SerialError:
            An error occurred during deserialization
        """
        def _iscomment(_chr):
            return _chr == '#' or _chr == '!'
        # Parse
        w = 0
        h = 0
        data = []
        _reader = _StringReader(string)
        while not _reader.eof:
            # Find non-whitespace
            _reader.skip_white()
            if _reader.eof: break
            # Is this a comment?
            if _iscomment(_reader.chr):
                _reader.skip_line()
                continue
            # Parse line
            h += 1
            _row = []
            while not _reader.eol:
                # Is this whitespace?
                if _reader.white:
                    break
                # Is this a comment?
                if _iscomment(_reader.chr):
                    _reader.skip_eol()
                    break
                # Parse
                match _reader.chr:
                    case '.': _row.append(False)
                    case 'O': _row.append(True)
                    case '*': _row.append(True)
                    case _:
                        raise _SerialError(_reader.error_unex_char())
                _reader.next()
            # Ensure rest of line contains only whitespace of comments
            while not _reader.eol:
                if _reader.white:
                    _reader.next()
                    continue
                if _iscomment(_reader.chr):
                    _reader.skip_eol()
                    break
                raise _SerialError(_reader.error_unex_char())
            # Add row
            if w < len(_row):
                w = len(_row)
            data.append(_row)
        # Create pattern
        pattern = _LifePattern(width = w, height = h)
        for _y in range(len(data)):
            _row = data[_y]
            for _x in range(len(_row)):
                pattern[_x, _y] = _row[_x]
        # Success!!!
        return pattern

    @classmethod
    def pattern_to_txt(cls, pattern:_LifePattern):
        """
        Serializes LifePattern data to a str containing plain text data\n
        NOTE: Rule configurations will not be saved
        
        :param pattern:
            Input LifePattern
        :return:
            Created string
        """
        with _StringIO() as strio:
            for y in range(pattern.height):
                for x in range(pattern.width):
                    strio.write('O' if pattern[x, y] else '.')
                strio.write('\n')
            return strio.getvalue()

    #endregion

    #region pattern bin

    @classmethod
    def pattern_from_bin(cls, data:_DataBuffer):
        """
        Deserializes LifePattern data from an DataBuffer
        
        :param data:
            Input DataBuffer
        :return:
            Created LifePattern
        :raise SerialError:
            Unexpected end of data
        """
        try:
            data.set_cursor(0)
            # Read width and height
            width = data.read_uint32_l()
            height = data.read_uint32_l()
            # Create pattern
            pattern = _LifePattern(width = width, height = height)
            _pos = 0
            while _pos < len(pattern) and data.cursor < len(data):
                # Read byte
                _byte = data.read_uint8()
                # Compressed?
                if (_byte & 0b00000001) != 0:
                    _live = (_byte & 0b00000010) != 0
                    _count = _byte >> 2
                    while _pos < len(pattern) and _count > 0:
                        pattern[_pos] = _live
                        _pos += 1
                        _count -= 1
                # Not compressed?
                else:
                    _mask = 0b00000010
                    while _pos < len(pattern) and _mask <= 0b10000000:
                        pattern[_pos] = (_byte & _mask) != 0
                        _pos += 1
                        _mask <<= 1
            # Success!!!
            return pattern
        except _DataError as _e:
            e = _SerialError(_e)
        raise e

    @classmethod
    def pattern_to_bin(cls, pattern:_LifePattern):
        """
        Serializes LifePattern data to an DataBuffer\n
        NOTE: Rule configurations will not be saved
        
        :param pattern:
            Input LifePattern
        :return:
            Created DataBuffer
        :raise SerialError:
            Pattern width is larger than 4294967295\n
            or\n
            Pattern height is larger than 4294967295
        """
        if pattern.width > _U32_MAX:
            raise _SerialError(f"Pattern width must be less than or equal to {_U32_MAX}.")
        if pattern.height > _U32_MAX:
            raise _SerialError(f"Pattern height must be less than or equal to {_U32_MAX}.")
        # Gather cell data
        celldata = bytearray((len(pattern) + 6) // 7)
        cellsize = 0
        _pos = 0
        while _pos < len(pattern):
            # Get first cell in byte
            _first = pattern[_pos]
            _pos += 1
            # Get next 6 cells
            _byte = 0b00000010 if _first else 0b00000000
            _mask = 0b00000100
            _compressable = True
            while _pos < len(pattern) and _mask <= 0b10000000:
                # Get cell
                _cell = pattern[_pos]
                _pos += 1
                # Compare with first
                if _cell != _first: _compressable = False
                # Add to byte
                if _cell: _byte |= _mask
                # Next
                _mask <<= 1
            if _mask <= 0b10000000:
                _compressable = False
            # Compressable?
            if _compressable:
                _count = 7
                while _count < 63 and _pos < len(pattern) and pattern[_pos] == _first:
                    _pos += 1
                    _count += 1
                _byte = ((_byte & 0b00000010) | (0b00000001)) | (_count << 2)
            # Add byte
            celldata[cellsize] = _byte
            cellsize += 1
        # Create buffer
        data = _DataBuffer()
        # Write width and height
        data.write_uint32_l(pattern.width)
        data.write_uint32_l(pattern.height)
        # Write cell data
        for _i in range(cellsize):
            data.write_uint8(celldata[_i])
        # Success!!!
        return data

    #endregion