#include <nds.h>

#ifndef GAME_ASSETS_MENUABOUTT_H
#define GAME_ASSETS_MENUABOUTT_H

namespace game::assets
{
    class MenuAboutT
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u16 title_x = 1;
        static constexpr u16 title_y = 1;
        static constexpr u16 title_len = 30;
        static constexpr u16 msg_beg = 3;
    };
}

#endif
