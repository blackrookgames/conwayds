#include <nds.h>

#include "engine/data/Pattern.h"
#include "engine/helper/_macros.h"

#ifndef GAME_SCNS_EDIT_TOOL_H
#define GAME_SCNS_EDIT_TOOL_H

namespace game::scns::edit
{
    /// @brief Represents a tool type
    enum class Tool { DRAW, ERASE, };

    /// @brief Number of tool types
    constexpr u8 toolCount = 2;
}

#endif