__all__ = [ 'StrUtil' ]

class StrUtil:
    """
    Utility for string-related operations
    """

    #region trimpnts

    @classmethod
    def trimpnts(cls, string:str):
        """
        Computes start and end points for trimming whitespace
        
        :param string:
            Input string
        :return:
            Start and end points for trimming whitespace\n
            If start and end points are equal, then the string contains only whitespace.
        """
        # Leading
        beg = 0
        while True:
            if beg == len(string):
                return 0, 0
            if string[beg] > ' ':
                break
            beg += 1
        # Trailing
        end = len(string)
        while string[end - 1] <= ' ':
            end -= 1
        # Return
        return beg, end

    #endregion

    #region find

    @classmethod
    def find(cls, string:str, substr:str):
        """
        Searches the string for a substring

        :param string:
            String to search
        :param substr:
            Substring to search for
        :return:
            Index of the first occurance of the substring (or -1 if substring could not be found)
        """
        for _i in range((len(string) - len(substr)) + 1):
            if string[_i:(_i + len(substr))] == substr: return _i
        return -1

    @classmethod
    def find_last(cls, string:str, substr:str):
        """
        Searches the string backwards for a substring

        :param string:
            String to search
        :param substr:
            Substring to search for
        :return:
            Index of the last occurance of the substring (or -1 if substring could not be found)
        """
        for _i in range(len(string) - len(substr), -1, -1):
            if string[_i:(_i + len(substr))] == substr: return _i
        return -1

    #endregion