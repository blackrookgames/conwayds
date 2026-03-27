#include <nds.h>

#ifndef GAME_ASSETS_MENURANDOM_H
#define GAME_ASSETS_MENURANDOM_H

namespace game::assets
{
    class MenuRandom
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u16 seed_x = 15;
        static constexpr u16 seed_y = 2;
        static constexpr u16 seed_len = 8;
        
        static constexpr u16 buttons = 19;
        static const u16 buttons_l[];
        static const u16 buttons_r[];
        static const u16 buttons_u[];
        static const u16 buttons_d[];
        static const u16 buttons_x[];
        static const u16 buttons_y[];
        static const u16 buttons_w[];
        static const u16 buttons_h[];
        
        static const u16 buttons_x0[];
        static const u16 buttons_y0[];
        static const u16 buttons_x1[];
        static const u16 buttons_y1[];
    };
}

#endif
