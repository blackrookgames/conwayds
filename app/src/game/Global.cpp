#include "game/Global.h"

#include <cstdio>
#include <cstring>
#include <iostream>

#include "engine/helper/_macros.h"

using namespace game;

#pragma region fields

engine::data::Pattern Global::f_Pattern;

#pragma endregion

#pragma region properties

engine::data::Pattern* Global::pattern() { return &f_Pattern; }

#pragma endregion

#pragma region functions

void Global::pattern_From(const engine::data::Pattern& input)
{
    std::copy(input.cells(), input.cells() + PATTERN_AREA, f_Pattern.cells());
}

void Global::pattern_To(engine::data::Pattern& output)
{
    std::copy(f_Pattern.cells(), f_Pattern.cells() + PATTERN_AREA, output.cells());
}

#pragma endregion