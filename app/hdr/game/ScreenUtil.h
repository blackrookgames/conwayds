#include <nds.h>

#ifndef GAME_SCREENUTIL_H
#define GAME_SCREENUTIL_H

namespace game
{
    /// @brief Utility for screen-related operations
    class ScreenUtil
    {
        public:

        /// @brief Loads RLE-compressed screen data
        /// @param in_data Input data
        /// @param in_len Size of input data
        /// @param out_data Output data
        /// @param out_len Size of output data
        static void load(const u16* in_data, size_t in_len, u16*& out_data, size_t& out_len);
    };
}

#endif
