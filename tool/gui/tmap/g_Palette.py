__all__ = [\
    'PALETTE_SUBCOUNT',\
    'Palette',]

from .g_PaletteSub import\
    PaletteSub as _PaletteSub

#region helper const

_DEF_PALETTE = [\
    [ "#941C25", "#AF1F28", "#CD212A", "#E23029", "#EB4D26", "#EF7425", "#F29F25", "#F4C123", "#F7D826", "#E8DC32", "#C3D242", "#9CC54B", "#6FB651", "#39A85F", "#0DA081", "#099BC0",],\
    [ "#A11E27", "#BE202A", "#D8212A", "#E73C28", "#ED6126", "#F18824", "#F3B123", "#F4CF25", "#F2DB2A", "#D5D739", "#AECC47", "#83BD4E", "#52AF58", "#22A573", "#0C9D9D", "#1181B2",],\
    [ "#AE2028", "#CC202B", "#E1232A", "#EB4827", "#EF7426", "#F29B24", "#F4C122", "#F3DB27", "#EADD2E", "#C2D241", "#98C54C", "#6AB552", "#35A862", "#0DA188", "#0C97B5", "#1967A4",],\
    [ "#B82029", "#D42129", "#E53228", "#ED5926", "#F18525", "#F3AB23", "#F2CA24", "#EADB2F", "#D4D73A", "#ABC947", "#7CBB4E", "#48AC5A", "#1EA479", "#0C9BA2", "#107FAE", "#1F5091",],\
    [ "#C3202A", "#DB2228", "#E84126", "#EE6925", "#F29525", "#F4BA24", "#EFD128", "#DFD937", "#BCCF44", "#91C04C", "#5DB152", "#29A466", "#0D9F8F", "#0D91B4", "#1568A5", "#253C82",],\
    [ "#CD1F2A", "#DF2627", "#E94D26", "#EF7B26", "#F3A625", "#F2C626", "#E8D72F", "#C9D240", "#A2C54A", "#73B54E", "#3BA85C", "#17A280", "#0C99A5", "#117FB0", "#1C5696", "#2E367C",],\
    [ "#D71F2A", "#E33026", "#EA5D26", "#F18D26", "#F3B625", "#EFD129", "#DDD837", "#B3CC48", "#89BD4D", "#54AC53", "#20A36D", "#0B9F98", "#0D90B3", "#156EAA", "#24478B", "#3C337B",],\
    [ "#E01E29", "#E74225", "#EE7425", "#F2A125", "#F4C526", "#E9D82F", "#C9D240", "#9EC54C", "#74B74E", "#33A75F", "#12A38B", "#0A9AAD", "#0F82B2", "#1C5F9F", "#2F3E86", "#533683",],\
    [ "#E62327", "#EB5525", "#F18825", "#F3B326", "#EFD02B", "#DBD838", "#B4CB48", "#83BD4F", "#54B055", "#1CA474", "#0B9FA2", "#0C8EB6", "#1470AA", "#225093", "#3A3982", "#653888",],\
    [ "#E72E26", "#EE6A26", "#F29824", "#F4C427", "#E5D732", "#C6D143", "#9DC44E", "#62B252", "#28A761", "#10A393", "#0B97B2", "#117DB1", "#1B5B9B", "#294187", "#433781", "#72398B",],\
    [ "#EA4026", "#F07E27", "#F2AA24", "#EDCD2C", "#D6D63B", "#B1CB49", "#82BC52", "#40AA5A", "#14A47A", "#0BA0A8", "#0E89B4", "#1769A5", "#244C8F", "#373A83", "#543684", "#81388C",],\
    [ "#ED5728", "#F29226", "#F3BC23", "#E3D333", "#C4D244", "#9BC44C", "#64B554", "#1EA466", "#0EA59B", "#099AB9", "#1277AE", "#1D5596", "#2E4085", "#493884", "#693788", "#90368C",],\
    [ "#EE6728", "#F2A225", "#EFC927", "#D5D439", "#ADCB48", "#7ABA51", "#3FAD60", "#11A280", "#0C9EAD", "#0E88B5", "#1865A1", "#24478A", "#383981", "#583785", "#7A3689", "#A0358A",],\
    [ "#EF7427", "#F3B024", "#EBD42C", "#C6D33F", "#93C24C", "#55B055", "#17A46F", "#0DA19F", "#0B94BB", "#1472AA", "#1F5192", "#2B3B80", "#43357D", "#663586", "#8A3488", "#B13388",],\
    [ "#F18C25", "#F3C223", "#DED534", "#B2CD45", "#7EBA4F", "#43A657", "#0F9570", "#0C92A4", "#1180B1", "#1B5E9B", "#264385", "#39377E", "#573481", "#7A3486", "#9D3488", "#C83887",],\
    [ "#F4A522", "#F4D522", "#D1D53C", "#9EC64B", "#69B352", "#359C59", "#0C846E", "#0D81A5", "#186AA3", "#224A8C", "#2D3679", "#48337C", "#6C3585", "#8E3287", "#B13389", "#DF3D86",],]

#endregion

#region const

PALETTE_SUBCOUNT = 16
"""
Number of sub-palettes within a palette
"""

#endregion

class Palette:
    """
    Represents a palette
    """

    #region init

    def __init__(self):
        """
        Initializer for Palette
        """
        self.__data:list[_PaletteSub] = []
        for _i in range(PALETTE_SUBCOUNT):
            _sub = _PaletteSub()
            _def = _DEF_PALETTE[_i]
            for _j in range(len(_sub)):
                _sub[_j] = _def[_j]
            self.__data.append(_sub)

    #endregion

    #region operators

    def __len__(self):
        return PALETTE_SUBCOUNT

    def __getitem__(self, index:int):
        """
        Gets the sub-palette at the specified index

        :param index:
            Index of sub-palette
        :returns:
            Sub-palette at the specified index
        :raise IndexError:
            Index is out of range
        """
        try:
            return self.__data[index]
        except Exception as _e:
            if index < 0 or index >= PALETTE_SUBCOUNT:
                e = IndexError("Index is out of range.")
            else: e = _e
        raise e

    #endregion