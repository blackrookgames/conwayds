#include "game/scns/edit/Editor.h"

#include <cstdio>
#include <cstring>

#include <__.h>
#include "engine/helper/ArrayUtil.h"
#include "game/Global.h"
#include "game/assets/Palette.h"
#include "game/assets/SimTileset.h"

using namespace game::scns::edit;

#pragma region macros

#define ROUGHSECOND 32768

#define BG_WIDTH 1024
#define BG_HEIGHT 1024
#define BG_TILE_COLS (BG_WIDTH / 8)
#define BG_TILE_ROWS (BG_HEIGHT / 8)
#define BG_TILE_COUNT (BG_TILE_COLS * BG_TILE_ROWS)

#define SAND_TILE_COLS (PATTERN_WIDTH / 2)
#define SAND_TILE_ROWS (PATTERN_HEIGHT / 2)
#define SAND_TILE_COUNT (SAND_TILE_COLS * SAND_TILE_ROWS)
#define SAND_WIDTH (SAND_TILE_COLS * 8)
#define SAND_HEIGHT (SAND_TILE_ROWS * 8)

#define VIEW_W_MIN 64
#define VIEW_W_MAX SAND_WIDTH
#define VIEW_ZOOM_MIN 0
#define VIEW_ZOOM_MAX (VIEW_W_MAX - VIEW_W_MIN)
#define VIEW_ZOOM_GRID 832

#define GEN_LENGTH(speed) ((ROUGHSECOND * 4) / speed)

#pragma endregion

#pragma region init

Editor::Editor(int layer, int mapBase, int tileBase, unsigned int priority)
{
    // Dirty
    f_IsDirty = true;
    // Background
    f_BG = bgInitSub(layer, BgType_Rotation, BgSize_R_1024x1024, mapBase, tileBase);
	f_BG_GFX = bgGetGfxPtr(f_BG);
    f_BG_Map = bgGetMapPtr(f_BG);
    f_BG_Buffer_A = new u8[BG_TILE_COUNT];
    f_BG_Buffer_B = new u8[BG_TILE_COUNT];
    f_BG_Buffer_Ptr = f_BG_Buffer_A;
    bgSetPriority(f_BG, priority);
    // View
    f_View = new engine::view::View(f_BG, bound_X0, bound_Y1);
    // Pattern
    game::Global::pattern_To(f_Pattern);
    // Grid
    f_Grid = true;
    // Post-init
    m_Refresh_Buffer_Ptr();
    m_Force_NumLive();
    m_Force_Buffer();
}

Editor::~Editor()
{
    // View
    delete f_View;
    // Background
    delete[] f_BG_Buffer_B;
    delete[] f_BG_Buffer_A;
}

#pragma endregion

#pragma region helper const

const engine::helper::RRValue48p16 Editor::f_Zoom_Grid = engine::helper::RRValue48p16(75, 0);

#pragma endregion

#pragma region const

const engine::helper::RRValue48p16 Editor::bound_X0 = engine::helper::RRValue48p16(-508, 0);
const engine::helper::RRValue48p16 Editor::bound_Y0 = engine::helper::RRValue48p16(-508, 0); // Remember, a pattern has 254 columns
const engine::helper::RRValue48p16 Editor::bound_X1 = engine::helper::RRValue48p16(508, 0); // Remember, a pattern has 254 rows
const engine::helper::RRValue48p16 Editor::bound_Y1 = engine::helper::RRValue48p16(508, 0);

#pragma endregion

#pragma region properties

const u16* Editor::bg_GFX() const { return f_BG_GFX; }
u16* Editor::bg_GFX() { return f_BG_GFX; }

const u16* Editor::bg_Map() const { return f_BG_Map; }
u16* Editor::bg_Map() { return f_BG_Map; }

const engine::view::View& Editor::view() const { return *f_View; }

engine::helper::RRValue48p16 Editor::view_Zoom() const { return f_View->cam_Zoom(); }
void Editor::view_Zoom(engine::helper::RRValue48p16 value)
{
    if (f_View->cam_Zoom() == value) return;
    f_View->cam_Zoom(value);
    m_Refresh_Buffer_Ptr();
}

engine::helper::RRValue48p16 Editor::view_X() const  { return f_View->cam_X(); }
void Editor::view_X(engine::helper::RRValue48p16 value) { f_View->cam_X(value); }

engine::helper::RRValue48p16 Editor::view_Y() const { return f_View->cam_Y(); }
void Editor::view_Y(engine::helper::RRValue48p16 value) { f_View->cam_Y(value); }

bool Editor::grid() const { return f_Grid; }
void Editor::grid(bool value)
{
    if (f_Grid == value) return;
    f_Grid = value;
    m_Refresh_Buffer_Ptr();
}

u32 Editor::numLive() const { return f_NumLive; }

#pragma endregion

#pragma region helper functions

void Editor::m_Refresh_Buffer_Ptr()
{
    u8* prev = f_BG_Buffer_Ptr;
    f_BG_Buffer_Ptr = (f_Grid && f_View->cam_Zoom() >= f_Zoom_Grid) ? f_BG_Buffer_B : f_BG_Buffer_A;
    if (f_BG_Buffer_Ptr != prev) markDirty();
}

void Editor::m_Force_NumLive()
{
    f_NumLive = 0;
    const bool* ptr = f_Pattern.cells();
    const bool* end = ptr + PATTERN_AREA;
    while (ptr < end) { if (*(ptr++)) ++f_NumLive; }
}

void Editor::m_Force_Buffer()
{
    // Clear
    std::fill(f_BG_Buffer_A, f_BG_Buffer_A + BG_TILE_COUNT, 0x10);
    std::fill(f_BG_Buffer_B, f_BG_Buffer_B + BG_TILE_COUNT, 0x20);
    // Plot rows
    bool* iptr = f_Pattern.cells();
    u8* optr0 = f_BG_Buffer_A;
    u8* optr1 = f_BG_Buffer_B;
    for (u16 iy = 0; iy < PATTERN_HEIGHT; iy += 2)
    {
        for (u16 ix = 0; ix < PATTERN_WIDTH; ix += 2)
        {
            if (*iptr) *optr0 |= 0b0001;
            if (iptr[1]) *optr0 |= 0b0010;
            if (iptr[PATTERN_WIDTH]) *optr0 |= 0b0100;
            if (iptr[PATTERN_WIDTH + 1]) *optr0 |= 0b1000;
            *optr1 |= *optr0 & 0x0F;
            iptr += 2; ++optr0; ++optr1;
        }
        iptr += PATTERN_WIDTH;
        *(optr0++) = 0x00;
        *(optr1++) = 0x00;
    }
    // Draw bottom border
    std::fill(f_BG_Buffer_A + BG_TILE_COUNT - BG_TILE_COLS, f_BG_Buffer_A + BG_TILE_COUNT, 0x00);
    std::fill(f_BG_Buffer_B + BG_TILE_COUNT - BG_TILE_COLS, f_BG_Buffer_B + BG_TILE_COUNT, 0x00);
    // Mark dirty
    markDirty();
}

#pragma endregion

#pragma region functions

void Editor::markDirty()
{
    f_IsDirty = true;
}

void Editor::vblank()
{
    // Always call view
    f_View->vblank();
    // Update dirty
    if (!f_IsDirty) return;
    f_IsDirty = false;
    // Update background
    DC_FlushRange(f_BG_Buffer_Ptr, BG_TILE_COUNT);
    dmaCopy(f_BG_Buffer_Ptr, f_BG_Map, BG_TILE_COUNT);
}

void Editor::savePattern()
{
    Global::pattern_From(f_Pattern);
}

bool Editor::getcell(u16 x, u16 y) const
{
    return f_Pattern.getcell(x, y);
}

void Editor::setcell(u16 x, u16 y, bool live)
{
    if (x >= PATTERN_WIDTH || y >= PATTERN_HEIGHT) return;
    // Update pattern
    bool prev = f_Pattern.getcell(x, y);
    f_Pattern.setcell(x, y, live);
    // Update buffer
    size_t index = (x / 2) + (y / 2) * BG_TILE_COLS;
    u8 mask = 1 << ((x % 2) + (y % 2) * 2);
    u8* ptrA = f_BG_Buffer_A + index;
    u8* ptrB = f_BG_Buffer_B + index;
    if (!live) { *ptrA ^= 0xFF; *ptrB ^= 0xFF; }
    *ptrA |= mask; *ptrB |= mask;
    if (!live) { *ptrA ^= 0xFF; *ptrB ^= 0xFF; }
    // Update number of live cells
    if (live != prev) { if (live) ++f_NumLive; else --f_NumLive; }
    // Mark dirty
    markDirty();
}

#pragma endregion