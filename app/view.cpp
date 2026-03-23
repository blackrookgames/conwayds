#include <algorithm>
#include <filesystem.h>
#include <nds.h>
#include <stdio.h>

#include "engine/helper/_macros.h"
#include "engine/helper/RRValue32.h"
#include "game/assets/Palette.h"
#include "game/assets/SimTileset.h"

namespace assets = game::assets;

int main()
{
    DS_SCREEN_OFF

	videoSetMode(MODE_2_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);
    videoSetModeSub(MODE_0_2D);
    vramSetBankC(VRAM_C_SUB_BG_0x06200000);

    int bg = bgInit(3, BgType_Rotation, BgSize_R_1024x1024, 5, 0);
	u16* bg_Gfx = bgGetGfxPtr(bg);
    u16* bg_Map = bgGetMapPtr(bg);
    // Initialize palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE, assets::Palette::size);
    *BG_PALETTE = 0;
    // Initialize tileset
	DC_FlushRange(assets::SimTileset::data, assets::SimTileset::size);
    dmaCopy(assets::SimTileset::data, bg_Gfx, assets::SimTileset::size);

    constexpr size_t cols = 1024 / 8;
    constexpr size_t rows = 1024 / 8;
    constexpr size_t count = cols * rows;
    constexpr size_t ww = 4;
    constexpr size_t hh = 4;
    u8* mapBuffer = new u8[count]();
    std::fill(mapBuffer, mapBuffer + count, 0);
    for (size_t y = 0; y < rows; y += hh)
    {
        for (size_t x = 0; x < cols; x += ww)
        {
            if (((y / hh) % 2) == 0) { if (((x / ww) % 2) == 1) continue; }
            else if (((x / ww) % 2) == 0) continue;
            u8* ptr = mapBuffer + x + y * cols;
            // Top
            ptr[0] = 0x07;
            ptr[1] = 0x03;
            ptr[2] = 0x03;
            ptr[3] = 0x0B;
            ptr += cols;
            // Middle 0
            ptr[0] = 0x05;
            ptr[3] = 0x0A;
            ptr += cols;
            // Middle 1
            ptr[0] = 0x05;
            ptr[3] = 0x0A;
            ptr += cols;
            // Bottom
            ptr[0] = 0x0D;
            ptr[1] = 0x0C;
            ptr[2] = 0x0C;
            ptr[3] = 0x0E;
        }
    }
    DC_FlushRange(mapBuffer, count);
    dmaCopy(mapBuffer, bg_Map, count);
    delete[] mapBuffer;
    
    DS_SCREEN_ON

    setBackdropColor(RGB15(31, 0, 0));

    engine::helper::RRValue32 v0(1, 64);
    engine::helper::RRValue32 v1(0, 128);
    char* test = v0.mul(v1).toStr();
    nocashMessage(test);
    delete[] test;

    
    while (pmMainLoop())
    {
        scanKeys();
        if (keysCurrent() & KEY_LEFT)
        {
            
        }
        if (keysCurrent() & KEY_RIGHT)
        {
            
        }
        if (keysCurrent() & KEY_UP)
        {
            
        }
        if (keysCurrent() & KEY_DOWN)
        {
            
        }
        if (keysCurrent() & KEY_L)
        {
            
        }
        if (keysCurrent() & KEY_R)
        {
            
        }
        // VBlank
        swiWaitForVBlank();
        // f_Simulation->vblank();
        // f_TextGFX->vblank();
        // Update backgrounds
        
        bgSetScroll(bg, -16, -16);
        bgUpdate();
    }

    return 0;
}
