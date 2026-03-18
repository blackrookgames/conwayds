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
    f_View_Zoom = 896;
    f_View_X = SAND_WIDTH / 2;
    f_View_Y = SAND_HEIGHT / 2;
    // Pattern
    game::Global::pattern_To(f_Pattern);
    f_Pattern.load_file("nitro:/samples/sample0.bin"); // TODO: Remove
    // Grid
    f_Grid = true;
    // Post-init
    m_Refresh_View();
    m_Refresh_Buffer_Ptr();
    m_Redraw_Buffer();
}

Editor::~Editor()
{
    // Buffer
    delete[] f_BG_Buffer_B;
    delete[] f_BG_Buffer_A;
}

#pragma endregion

#pragma region properties

const u16* Editor::bg_GFX() const { return f_BG_GFX; }
u16* Editor::bg_GFX() { return f_BG_GFX; }

const u16* Editor::bg_Map() const { return f_BG_Map; }
u16* Editor::bg_Map() { return f_BG_Map; }

s32 Editor::view_Zoom() const { return f_View_Zoom; }
void Editor::view_Zoom(s32 value)
{
    if (f_View_Zoom == value) return;
    f_View_Zoom = value;
    m_Refresh_View();
}

s32 Editor::view_W() const { return f_View_W; }

s32 Editor::view_H() const { return f_View_H; }

s32 Editor::view_Max_X() const { return f_View_Max_X; }

s32 Editor::view_Max_Y() const { return f_View_Max_Y; }

s32 Editor::view_X() const  { return f_View_X; }
void Editor::view_X(s32 value)
{
    if (f_View_X == value) return;
    f_View_X = value;
    m_Refresh_View();
}

s32 Editor::view_Y() const { return f_View_Y; }
void Editor::view_Y(s32 value)
{
    if (f_View_Y == value) return;
    f_View_Y = value;
    m_Refresh_View();
}

bool Editor::grid() const { return f_Grid; }
void Editor::grid(bool value)
{
    if (f_Grid == value) return;
    f_Grid = value;
    m_Refresh_Buffer_Ptr();
}

#pragma endregion

#pragma region helper functions

void Editor::m_Refresh_View()
{
    // Clamp zoom value
    if (f_View_Zoom < VIEW_ZOOM_MIN) f_View_Zoom = VIEW_ZOOM_MIN;
    if (f_View_Zoom > VIEW_ZOOM_MAX) f_View_Zoom = VIEW_ZOOM_MAX;
    // Compute size
    f_View_W = SAND_WIDTH - f_View_Zoom;
    f_View_H = (f_View_W * DS_SCREEN_HEIGHT + DS_SCREEN_WIDTH - 1) / DS_SCREEN_WIDTH;
    // Compute min/max
    f_View_Min_X = f_View_W / 2;
    f_View_Min_Y = f_View_H / 2;
    f_View_Max_X = SAND_WIDTH - f_View_Min_X;
    f_View_Max_Y = SAND_HEIGHT - f_View_Min_Y;
    // Update background
    bgSetScale(f_BG, f_View_W, f_View_W); // f_View_W is the scale for both axes
    // Clamp X
    if (f_View_X < f_View_Min_X) f_View_X = f_View_Min_X;
    if (f_View_X > f_View_Max_X) f_View_X = f_View_Max_X;
    // Clamp Y
    if (f_View_Y < f_View_Min_Y) f_View_Y = f_View_Min_Y;
    if (f_View_Y > f_View_Max_Y) f_View_Y = f_View_Max_Y;
    // Update background
    bgSetScroll(f_BG, f_View_X - f_View_W / 2, f_View_Y - f_View_H / 2);
    // Update map pointer
    m_Refresh_Buffer_Ptr();
}

void Editor::m_Refresh_Buffer_Ptr()
{
    u8* prev = f_BG_Buffer_Ptr;
    f_BG_Buffer_Ptr = (f_Grid && f_View_Zoom < VIEW_ZOOM_GRID) ? f_BG_Buffer_A : f_BG_Buffer_B;
    if (f_BG_Buffer_Ptr != prev) markDirty();
}

void Editor::m_Redraw_Buffer()
{
    // Clear
    std::fill(f_BG_Buffer_A, f_BG_Buffer_A + BG_TILE_COUNT, 0x00);
    std::fill(f_BG_Buffer_B, f_BG_Buffer_B + BG_TILE_COUNT, 0x10);
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
            *optr1 |= *optr0;
            iptr += 2; ++optr0; ++optr1;
        }
        iptr += PATTERN_WIDTH;
        optr0 += (BG_TILE_COLS - SAND_TILE_COLS);
        optr1 += (BG_TILE_COLS - SAND_TILE_COLS);
    }
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

#pragma endregion