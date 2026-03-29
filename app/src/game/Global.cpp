#include "game/Global.h"

#include <cstdio>
#include <cstring>
#include <iostream>

#include "engine/helper/_macros.h"

using namespace game;

#pragma region fields

engine::data::Pattern Global::f_Pattern;
engine::io::Path Global::f_Pattern_Path = engine::io::Path();

engine::helper::RRValue48p16 Global::f_View_X = engine::helper::RRValue48p16(0, 0);
engine::helper::RRValue48p16 Global::f_View_Y = engine::helper::RRValue48p16(0, 0);
engine::helper::RRValue48p16 Global::f_View_Zoom = engine::helper::RRValue48p16(100, 0);

bool Global::f_SaveEnabled = false;

game::scns::edit::Tool Global::f_Edit_Tool = game::scns::edit::Tool::DRAW;
bool Global::f_Edit_Grid = true;

u16 Global::f_Menu_Main_Index = 0;
u16 Global::f_Menu_Load_Index = 0;

#pragma endregion

#pragma region properties

engine::data::Pattern* Global::pattern() { return &f_Pattern; }

const engine::io::Path& Global::pattern_Path() { return f_Pattern_Path; }
void Global::pattern_Path(const engine::io::Path& value) { f_Pattern_Path = value; }
void Global::pattern_Path(engine::io::Path&& value) { f_Pattern_Path = std::move(value); }

engine::helper::RRValue48p16 Global::view_X() { return f_View_X; }
void Global::view_X(engine::helper::RRValue48p16 value) { f_View_X = value; }

engine::helper::RRValue48p16 Global::view_Y() { return f_View_Y; }
void Global::view_Y(engine::helper::RRValue48p16 value) { f_View_Y = value; }

engine::helper::RRValue48p16 Global::view_Zoom() { return f_View_Zoom; }
void Global::view_Zoom(engine::helper::RRValue48p16 value) { f_View_Zoom = value; }

bool Global::saveEnabled() { return f_SaveEnabled; }
void Global::saveEnabled(bool value) { f_SaveEnabled = value; }

game::scns::edit::Tool Global::edit_Tool() { return f_Edit_Tool; }
void Global::edit_Tool(game::scns::edit::Tool value) { f_Edit_Tool = value; }

bool Global::edit_Grid() { return f_Edit_Grid; }
void Global::edit_Grid(bool value) { f_Edit_Grid = value; }

u16 Global::menu_Main_Index() { return f_Menu_Main_Index; }
void Global::menu_Main_Index(u16 value) { f_Menu_Main_Index = value; }

u16 Global::menu_Load_Index() { return f_Menu_Load_Index; }
void Global::menu_Load_Index(u16 value) { f_Menu_Load_Index = value; }

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