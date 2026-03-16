#include <nds.h>

#include "engine/helper/_macros.h"

#ifndef ENGINE_GFX_TEXTFLAGS_H
#define ENGINE_GFX_TEXTFLAGS_H

namespace engine::gfx
{
    /// @brief Represents flags for printing text
    enum class TextFlags : u16
    {
        /// @brief Default
        Default = 0,
        /// @brief Flip characters horizontally
        Flip_X = 0b01 << 10,
        /// @brief Flip characters vertically
        Flip_Y = 0b10 << 10,
        /// @brief Use palette 0
        Palette_0 = 0x0 << 12,
        /// @brief Use palette 1
        Palette_1 = 0x1 << 12,
        /// @brief Use palette 2
        Palette_2 = 0x2 << 12,
        /// @brief Use palette 3
        Palette_3 = 0x3 << 12,
        /// @brief Use palette 4
        Palette_4 = 0x4 << 12,
        /// @brief Use palette 5
        Palette_5 = 0x5 << 12,
        /// @brief Use palette 6
        Palette_6 = 0x6 << 12,
        /// @brief Use palette 7
        Palette_7 = 0x7 << 12,
        /// @brief Use palette 8
        Palette_8 = 0x8 << 12,
        /// @brief Use palette 9
        Palette_9 = 0x9 << 12,
        /// @brief Use palette 10
        Palette_A = 0xA << 12,
        /// @brief Use palette 11
        Palette_B = 0xB << 12,
        /// @brief Use palette 12
        Palette_C = 0xC << 12,
        /// @brief Use palette 13
        Palette_D = 0xD << 12,
        /// @brief Use palette 14
        Palette_E = 0xE << 12,
        /// @brief Use palette 15
        Palette_F = 0xF << 12,
    };

    ENUMFLAGS_OPS(TextFlags, u16)
}

#endif