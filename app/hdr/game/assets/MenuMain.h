#include <nds.h>

#ifndef GAME_ASSETS_MENUMAIN_H
#define GAME_ASSETS_MENUMAIN_H

namespace game::assets
{
    class MenuMain
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u8 button_x = 1;
        static constexpr u8 button_y = 1;
        static constexpr u8 button_w = 15;
        static constexpr u8 button_h = 7;
    };
}

#endif
