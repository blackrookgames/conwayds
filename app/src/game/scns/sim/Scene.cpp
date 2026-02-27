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

#define MAIN_2_MAP_WIDTH 32
#define MAIN_2_MAP_HEIGHT 32
#define MAIN_2_MAP_AREA (MAIN_2_MAP_WIDTH * MAIN_2_MAP_HEIGHT)

#define MAIN_3_MAP_WIDTH 128
#define MAIN_3_MAP_HEIGHT 128
#define MAIN_3_MAP_AREA (MAIN_3_MAP_WIDTH * MAIN_3_MAP_HEIGHT)

#define VIEW_2_MIN 16
#define VIEW_2_MAX 256
#define VIEW_2_INC 2
#define VIEW_3_MIN 64
#define VIEW_3_MAX 1024
#define VIEW_3_INC 8

#pragma endregion

#pragma region init

Scene::Scene() { }

Scene::~Scene() { }

#pragma endregion

#pragma region helper functions

void Scene::m_enter()
{
    engine::scenes::Scene::m_enter();

    // Initialize simulation
    f_sim_tiles_a = new u8[MAIN_3_MAP_AREA];
    f_sim_tiles_b = new u8[MAIN_3_MAP_AREA];
    f_sim_ptr = f_sim_tiles_a;
    f_sim_dirty = true;
    {
        u8* optr;
        // Open pattern
        engine::data::Pattern pattern;
        pattern.load_file("nitro:/samples/sample0.bin");
        // Clear first row
        std::fill(f_sim_ptr, f_sim_ptr + MAIN_3_MAP_WIDTH, (u8)0);
        // Clear first column
        optr = f_sim_ptr;
        for (u16 y = 0; y < MAIN_3_MAP_HEIGHT; ++y) { *optr = 0; optr += MAIN_3_MAP_WIDTH; }
        // Plot rows
        optr = f_sim_ptr;
        for (u16 iy = 0; iy < PATTERN_HEIGHT; iy += 2)
        {
            for (u16 ix = 0; ix < PATTERN_WIDTH; ix += 2)
            {
                if (pattern.getcell(ix, iy)) *optr |= 0b1000;
                if (pattern.getcell(ix + 1, iy)) optr[1] |= 0b0100;
                if (pattern.getcell(ix, iy + 1)) optr[MAIN_3_MAP_WIDTH] |= 0b0010;
                optr[MAIN_3_MAP_WIDTH + 1] = pattern.getcell(ix + 1, iy + 1) ? 0b0001 : 0b0000;
                ++optr;
            }
            ++optr;
        }
    }

    // Initialize video
	videoSetMode(MODE_2_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);

    // Initialize "back" background layer
    f_main_2 = bgInit(2, BgType_Rotation, BgSize_R_256x256, 8, 0);
	f_main_2_gfx = bgGetGfxPtr(f_main_2);
    f_main_2_map = bgGetMapPtr(f_main_2);
    bgSetPriority(f_main_2, 3);

    // Initialize "fore" background layer
    f_main_3 = bgInit(3, BgType_Rotation, BgSize_R_1024x1024, 9, 0);
	f_main_3_gfx = bgGetGfxPtr(f_main_3);
    f_main_3_map = bgGetMapPtr(f_main_3);
    f_main_3_buffer = new u8[MAIN_3_MAP_AREA];
    bgSetPriority(f_main_3, 2);

    // Setup palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE, assets::Palette::size);

    // Setup palette
	DC_FlushRange(assets::SimTileset::data, assets::SimTileset::size);
    dmaCopy(assets::SimTileset::data, f_main_3_gfx, assets::SimTileset::size);

    // Setup view
    m_update_view_size(256);
    f_view_x = (VIEW_3_MAX - f_view_w) / 2;
    f_view_y = (VIEW_3_MAX - f_view_h) / 2;
    m_update_scroll();

    // Setup "fore" background layer tiles
    m_update_simtiles();

    // Setup "back" background layer tiles
    {
        u8* temp = new u8[MAIN_2_MAP_AREA];
        u8* optr = temp;
        // Top
        *(optr++) = 0x10;
        for (u8 x = 2; x < MAIN_2_MAP_WIDTH; ++x) *(optr++) = 0x14;
        *(optr++) = 0x11;
        // Middle
        for (u8 y = 2; y < MAIN_2_MAP_HEIGHT; ++y)
        {
            *(optr++) = 0x16;
            for (u8 x = 2; x < MAIN_2_MAP_WIDTH; ++x) *(optr++) = 0x00;
            *(optr++) = 0x17;
        }
        // Bottom
        *(optr++) = 0x12;
        for (u8 x = 2; x < MAIN_2_MAP_WIDTH; ++x) *(optr++) = 0x15;
        *(optr++) = 0x13;
        // To VRAM
        DC_FlushRange(temp, MAIN_2_MAP_AREA);
        dmaCopy(temp, f_main_2_map, MAIN_2_MAP_AREA);
        // Dispose
        delete[] temp;
    }
    
    // Start timer
    timerStart(0, ClockDivider_1024, 0, nullptr);

    // Initialize pause indicater
    f_paused = false;

    // Initialize simulation cycles
    f_cycle_length = 5000;
    f_cycle_progress = 0;
}

void Scene::m_exit()
{
    timerStop(0);

    delete[] f_main_3_buffer;

    delete[] f_sim_tiles_b;
    delete[] f_sim_tiles_a;

    engine::scenes::Scene::m_exit();
}

void Scene::m_update()
{
    engine::scenes::Scene::m_update();

    u16 ticks = timerElapsed(0);
    if (f_paused) m_update_paused();
    else m_update_unpaused(ticks);
    
    swiWaitForVBlank();
    if (f_sim_dirty)
        m_update_simtiles();
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
            m_update_view_size(f_view_w + VIEW_3_INC);
        }
        if (keysCurrent() & KEY_R)
        {
            m_update_view_size(f_view_w - VIEW_3_INC);
        }
        if (keysCurrent() & KEY_LEFT)
        {
            f_view_x -= f_view_inc;
            if (f_view_x < 0) f_view_x = 0;
            m_update_scroll();
        }
        if (keysCurrent() & KEY_RIGHT)
        {
            f_view_x += f_view_inc;
            if (f_view_x > f_view_max_x) f_view_x = f_view_max_x;
            m_update_scroll();
        }
        if (keysCurrent() & KEY_UP)
        {
            f_view_y -= f_view_inc;
            if (f_view_y < 0) f_view_y = 0;
            m_update_scroll();
        }
        if (keysCurrent() & KEY_DOWN)
        {
            f_view_y += f_view_inc;
            if (f_view_y > f_view_max_y) f_view_y = f_view_max_y;
            m_update_scroll();
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
    f_sim_ptr = (f_sim_ptr == f_sim_tiles_a) ? f_sim_tiles_b : f_sim_tiles_a;
    // Clear first row
    std::fill(f_sim_ptr, f_sim_ptr + MAIN_3_MAP_WIDTH, (u8)0);
    // Clear first column
    optr = f_sim_ptr;
    for (u16 y = 0; y < MAIN_3_MAP_HEIGHT; ++y) *(optr++) = 0;
    // Plot rows
    iptr = prev_ptr;
    optr = f_sim_ptr;
    for (u16 y = 1; y < MAIN_3_MAP_HEIGHT; ++y)
    {
        for (u16 x = 1; x < MAIN_3_MAP_WIDTH; ++x)
        {
            if (*iptr != 0 || iptr[1] != 0 || iptr[MAIN_3_MAP_WIDTH] != 0 || iptr[MAIN_3_MAP_WIDTH + 1] != 0)
            {
                bool live;
                u8 neighbors;
                // Get TL
                bool x0y0 = (*iptr & 0b0001) != 0;
                bool x1y0 = (*iptr & 0b0010) != 0;
                bool x0y1 = (*iptr & 0b0100) != 0;
                bool x1y1 = (*iptr & 0b1000) != 0;
                iptr += MAIN_3_MAP_WIDTH;
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
                iptr -= MAIN_3_MAP_WIDTH;
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
                optr += MAIN_3_MAP_WIDTH;
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
                optr -= MAIN_3_MAP_WIDTH;
                // Set TR
                neighbors = 0;
                if (x1y0) ++neighbors; if (x2y0) ++neighbors; if (x3y0) ++neighbors; if (x1y1) ++neighbors;
                if (x1y2) ++neighbors; if (x2y2) ++neighbors; if (x3y2) ++neighbors; if (x3y1) ++neighbors;
                if (x2y1) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                if (live) *optr |= 0b0100;
            }
            else
            {
                optr[MAIN_3_MAP_WIDTH + 1] = 0;
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
    DC_FlushRange(f_sim_ptr, MAIN_3_MAP_AREA);
    dmaCopy(f_sim_ptr, f_main_3_map, MAIN_3_MAP_AREA);
    f_sim_dirty = false;
}

void Scene::m_update_view_size(s32 size)
{
    s32 off_x = f_view_x + f_view_w / 2;
    s32 off_y = f_view_y + f_view_h / 2;
    // Set size
    if (size < VIEW_3_MIN)
        f_view_w = VIEW_3_MIN;
    else if (size > VIEW_3_MAX)
        f_view_w = VIEW_3_MAX;
    else
        f_view_w = size;
    f_view_h = (f_view_w * DS_SCREEN_HEIGHT + DS_SCREEN_WIDTH - 1) / DS_SCREEN_WIDTH;
    // Update max
    f_view_max_x = VIEW_3_MAX - f_view_w;
    f_view_max_y = VIEW_3_MAX - f_view_h;
    // Update inc
    f_view_inc = VIEW_3_MAX / f_view_w;
    // Update position
    f_view_x = off_x - f_view_w / 2;
    f_view_y = off_y - f_view_h / 2;
    if (f_view_x < 0) f_view_x = 0;
    if (f_view_y < 0) f_view_y = 0;
    if (f_view_x > f_view_max_x) f_view_x = f_view_max_x;
    if (f_view_y > f_view_max_y) f_view_y = f_view_max_y;
    // Update background
    int size2 = f_view_w / 4;
    m_update_scroll();
    bgSetScale(f_main_2, size2, size2);
    bgSetScale(f_main_3, f_view_w, f_view_w); // f_view_3_w is the scale for both axes
}

void Scene::m_update_scroll()
{
    bgSetScroll(f_main_2, f_view_x / 4, f_view_y / 4);
    bgSetScroll(f_main_3, f_view_x, f_view_y);
}

#pragma endregion