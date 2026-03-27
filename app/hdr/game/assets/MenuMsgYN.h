#include <nds.h>

#ifndef GAME_ASSETS_MENUMSGYN_H
#define GAME_ASSETS_MENUMSGYN_H

namespace game::assets
{
    class MenuMsgYN
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u16 msg_x = 2;
        static constexpr u16 msg_y = 2;
        static constexpr u16 msg_w = 28;
        static constexpr u16 msg_h = 12;
        
        static constexpr u16 button_x = 2;
        static constexpr u16 button_y = 15;
        static constexpr u16 button_w = 14;
        static constexpr u16 button_h = 7;
        static constexpr u16 buttons = 2;
        static constexpr u16 columns = 2;
    };
}

#endif
