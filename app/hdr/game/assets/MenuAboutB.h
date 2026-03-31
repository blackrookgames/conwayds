#include <nds.h>

#ifndef GAME_ASSETS_MENUABOUTB_H
#define GAME_ASSETS_MENUABOUTB_H

namespace game::assets
{
    class MenuAboutB
    {
        public:
        
        static const size_t size;
        static const u16 data[];
        
        static constexpr u16 msg_end = 16;
        
        static constexpr u16 tchbtns_w = 16;
        static constexpr u16 tchbtns_h = 3;
        static constexpr u16 tchbtns_text_x = 1;
        static constexpr u16 tchbtns_text_y = 1;
        static constexpr u16 tchbtns_text_len = 14;
        static constexpr u8 tchbtns_count = 2;
        static const u16 tchbtns_x[];
        static const u16 tchbtns_y[];
        
        static constexpr u16 buttons_w = 16;
        static constexpr u16 buttons_h = 5;
        static constexpr u16 buttons_text_x = 1;
        static constexpr u16 buttons_text_y = 2;
        static constexpr u16 buttons_text_len = 14;
        static constexpr u8 buttons_count = 2;
        static const u16 buttons_x[];
        static const u16 buttons_y[];
    };
}

#endif
