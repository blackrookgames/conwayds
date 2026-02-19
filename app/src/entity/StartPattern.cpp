#include "entity/StartPattern.h"

#include <algorithm>

using namespace entity;

#pragma region macros

#define VALID_RANGE(x, y, fail) \
    if (x >= PATTERN_WIDTH) fail \
    if (y >= PATTERN_HEIGHT) fail

#pragma endregion

#pragma region init

StartPattern::StartPattern()
{
    f_cells = new bool[PATTERN_AREA];
    std::fill_n(f_cells, PATTERN_AREA, false);
}

StartPattern::~StartPattern()
{
    delete f_cells;
}

#pragma endregion

#pragma region properties

const bool* StartPattern::cells() const { return f_cells; }

bool* StartPattern::cells() { return f_cells; }

#pragma endregion

#pragma region functions

bool StartPattern::cell(u16 x, u16 y) const
{
    VALID_RANGE(x, y, return false;)
    return f_cells[x + y * PATTERN_WIDTH];
}

void StartPattern::cell(u16 x, u16 y, bool alive)
{
    VALID_RANGE(x, y, return;)
    f_cells[x + y * PATTERN_WIDTH] = alive;
}

#pragma endregion