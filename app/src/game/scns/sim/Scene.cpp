#include "game/scns/sim/Scene.h"

#include "engine/data/Pattern.h"
#include "game/assets/Palette.h"
#include "game/assets/SimTileset.h"

#include <cstdio>
#include <nds/debug.h>

using namespace game::scns::sim;

#pragma region macros

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

	videoSetMode(MODE_2_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);

    f_main_3 = bgInit(3, BgType_Rotation, BgSize_R_1024x1024, 0, 1);
	f_main_3_gfx = bgGetGfxPtr(f_main_3);
    f_main_3_map = bgGetMapPtr(f_main_3);

	DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE, assets::Palette::size);

	DC_FlushRange(assets::SimTileset::data, assets::SimTileset::size);
    dmaCopy(assets::SimTileset::data, f_main_3_gfx, assets::SimTileset::size);
    
    engine::data::Pattern pattern;
    pattern.load_file("nitro:/samples/sample0.bin");

    const u32 map_area = 128 * 128;
    u8* map = new u8[map_area]();
    {
        const bool* iptr = pattern.cells();
        for (u32 i = 0; i < PATTERN_AREA; ++i)
        {
            u32 x = i & 0xFF;
            u32 y = i >> 8;
            u32 pos = (x >> 1) + ((y >> 1) << 7);
            u8 omsk = 1 << ((x & 1) | ((y & 1) << 1));
            if (*(iptr++)) map[pos] |= omsk;
        }
    } 
	DC_FlushRange(map, map_area);
    dmaCopy(map, f_main_3_map, map_area);
    delete[] map;

    m_update_view_size(256);
    f_view_x = (VIEWSIZE_MAX - f_view_w) / 2;
    f_view_y = (VIEWSIZE_MAX - f_view_h) / 2;
    bgSetScroll(f_main_3, f_view_x, f_view_y);
}

void Scene::m_exit()
{
    engine::scenes::Scene::m_exit();
}

void Scene::m_update()
{
    engine::scenes::Scene::m_update();

	scanKeys();
	if (keysDown() & KEY_START)
    {
        nocashMessage("Start\n");
    }
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
    
    bgUpdate();
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