#include <nds.h>

#ifndef GAME_ASSETS_MENUMANAGE_H
#define GAME_ASSETS_MENUMANAGE_H

namespace game::assets
{
    class MenuManage
    {
        public:
        
        struct Region { u16 x; u16 y; u16 w; u16 h; u16 x0; u16 y0; u16 x1; u16 y1; };
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u16 list_x = 3;
        static constexpr u16 list_y = 3;
        static constexpr u16 list_w = 23;
        static constexpr u16 list_h = 13;
        static constexpr u16 list_u_x = 26;
        static constexpr u16 list_u_y = 3;
        static constexpr u16 list_d_x = 26;
        static constexpr u16 list_d_y = 15;
        
        static constexpr u16 buttons_count = 4;
        static constexpr u16 buttons_touch = 2;
        static const Region buttons[];
    };
}

#endif
