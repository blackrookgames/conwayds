#include "game/scns/sim/Scene.h"

#include "game/assets/Palette.h"
#include "game/assets/SimTileset.h"
#include "game/assets/Zach.h"

#include <stdio.h>

using namespace game::scns::sim;

#pragma region macros

#define SCALE_MIN 64
#define SCALE_MAX 1024
#define SCALE_INC 8

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
    
    const u8* iptr = game::assets::Zach::data + 8; // Assume size of 256 x 256
    u8* optr = new u8[128 * 128]();
    bool hasrle = *(iptr++) != 0;
    u8 rleval = *(iptr++);
    if (hasrle) { }
    else
    {
        u32 i = 0;
        while (i < (256 * 256))
        {
            u8 mask = 1;
            for (u8 j = 0; j < 8; ++j)
            {
                u32 x = i & 0xFF;
                u32 y = i >> 8;
                u32 pos = (x >> 1) + ((y >> 1) << 7);
                u8 omsk = 1 << ((x & 1) | ((y & 1) << 1));
                // Set bit
                if ((*iptr & mask) != 0) optr[pos] |= omsk;
                // Next bit
                ++i;
                mask <<= 1;
            }
            // Next byte
            ++iptr;
        }
    } 
	DC_FlushRange(optr, 128 * 128);
    dmaCopy(optr, f_main_3_map, 128 * 128);
    delete[] optr;

    f_scale = 128;
    bgSetScale(f_main_3, f_scale, f_scale);
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
        fprintf(stderr, "Start\n");
    }
    if (keysCurrent() & KEY_L)
    {
        f_scale += SCALE_INC;
        if (f_scale > SCALE_MAX) f_scale = SCALE_MAX;
        bgSetScale(f_main_3, f_scale, f_scale);
    }
    if (keysCurrent() & KEY_R)
    {
        f_scale -= SCALE_INC;
        if (f_scale < SCALE_MIN) f_scale = SCALE_MIN;
        bgSetScale(f_main_3, f_scale, f_scale);
    }
    
    bgUpdate();
}

#pragma endregion