#include "game/scns/sim/Scene.h"

#include <cstdio>
#include <cstring>
#include <nds/debug.h>

#include <__.h>
#include "engine/data/Pattern.h"
#include "game/assets/Palette.h"
#include "game/assets/SimTileset.h"

using namespace game::scns::sim;

#pragma region macros

#define SIM_WIDTH (PATTERN_HEIGHT / 2)
#define SIM_HEIGHT (PATTERN_WIDTH / 2)
#define SIM_X1 (SIM_WIDTH / 2)
#define SIM_Y1 (SIM_HEIGHT / 2)
#define SIM_X2 (SIM_X1 + SIM_WIDTH)
#define SIM_Y2 (SIM_Y1 + SIM_HEIGHT)
#define SIM_FULLW PATTERN_WIDTH
#define SIM_FULLH PATTERN_HEIGHT
#define SIM_AREA (SIM_FULLW * SIM_FULLH)

#define MAIN_3_MAP_WIDTH 128
#define MAIN_3_MAP_HEIGHT 128
#define MAIN_3_MAP_AREA (MAIN_3_MAP_WIDTH * MAIN_3_MAP_HEIGHT)

#define VIEWSIZE_MIN 64
#define VIEWSIZE_MAX 1024
#define VIEWSIZE_INC 8

#pragma endregion

#pragma region init

Scene::Scene() { }

Scene::~Scene() { }

#pragma endregion

#pragma region helper functions

void Scene::m_enter()
{
    engine::scenes::Scene::m_enter();
    
    f_sim_a = new u8[SIM_AREA];
    f_sim_b = new u8[SIM_AREA];
    f_sim_ptr = f_sim_a;
    {
        // Open pattern
        engine::data::Pattern pattern;
        pattern.load_file("nitro:/samples/sample0.bin");
        // Load pattern onto simulation
        const bool* iptr = pattern.cells();
        u8* optr = f_sim_a;
        for (u16 oy = 0; oy < SIM_FULLH; ++oy)
        {
            bool yinrange = oy >= SIM_Y1 && oy < SIM_Y2;
            for (u16 ox = 0; ox < SIM_FULLW; ++ox)
            {
                if (yinrange && ox >= SIM_X1 && ox < SIM_X2)
                {
                    // Compute tile
                    u8 tile = 
                        (*iptr ? 0b0001 : 0b0000) | 
                        (iptr[1] ? 0b0010 : 0b0000) |
                        (iptr[PATTERN_WIDTH] ? 0b0100 : 0b0000) |
                        (iptr[PATTERN_WIDTH + 1] ? 0b1000 : 0b0000);
                    // Set tile
                    *optr = tile;
                    // Next
                    iptr += 2;
                }
                else
                {
                    *optr = 0b0000;
                }
                ++optr;
            }
            if (yinrange) iptr += PATTERN_WIDTH;
        }
    }

	videoSetMode(MODE_2_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);

    f_main_3 = bgInit(3, BgType_Rotation, BgSize_R_1024x1024, 0, 1);
	f_main_3_gfx = bgGetGfxPtr(f_main_3);
    f_main_3_map = bgGetMapPtr(f_main_3);
    f_main_3_buffer = new u8[MAIN_3_MAP_AREA];

	DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE, assets::Palette::size);

	DC_FlushRange(assets::SimTileset::data, assets::SimTileset::size);
    dmaCopy(assets::SimTileset::data, f_main_3_gfx, assets::SimTileset::size);

    m_update_view_size(256);
    f_view_x = (VIEWSIZE_MAX - f_view_w) / 2;
    f_view_y = (VIEWSIZE_MAX - f_view_h) / 2;
    bgSetScroll(f_main_3, f_view_x, f_view_y);;

    m_update_simtiles();
    
    timerStart(0, ClockDivider_1024, 0, nullptr);

    f_paused = false;

    f_cycle_length = 10000;
    f_cycle_progress = 0;
}

void Scene::m_exit()
{
    timerStop(0);

    delete[] f_main_3_buffer;

    delete[] f_sim_b;
    delete[] f_sim_a;

    engine::scenes::Scene::m_exit();
}

void Scene::m_update()
{
    engine::scenes::Scene::m_update();

    u16 ticks = timerElapsed(0);
    if (f_paused) m_update_paused();
    else m_update_unpaused(ticks);
    
    bgUpdate();
}

void Scene::m_update_unpaused(u16 ticks)
{
    // Update cycle
    f_cycle_progress += ticks;
    if (f_cycle_progress >= f_cycle_length)
    {
        m_update_sim();
        f_cycle_progress = f_cycle_progress % f_cycle_length;
    }

    // Scan input
    scanKeys();
    if (keysDown() & KEY_START)
    {
        f_paused = true;
    }
    else
    {
        if (keysCurrent() & KEY_L)
        {
            m_update_view_size(f_view_w + VIEWSIZE_INC);
        }
        if (keysCurrent() & KEY_R)
        {
            m_update_view_size(f_view_w - VIEWSIZE_INC);
        }
        if (keysCurrent() & KEY_LEFT)
        {
            f_view_x -= f_view_inc;
            if (f_view_x < 0) f_view_x = 0;
            bgSetScroll(f_main_3, f_view_x, f_view_y);
        }
        if (keysCurrent() & KEY_RIGHT)
        {
            f_view_x += f_view_inc;
            if (f_view_x > f_view_max_x) f_view_x = f_view_max_x;
            bgSetScroll(f_main_3, f_view_x, f_view_y);
        }
        if (keysCurrent() & KEY_UP)
        {
            f_view_y -= f_view_inc;
            if (f_view_y < 0) f_view_y = 0;
            bgSetScroll(f_main_3, f_view_x, f_view_y);
        }
        if (keysCurrent() & KEY_DOWN)
        {
            f_view_y += f_view_inc;
            if (f_view_y > f_view_max_y) f_view_y = f_view_max_y;
            bgSetScroll(f_main_3, f_view_x, f_view_y);
        }
    }
}

void Scene::m_update_paused()
{
    // Scan input
    scanKeys();
    if (keysDown() & KEY_START)
    {
        f_paused = false;
    }
}

void Scene::m_update_sim()
{
    const u8* iptr;
    u8* optr;
    // Update pointer
    u8* prev_ptr = f_sim_ptr;
    f_sim_ptr = (f_sim_ptr == f_sim_a) ? f_sim_b : f_sim_a;
    // Clear first row
    std::fill(f_sim_ptr, f_sim_ptr + SIM_FULLW, (u8)0);
    // Clear first column
    optr = f_sim_ptr;
    for (u16 y = 0; y < SIM_FULLH; ++y) *(optr++) = 0;
    // Plot rows
    iptr = prev_ptr;
    optr = f_sim_ptr;
    for (u16 y = 1; y < SIM_FULLH; ++y)
    {
        for (u16 x = 1; x < SIM_FULLW; ++x)
        {
            if (*iptr != 0 || iptr[1] != 0 || iptr[SIM_FULLW] != 0 || iptr[SIM_FULLW + 1] != 0)
            {
                bool live;
                u8 neighbors;
                // Get TL
                bool x0y0 = (*iptr & 0b0001) != 0;
                bool x1y0 = (*iptr & 0b0010) != 0;
                bool x0y1 = (*iptr & 0b0100) != 0;
                bool x1y1 = (*iptr & 0b1000) != 0;
                iptr += SIM_FULLW;
                // Get BL
                bool x0y2 = (*iptr & 0b0001) != 0;
                bool x1y2 = (*iptr & 0b0010) != 0;
                bool x0y3 = (*iptr & 0b0100) != 0;
                bool x1y3 = (*iptr & 0b1000) != 0;
                iptr += 1;
                // Get BR
                bool x2y2 = (*iptr & 0b0001) != 0;
                bool x3y2 = (*iptr & 0b0010) != 0;
                bool x2y3 = (*iptr & 0b0100) != 0;
                bool x3y3 = (*iptr & 0b1000) != 0;
                iptr -= SIM_FULLW;
                // Get TR
                bool x2y0 = (*iptr & 0b0001) != 0;
                bool x3y0 = (*iptr & 0b0010) != 0;
                bool x2y1 = (*iptr & 0b0100) != 0;
                bool x3y1 = (*iptr & 0b1000) != 0;
                // Set TL
                neighbors = 0;
                if (x0y0) ++neighbors; if (x1y0) ++neighbors; if (x2y0) ++neighbors; if (x0y1) ++neighbors;
                if (x0y2) ++neighbors; if (x1y2) ++neighbors; if (x2y2) ++neighbors; if (x2y1) ++neighbors;
                if (x1y1) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                if (live) *optr |= 0b1000;
                optr += SIM_FULLW;
                // Set BL
                neighbors = 0;
                if (x0y1) ++neighbors; if (x1y1) ++neighbors; if (x2y1) ++neighbors; if (x0y2) ++neighbors;
                if (x0y3) ++neighbors; if (x1y3) ++neighbors; if (x2y3) ++neighbors; if (x2y2) ++neighbors;
                if (x1y2) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                if (live) *optr |= 0b0010;
                optr += 1;
                // Set BR
                neighbors = 0;
                if (x1y1) ++neighbors; if (x2y1) ++neighbors; if (x3y1) ++neighbors; if (x1y2) ++neighbors;
                if (x1y3) ++neighbors; if (x2y3) ++neighbors; if (x3y3) ++neighbors; if (x3y2) ++neighbors;
                if (x2y2) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                *optr = live ? 0b0001 : 0b0000; // Use set, not or
                optr -= SIM_FULLW;
                // Set TR
                neighbors = 0;
                if (x1y0) ++neighbors; if (x2y0) ++neighbors; if (x3y0) ++neighbors; if (x1y1) ++neighbors;
                if (x1y2) ++neighbors; if (x2y2) ++neighbors; if (x3y2) ++neighbors; if (x3y1) ++neighbors;
                if (x2y1) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                if (live) *optr |= 0b0100;
            }
            else
            {
                optr[SIM_FULLW + 1] = 0;
                ++iptr; ++optr;
            }
        }
        ++iptr; ++optr;
    }
    // Update tiles
    m_update_simtiles();
}

void Scene::m_update_simtiles()
{
    const u8* iptr = f_sim_ptr + SIM_X1 + SIM_Y1 * SIM_FULLW;
    u8* optr = (u8*)f_main_3_map;
    DC_FlushRange(f_main_3_map, SIM_FULLW * SIM_FULLH);
    for (u16 y = 0; y < SIM_HEIGHT; ++y)
    {
        dmaCopy(iptr, optr, SIM_WIDTH);
        iptr += SIM_FULLW;
        optr += SIM_WIDTH;
    }
}

void Scene::m_update_view_size(s32 size)
{
    s32 off_x = f_view_x + f_view_w / 2;
    s32 off_y = f_view_y + f_view_h / 2;
    // Set size
    if (size < VIEWSIZE_MIN)
        f_view_w = VIEWSIZE_MIN;
    else if (size > VIEWSIZE_MAX)
        f_view_w = VIEWSIZE_MAX;
    else
        f_view_w = size;
    f_view_h = (f_view_w * DS_SCREEN_HEIGHT + DS_SCREEN_WIDTH - 1) / DS_SCREEN_WIDTH;
    // Update max
    f_view_max_x = VIEWSIZE_MAX - f_view_w;
    f_view_max_y = VIEWSIZE_MAX - f_view_h;
    // Update inc
    f_view_inc = VIEWSIZE_MAX / f_view_w;
    // Update position
    f_view_x = off_x - f_view_w / 2;
    f_view_y = off_y - f_view_h / 2;
    if (f_view_x < 0) f_view_x = 0;
    if (f_view_y < 0) f_view_y = 0;
    if (f_view_x > f_view_max_x) f_view_x = f_view_max_x;
    if (f_view_y > f_view_max_y) f_view_y = f_view_max_y;
    // Update background
    bgSetScroll(f_main_3, f_view_x, f_view_y);
    bgSetScale(f_main_3, f_view_w, f_view_w); // f_view_w is the scale for both axes
}

#pragma endregion