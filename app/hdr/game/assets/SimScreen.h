#include <nds.h>

#ifndef GAME_ASSETS_SIMSCREEN_H
#define GAME_ASSETS_SIMSCREEN_H

namespace game::assets
{
    class SimScreen
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u8 gen_x = 14;
        static constexpr u8 gen_y = 2;
        static constexpr u8 live_x = 14;
        static constexpr u8 live_y = 4;
        static constexpr u8 speed_x0 = 1;
        static constexpr u8 speed_y0 = 8;
        static constexpr u8 speed_x1 = 31;
        static constexpr u8 speed_y1 = 10;
    };
}

#endif
