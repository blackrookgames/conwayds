#include "engine/helper/ArrayUtil.h"
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

#define MAIN_3_MAP_WIDTH 128
#define MAIN_3_MAP_HEIGHT 128
#define MAIN_3_MAP_AREA (MAIN_3_MAP_WIDTH * MAIN_3_MAP_HEIGHT)

#define VIEW_3_MIN 64
#define VIEW_3_MAX 1024
#define VIEW_3_INC 8

#define CYCLE_LENGTH_MIN 1000
#define CYCLE_LENGTH_MAX 100000

#pragma endregion

#pragma region properties


u32 Scene::cycle_length() const { return f_cycle_length; }

void Scene::cycle_length(u32 value)
{
    if (value < CYCLE_LENGTH_MIN)
        f_cycle_length = CYCLE_LENGTH_MIN;
    else if (value > CYCLE_LENGTH_MAX)
        f_cycle_length = CYCLE_LENGTH_MAX;
    else f_cycle_length = value;
}

#pragma endregion

#pragma region helper functions

void sim_initEmpty(u8* output)
{
    u8* optr = output;
    // Top
    *(optr++) = 0x10;
    for (u16 x = 2; x < MAIN_3_MAP_WIDTH; ++x) *(optr++) = 0x70;
    *(optr++) = 0x20;
    // Top
    for (u16 y = 2; y < MAIN_3_MAP_HEIGHT; ++y)
    {
        *(optr++) = 0x50;
        for (u16 x = 2; x < MAIN_3_MAP_WIDTH; ++x) *(optr++) = 0x00;
        *(optr++) = 0x60;
    }
    // Bottom
    *(optr++) = 0x30;
    for (u16 x = 2; x < MAIN_3_MAP_WIDTH; ++x) *(optr++) = 0x80;
    *(optr++) = 0x40;

}

void sim_loadPattern(const char* path, const u8* empty, u8* output)
{
    // Open pattern
    engine::data::Pattern pattern;
    pattern.load_file(path);
    // Clear first row
    std::copy(empty, empty + MAIN_3_MAP_WIDTH, output);
    // Clear first column
    engine::helper::ArrayUtil::copy(empty, empty + MAIN_3_MAP_AREA, output, MAIN_3_MAP_WIDTH);
    // Plot rows
    u8* optr = output;
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
    f_sim_empty = new u8[MAIN_3_MAP_AREA];
    f_sim_tiles_a = new u8[MAIN_3_MAP_AREA];
    f_sim_tiles_b = new u8[MAIN_3_MAP_AREA];
    f_sim_ptr = f_sim_tiles_a;
    f_sim_dirty = true;
    sim_initEmpty(f_sim_empty);
    sim_loadPattern("nitro:/samples/sample0.bin", f_sim_empty, f_sim_ptr);

    // Initialize video
	videoSetMode(MODE_2_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);

    // Initialize background layer
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
    delete[] f_sim_empty;

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
    // Update pointer
    u8* prev_ptr = f_sim_ptr;
    f_sim_ptr = (f_sim_ptr == f_sim_tiles_a) ? f_sim_tiles_b : f_sim_tiles_a;
    // Clear first row
    std::copy(f_sim_empty, f_sim_empty + MAIN_3_MAP_WIDTH, f_sim_ptr);
    // Clear first column
    engine::helper::ArrayUtil::copy(f_sim_empty, f_sim_empty + MAIN_3_MAP_AREA, f_sim_ptr, MAIN_3_MAP_WIDTH);
    // Plot rows
    const u8* iptr = prev_ptr;
    const u8* eptr = f_sim_empty;
    u8* optr = f_sim_ptr;
    for (u16 y = 1; y < MAIN_3_MAP_HEIGHT; ++y)
    {
        for (u16 x = 1; x < MAIN_3_MAP_WIDTH; ++x)
        {
            u8 tl = *iptr & 0x0F;
            u8 tr = iptr[1] & 0x0F;
            u8 bl = iptr[MAIN_3_MAP_WIDTH] & 0x0F;
            u8 br = iptr[MAIN_3_MAP_WIDTH + 1] & 0x0F;
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
                if (live) *optr |= 0b1000;
                eptr += MAIN_3_MAP_WIDTH;
                optr += MAIN_3_MAP_WIDTH;
                // Set BL
                neighbors = 0;
                if (x0y1) ++neighbors; if (x1y1) ++neighbors; if (x2y1) ++neighbors; if (x0y2) ++neighbors;
                if (x0y3) ++neighbors; if (x1y3) ++neighbors; if (x2y3) ++neighbors; if (x2y2) ++neighbors;
                if (x1y2) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                if (live) *optr |= 0b0010;
                eptr += 1;
                optr += 1;
                // Set BR
                neighbors = 0;
                if (x1y1) ++neighbors; if (x2y1) ++neighbors; if (x3y1) ++neighbors; if (x1y2) ++neighbors;
                if (x1y3) ++neighbors; if (x2y3) ++neighbors; if (x3y3) ++neighbors; if (x3y2) ++neighbors;
                if (x2y2) live = (neighbors >= 2 && neighbors <= 3); else live = neighbors == 3;
                *optr = *eptr | (live ? 0b0001 : 0b0000);
                eptr -= MAIN_3_MAP_WIDTH;
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
                optr[MAIN_3_MAP_WIDTH + 1] = eptr[MAIN_3_MAP_WIDTH + 1];
                ++eptr; ++optr;
            }
        }
        ++iptr; ++eptr; ++optr;
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
    m_update_scroll();
    bgSetScale(f_main_3, f_view_w, f_view_w); // f_view_3_w is the scale for both axes
}

void Scene::m_update_scroll()
{
    bgSetScroll(f_main_3, f_view_x, f_view_y);
}

#pragma endregion