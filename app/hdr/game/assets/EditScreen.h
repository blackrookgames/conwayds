#include <nds.h>

#ifndef GAME_ASSETS_EDITSCREEN_H
#define GAME_ASSETS_EDITSCREEN_H

namespace game::assets
{
    class EditScreen
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u8 coord_x = 1;
        static constexpr u8 coord_y = 23;
        static constexpr u8 coord_len = 15 - coord_x;
        static constexpr u8 tool_x = 31;
        static constexpr u8 tool_y = 23;
        static constexpr u8 live_x = 14;
        static constexpr u8 live_y = 2;
    };
}

#endif
