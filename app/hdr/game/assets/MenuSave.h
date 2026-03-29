#include <nds.h>

#ifndef GAME_ASSETS_MENUSAVE_H
#define GAME_ASSETS_MENUSAVE_H

namespace game::assets
{
    class MenuSave
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u16 field_x = 3;
        static constexpr u16 field_y = 3;
        static constexpr u16 field_len = 26;
        static constexpr u16 caps_x = 2;
        static constexpr u16 caps_y = 5;
        static constexpr u16 caps_len = 4;
        static constexpr u16 shift_x = 25;
        static constexpr u16 shift_y = 5;
        static constexpr u16 shift_len = 5;
        
        static constexpr u16 button_w = 14;
        static constexpr u16 button_h = 5;
        static constexpr u16 button_ok_x = 2;
        static constexpr u16 button_ok_y = 17;
        static constexpr u16 button_cancel_x = 16;
        static constexpr u16 button_cancel_y = 17;
        static constexpr u16 keyboard_x = 2;
        static constexpr u16 keyboard_y = 6;
        static constexpr u16 keyboard_w = 27;
        static constexpr u16 keyboard_h = 11;
        static constexpr u16 keyboard_x0 = 2 * 8 + 4;
        static constexpr u16 keyboard_y0 = 6 * 8 + 4;
        static constexpr u16 keyboard_x1 = 29 * 8 - 4;
        static constexpr u16 keyboard_y1 = 17 * 8 - 4;
        static constexpr u16 keyboard_cell_w = 16;
        static constexpr u16 keyboard_cell_h = 16;
        static constexpr u16 keyboard_cell_tile_w = 2;
        static constexpr u16 keyboard_cell_tile_h = 2;

        static const u8 keygrid[];
        static constexpr u16 keygrid_x = 3;
        static constexpr u16 keygrid_y = 7;
        static constexpr u16 keygrid_cols = 13;
        static constexpr u16 keygrid_rows = 5;
        static constexpr u16 keygrid_size = keygrid_cols * keygrid_rows;
        static constexpr u16 keygrid_split = 7;
    };
}

#endif
