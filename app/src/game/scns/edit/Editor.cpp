#include "game/scns/edit/Editor.h"

#include <cstdio>
#include <cstring>

#include <__.h>
#include "engine/data/Pattern.h"
#include "engine/helper/ArrayUtil.h"
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

#define VIEW_W_MIN 64
#define VIEW_W_MAX BG_WIDTH
#define VIEW_ZOOM_MIN 0
#define VIEW_ZOOM_MAX (VIEW_W_MAX - VIEW_W_MIN)

#define GEN_LENGTH(speed) ((ROUGHSECOND * 4) / speed)

#pragma endregion

#pragma region helper functions

namespace game::scns::edit
{
    void map_InitEmpty(u8* output)
    {
        u8* optr = output;
        // Top
        *(optr++) = 0x10;
        for (u16 x = 2; x < BG_TILE_COLS; ++x) *(optr++) = 0x70;
        *(optr++) = 0x20;
        // Top
        for (u16 y = 2; y < BG_TILE_ROWS; ++y)
        {
            *(optr++) = 0x50;
            for (u16 x = 2; x < BG_TILE_COLS; ++x) *(optr++) = 0x00;
            *(optr++) = 0x60;
        }
        // Bottom
        *(optr++) = 0x30;
        for (u16 x = 2; x < BG_TILE_COLS; ++x) *(optr++) = 0x80;
        *(optr++) = 0x40;
    }

    void map_Load(const char* path, const u8* empty, u8* output)
    {
        // Open pattern
        engine::data::Pattern pattern;
        pattern.load_file(path);
        // Clear first row
        std::copy(empty, empty + BG_TILE_COLS, output);
        // Clear first column
        engine::helper::ArrayUtil::copy(empty, empty + BG_TILE_COUNT, output, BG_TILE_COLS);
        // Plot rows
        u8* optr = output;
        for (u16 iy = 0; iy < PATTERN_HEIGHT; iy += 2)
        {
            for (u16 ix = 0; ix < PATTERN_WIDTH; ix += 2)
            {
                if (pattern.getcell(ix, iy)) *optr |= 0b1000;
                if (pattern.getcell(ix + 1, iy)) optr[1] |= 0b0100;
                if (pattern.getcell(ix, iy + 1)) optr[BG_TILE_COLS] |= 0b0010;
                optr[BG_TILE_COLS + 1] = pattern.getcell(ix + 1, iy + 1) ? 0b0001 : 0b0000;
                ++optr;
            }
            ++optr;
        }
    }
}

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
    bgSetPriority(f_BG, priority);
    // View
    f_View_Zoom = 896;
    f_View_X = BG_WIDTH / 2;
    f_View_Y = BG_HEIGHT / 2;
    m_View_FixSize();
    // Map
    f_Map_Empty = new u8[BG_TILE_COUNT];
    f_Map_A = new u8[BG_TILE_COUNT];
    f_Map_B = new u8[BG_TILE_COUNT];
    f_Map_Ptr = f_Map_A;
    map_InitEmpty(f_Map_Empty);
    map_Load("nitro:/samples/sample0.bin", f_Map_Empty, f_Map_Ptr);
}

Editor::~Editor()
{
    // Map
    delete[] f_Map_B;
    delete[] f_Map_A;
    delete[] f_Map_Empty;
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
    f_View_Zoom = value;
    m_View_FixSize();
}

s32 Editor::view_W() const { return f_View_W; }

s32 Editor::view_H() const { return f_View_H; }

s32 Editor::view_Max_X() const { return f_View_Max_X; }

s32 Editor::view_Max_Y() const { return f_View_Max_Y; }

s32 Editor::view_X() const  { return f_View_X; }
void Editor::view_X(s32 value)
{
    f_View_X = value;
    m_View_FixPosition();
}

s32 Editor::view_Y() const { return f_View_Y; }
void Editor::view_Y(s32 value)
{
    f_View_Y = value;
    m_View_FixPosition();
}

#pragma endregion

#pragma region helper functions

void Editor::m_View_FixSize()
{
    // Clamp zoom value
    if (f_View_Zoom < VIEW_ZOOM_MIN)
        f_View_Zoom = VIEW_ZOOM_MIN;
    if (f_View_Zoom > VIEW_ZOOM_MAX)
        f_View_Zoom = VIEW_ZOOM_MAX;
    // Compute size
    f_View_W = BG_WIDTH - f_View_Zoom;
    f_View_H = (f_View_W * DS_SCREEN_HEIGHT + DS_SCREEN_WIDTH - 1) / DS_SCREEN_WIDTH;
    // Compute min/max
    f_View_Min_X = f_View_W / 2;
    f_View_Min_Y = f_View_H / 2;
    f_View_Max_X = BG_WIDTH - f_View_Min_X;
    f_View_Max_Y = BG_HEIGHT - f_View_Min_Y;
    // Update background
    bgSetScale(f_BG, f_View_W, f_View_W); // f_View_W is the scale for both axes
    // Fix position
    m_View_FixPosition();
}

void Editor::m_View_FixPosition()
{
    // Clamp X
    if (f_View_X < f_View_Min_X)
        f_View_X = f_View_Min_X;
    if (f_View_X > f_View_Max_X)
        f_View_X = f_View_Max_X;
    // Clamp Y
    if (f_View_Y < f_View_Min_Y)
        f_View_Y = f_View_Min_Y;
    if (f_View_Y > f_View_Max_Y)
        f_View_Y = f_View_Max_Y;
    // Update background
    bgSetScroll(f_BG, f_View_X - f_View_W / 2, f_View_Y - f_View_H / 2);
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
    DC_FlushRange(f_Map_Ptr, BG_TILE_COUNT);
    dmaCopy(f_Map_Ptr, f_BG_Map, BG_TILE_COUNT);
}

#pragma endregion