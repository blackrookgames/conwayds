#include "engine/data/RLE.h"
#include "engine/helper/ArrayUtil.h"
#include "game/scns/sim/Scene.h"

#include <cstdio>
#include <cstring>
#include <iomanip>
#include <nds/debug.h>

#include <__.h>
#include "engine/data/Pattern.h"
#include "game/assets/Palette.h"
#include "game/assets/SimScreen.h"
#include "game/assets/SimTileset.h"
#include "game/assets/TextTileset.h"

#include <sstream>

using namespace game::scns::sim;

#pragma region init

Scene::Scene()
{
    f_Simulation = nullptr;

    u16* test_data;
    size_t test_len;
    engine::data::RLE::extract(
        game::assets::SimScreen::data, game::assets::SimScreen::size,
        test_data, test_len);
    NOCASHMESSAGE(test_len)
    for (size_t i = 1; i < test_len; i += 32)
    {
        std::ostringstream test;
        for (size_t j = 0; j < 32; ++j)
            test << test_data[i + j] << ' ';
        test << std::endl;
        nocashMessage(test);
    }
}

Scene::~Scene()
{
    if (f_Simulation) delete[] f_Simulation;
}

#pragma endregion

#pragma region helper functions

void Scene::m_enter()
{
    engine::scenes::Scene::m_enter();
    // Turn off screen
    DS_SCREEN_OFF
    // Initialize pause indicater
    f_Paused = false;
    // Initialize video
	videoSetMode(MODE_2_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);
    videoSetModeSub(MODE_0_2D);
    vramSetBankC(VRAM_C_SUB_BG_0x06200000);
    // Initialize text graphics
    f_TextGFX = new engine::gfx::TextGFX(true, 0, 8, 0, 0);
    f_TextStream = new std::ostream(f_TextGFX);
    {
        f_TextGFX->clear();
        f_TextGFX->setCursor(1, 1);
        *f_TextStream << "Live:";
        f_TextStream->flush();
        f_TextGFX->setCursor(1, 3);
        *f_TextStream << "Gen:";
        f_TextStream->flush();
    }
    // Initialize simulation
    f_Simulation = new Simulation(3, 9, 0, 2);
    f_RegLen = f_Simulation->cycle_Length();
    // Initialize main palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE, assets::Palette::size);
    *BG_PALETTE = 0;
    // Initialize main tileset
	DC_FlushRange(assets::SimTileset::data, assets::SimTileset::size);
    dmaCopy(assets::SimTileset::data, f_Simulation->bg_GFX(), assets::SimTileset::size);
    // Initialize sub palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE_SUB, assets::Palette::size);
    *BG_PALETTE_SUB = 0;
    // Initialize sub tileset
	DC_FlushRange(assets::TextTileset::data, assets::TextTileset::size);
    dmaCopy(assets::TextTileset::data, f_TextGFX->bg_GFX(), assets::TextTileset::size);
    // Start timer
    timerStart(0, ClockDivider_1024, 0, nullptr);
    // Turn on screen
    DS_SCREEN_ON
}

void Scene::m_exit()
{
    // Stop timer
    timerStop(0);
    // Delete simulation
    delete f_Simulation;
    f_Simulation = nullptr;
    // Delete text graphics
    delete f_TextStream;
    delete f_TextGFX;
    // Base
    engine::scenes::Scene::m_exit();
}

void Scene::m_update()
{
    engine::scenes::Scene::m_update();
    // Get delta
    u16 delta = timerElapsed(0);
    // Update simulation
    f_Simulation->update(f_Paused ? 0 : delta);
    // Scan input
    scanKeys();
    if (keysDown() & KEY_START)
    {
        f_Paused = !f_Paused;
    }
    else
    {
        // Zoom
        if (keysCurrent() & KEY_L)
        {
            f_Simulation->view_Zoom(f_Simulation->view_Zoom() - 8);
        }
        if (keysCurrent() & KEY_R)
        {
            f_Simulation->view_Zoom(f_Simulation->view_Zoom() + 8);
        }
        // Pan
        s32 inc = 1024 / f_Simulation->view_W();
        if (keysCurrent() & KEY_LEFT)
        {
            f_Simulation->view_X(f_Simulation->view_X() - inc);
        }
        if (keysCurrent() & KEY_RIGHT)
        {
            f_Simulation->view_X(f_Simulation->view_X() + inc);
        }
        if (keysCurrent() & KEY_UP)
        {
            f_Simulation->view_Y(f_Simulation->view_Y() - inc);
        }
        if (keysCurrent() & KEY_DOWN)
        {
            f_Simulation->view_Y(f_Simulation->view_Y() + inc);
        }
        // Fast forward
        if (keysCurrent() & KEY_X) f_Simulation->cycle_Length(1000);
        else f_Simulation->cycle_Length(f_RegLen);
    }
    // Update text
    f_TextGFX->setCursor(10, 1);
    *f_TextStream << std::left << std::setw(12) << f_Simulation->sim_Live();
    f_TextStream->flush();
    f_TextGFX->setCursor(10, 3);
    *f_TextStream << std::left << std::setw(12) << f_Simulation->sim_Gen();
    f_TextStream->flush();
    // VBlank
    swiWaitForVBlank();
    f_Simulation->vblank();
    f_TextGFX->vblank();
    // Update backgrounds
    bgUpdate();
}

#pragma endregion