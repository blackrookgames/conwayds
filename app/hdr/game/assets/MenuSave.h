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
    };
}

#endif
