#include "game/scns/sim/Simulation.h"

#include <cstdio>
#include <cstring>

#include <__.h>
#include "engine/data/Pattern.h"
#include "engine/helper/ArrayUtil.h"
#include "game/assets/Palette.h"
#include "game/assets/SimTileset.h"

using namespace game::scns::sim;

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

namespace game::scns::sim
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
        const u8* eptr = empty;
        for (u16 iy = 0; iy < PATTERN_HEIGHT; iy += 2)
        {
            for (u16 ix = 0; ix < PATTERN_WIDTH; ix += 2)
            {
                // Top-left
                if (pattern.getcell(ix, iy)) *optr |= 0b1000;
                // Top-right
                if (pattern.getcell(ix + 1, iy)) optr[1] |= 0b0100;
                // Bottom-left
                if (pattern.getcell(ix, iy + 1)) optr[BG_TILE_COLS] |= 0b0010;
                // Bottom-right
                optr[BG_TILE_COLS + 1] = eptr[BG_TILE_COLS + 1];
                if (pattern.getcell(ix + 1, iy + 1)) optr[BG_TILE_COLS + 1] |= 0b0001;
                // Next
                ++optr; ++eptr;
            }
            ++optr; ++eptr;
        }
    }
}

#pragma endregion

#pragma region init

Simulation::Simulation(int layer, int mapBase, int tileBase, unsigned int priority)
{
    // Dirty
    f_IsDirty = true;
    // Background
    f_BG = bgInit(layer, BgType_Rotation, BgSize_R_1024x1024, mapBase, tileBase);
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
    // Cycle
    f_Speed = 16;
    f_Gen_Length = GEN_LENGTH(f_Speed);
    f_Gen_Progress = 0;
    // Simulation details
    f_Sim_Live = 0;
    f_Sim_Gen = 0;
}

Simulation::~Simulation()
{
    // Map
    delete[] f_Map_B;
    delete[] f_Map_A;
    delete[] f_Map_Empty;
}

#pragma endregion

#pragma region properties

const u16* Simulation::bg_GFX() const { return f_BG_GFX; }
u16* Simulation::bg_GFX() { return f_BG_GFX; }

const u16* Simulation::bg_Map() const { return f_BG_Map; }
u16* Simulation::bg_Map() { return f_BG_Map; }

s32 Simulation::view_Zoom() const { return f_View_Zoom; }
void Simulation::view_Zoom(s32 value)
{
    f_View_Zoom = value;
    m_View_FixSize();
}

s32 Simulation::view_W() const { return f_View_W; }

s32 Simulation::view_H() const { return f_View_H; }

s32 Simulation::view_Max_X() const { return f_View_Max_X; }

s32 Simulation::view_Max_Y() const { return f_View_Max_Y; }

s32 Simulation::view_X() const  { return f_View_X; }
void Simulation::view_X(s32 value)
{
    f_View_X = value;
    m_View_FixPosition();
}

s32 Simulation::view_Y() const { return f_View_Y; }
void Simulation::view_Y(s32 value)
{
    f_View_Y = value;
    m_View_FixPosition();
}

u32 Simulation::speed() const { return f_Speed; }
void Simulation::speed(u32 value)
{
    if (value < speed_Min)
        f_Speed = speed_Min;
    else if (value > speed_Max)
        f_Speed = speed_Max;
    else f_Speed = value;
    f_Gen_Length = GEN_LENGTH(f_Speed);
}

u32 Simulation::sim_Live() const { return f_Sim_Live; }

u32 Simulation::sim_Gen() const { return f_Sim_Gen; }

#pragma endregion

#pragma region helper functions

void Simulation::m_View_FixSize()
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

void Simulation::m_View_FixPosition()
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

void Simulation::markDirty()
{
    f_IsDirty = true;
}

void Simulation::update(u16 delta)
{
    if (delta > 0) // If zero, assume program is paused
    {
        f_Gen_Progress += delta;
        if (f_Gen_Progress >= f_Gen_Length)
        {
            // Next generation
            ++f_Sim_Gen;
            // Reset live cell count
            f_Sim_Live = 0;
            // Update pointer
            u8* prev_ptr = f_Map_Ptr;
            f_Map_Ptr = (f_Map_Ptr == f_Map_A) ? f_Map_B : f_Map_A;
            // Clear first row
            std::copy(f_Map_Empty, f_Map_Empty + BG_TILE_COLS, f_Map_Ptr);
            // Clear first column
            engine::helper::ArrayUtil::copy(f_Map_Empty, f_Map_Empty + BG_TILE_COUNT, f_Map_Ptr, BG_TILE_COLS);
            // Plot rows
            const u8* iptr = prev_ptr;
            const u8* eptr = f_Map_Empty;
            u8* optr = f_Map_Ptr;
            for (u16 y = 1; y < BG_TILE_ROWS; ++y)
            {
                for (u16 x = 1; x < BG_TILE_COLS; ++x)
                {
                    u8 tl = *iptr & 0x0F;
                    u8 tr = iptr[1] & 0x0F;
                    u8 bl = iptr[BG_TILE_COLS] & 0x0F;
                    u8 br = iptr[BG_TILE_COLS + 1] & 0x0F;
                    ++iptr;
                    if (tl != 0 || tr != 0 || bl != 0 || br != 0)
                    {
                        bool live;
                        u8 neighbors;
                        // Get TL
                        bool x0y0 = (tl & 0b0001) != 0;
                        bool x1y0 = (tl & 0b0010) != 0;
                        bool x0y1 = (tl & 0b0100) != 0;
                        bool x1y1 = (tl & 0b1000) != 0;
                        // Get TR
                        bool x2y0 = (tr & 0b0001) != 0;
                        bool x3y0 = (tr & 0b0010) != 0;
                        bool x2y1 = (tr & 0b0100) != 0;
                        bool x3y1 = (tr & 0b1000) != 0;
                        // Get BL
                        bool x0y2 = (bl & 0b0001) != 0;
                        bool x1y2 = (bl & 0b0010) != 0;
                        bool x0y3 = (bl & 0b0100) != 0;
                        bool x1y3 = (bl & 0b1000) != 0;
                        // Get BR
                        bool x2y2 = (br & 0b0001) != 0;
                        bool x3y2 = (br & 0b0010) != 0;
                        bool x2y3 = (br & 0b0100) != 0;
                        bool x3y3 = (br & 0b1000) != 0;
                        // Set TL
                        neighbors = 0;
                        if (x0y0) ++neighbors; if (x1y0) ++neighbors; if (x2y0) ++neighbors; if (x0y1) ++neighbors;
                        if (x0y2) ++neighbors; if (x1y2) ++neighbors; if (x2y2) ++neighbors; if (x2y1) ++neighbors;
                        if (x1y1) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                        if (live) { *optr |= 0b1000; ++f_Sim_Live; }
                        eptr += BG_TILE_COLS;
                        optr += BG_TILE_COLS;
                        // Set BL
                        neighbors = 0;
                        if (x0y1) ++neighbors; if (x1y1) ++neighbors; if (x2y1) ++neighbors; if (x0y2) ++neighbors;
                        if (x0y3) ++neighbors; if (x1y3) ++neighbors; if (x2y3) ++neighbors; if (x2y2) ++neighbors;
                        if (x1y2) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                        if (live) { *optr |= 0b0010; ++f_Sim_Live; }
                        eptr += 1;
                        optr += 1;
                        // Set BR
                        neighbors = 0;
                        if (x1y1) ++neighbors; if (x2y1) ++neighbors; if (x3y1) ++neighbors; if (x1y2) ++neighbors;
                        if (x1y3) ++neighbors; if (x2y3) ++neighbors; if (x3y3) ++neighbors; if (x3y2) ++neighbors;
                        if (x2y2) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                        *optr = *eptr;
                        if (live) { *optr |= 0b0001; ++f_Sim_Live; }
                        *optr = *eptr | (live ? 0b0001 : 0b0000);
                        eptr -= BG_TILE_COLS;
                        optr -= BG_TILE_COLS;
                        // Set TR
                        neighbors = 0;
                        if (x1y0) ++neighbors; if (x2y0) ++neighbors; if (x3y0) ++neighbors; if (x1y1) ++neighbors;
                        if (x1y2) ++neighbors; if (x2y2) ++neighbors; if (x3y2) ++neighbors; if (x3y1) ++neighbors;
                        if (x2y1) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                        if (live) { *optr |= 0b0100; ++f_Sim_Live; }
                    }
                    else
                    {
                        optr[BG_TILE_COLS + 1] = eptr[BG_TILE_COLS + 1];
                        ++eptr; ++optr;
                    }
                }
                ++iptr; ++eptr; ++optr;
            }
            // Mark as dirty
            f_IsDirty = true;
            // Wrap progress
            f_Gen_Progress = f_Gen_Progress % f_Gen_Length;
        }
    }
}

void Simulation::vblank()
{
    // Update dirty
    if (!f_IsDirty) return;
    f_IsDirty = false;
    // Update background
    DC_FlushRange(f_Map_Ptr, BG_TILE_COUNT);
    dmaCopy(f_Map_Ptr, f_BG_Map, BG_TILE_COUNT);
}

#pragma endregion