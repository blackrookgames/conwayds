#include "StartPattern.h"

#include <algorithm>

#pragma region macros

#define VALID_RANGE(x, y, fail) \
    if (x >= PATTERN_WIDTH) fail \
    if (y >= PATTERN_HEIGHT) fail

#pragma endregion

#pragma region init

StartPattern::StartPattern(u8 fgColor, u8 bgColor)
{
    f_fgColor = fgColor;
    f_bgColor = (fgColor != bgColor) ? bgColor : (~bgColor);
    f_cells = new u8[PATTERN_AREA];
    std::fill_n(f_cells, PATTERN_AREA, f_bgColor);
}

StartPattern::~StartPattern()
{
    delete f_cells;
}

#pragma endregion

#pragma region functions

bool StartPattern::cell(u16 x, u16 y) const
{
    VALID_RANGE(x, y, return false;)
    return f_cells[x + y * PATTERN_WIDTH] == f_fgColor;
}

void StartPattern::cell(u16 x, u16 y, bool alive)
{
    VALID_RANGE(x, y, return;)
    f_cells[x + y * PATTERN_WIDTH] = alive ? f_fgColor : f_bgColor;
}

void StartPattern::draw(void* gfxptr) const
{
	DC_FlushRange(f_cells, PATTERN_AREA);
	dmaCopy(f_cells, gfxptr, PATTERN_AREA);
}

#pragma endregion