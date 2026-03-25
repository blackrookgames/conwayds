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
        
        static constexpr u8 coordx_x = 4;
        static constexpr u8 coordx_y = 20;
        static constexpr u8 coordy_x = 4;
        static constexpr u8 coordy_y = 21;
        static constexpr u8 zoom_x = 4;
        static constexpr u8 zoom_y = 22;
        static constexpr u8 tool_x = 31;
        static constexpr u8 tool_y = 23;
        static constexpr u8 live_x = 14;
        static constexpr u8 live_y = 2;
    };
}

#endif
