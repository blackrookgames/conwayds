#include <nds.h>

#ifndef GAME_ASSETS_MENUMSGOK_H
#define GAME_ASSETS_MENUMSGOK_H

namespace game::assets
{
    class MenuMsgOK
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u16 msg_x = 2;
        static constexpr u16 msg_y = 2;
        static constexpr u16 msg_w = 28;
        static constexpr u16 msg_h = 12;
        
        static constexpr u16 button_x = 8;
        static constexpr u16 button_y = 15;
        static constexpr u16 button_w = 16;
        static constexpr u16 button_h = 7;
        static constexpr u16 buttons = 1;
        static constexpr u16 columns = 1;
    };
}

#endif
