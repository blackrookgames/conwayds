#include "game/scns/edit/Scene.h"

#include <cstdio>
#include <cstring>
#include <iomanip>
#include <nds/debug.h>

#include <__.h>
#include "engine/data/Pattern.h"
#include "engine/data/RLE.h"
#include "engine/helper/ArrayUtil.h"
#include "game/assets/EditTileset.h"
#include "game/assets/Palette.h"
#include "game/assets/SimScreen.h"
#include "game/assets/SimScreenPause.h"
#include "game/assets/TextTileset.h"

#include "game/scns/sim/Scene.h"

using namespace game::scns::edit;

#pragma region helper functions

namespace game::scns::edit
{
    void loadScreenData(const u16* in_data, size_t in_len, u16*& out_data, size_t& out_len)
    {
        static constexpr size_t offset = 1;
        // Extract
        u16* temp_data;
        size_t temp_len;
        engine::data::RLE::extract(in_data, in_len, temp_data, temp_len);
        if (temp_len <= offset) { out_data = nullptr; out_len = 0; return; }
        // Create final array
        out_len = temp_len - offset;
        out_data = new u16[out_len];
        std::copy(temp_data + offset, temp_data + temp_len, out_data);
        delete[] temp_data;
    }
}

#pragma endregion

#pragma region init

Scene::Scene()
{
    f_Screen_Main = nullptr;
    f_Screen_Pause = nullptr;
    f_TextGFX = nullptr;
    f_TextStream = nullptr;
    f_Editor = nullptr;
}

Scene::~Scene() { }

#pragma endregion

#pragma region helper functions

void Scene::m_enter()
{
    engine::scenes::Scene::m_enter();
    // Turn off screen
    DS_SCREEN_OFF
    // Initialize video
	videoSetMode(MODE_0_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);
    videoSetModeSub(MODE_2_2D);
    vramSetBankC(VRAM_C_SUB_BG_0x06200000);
    // Initialize screen data
    loadScreenData(\
        game::assets::SimScreen::data, game::assets::SimScreen::size,\
        f_Screen_Main, f_Screen_Main_Len);
    loadScreenData(\
        game::assets::SimScreenPause::data, game::assets::SimScreenPause::size,\
        f_Screen_Pause, f_Screen_Pause_Len);
    // Initialize text graphics
    f_TextGFX = new engine::gfx::TextGFX(false, 0, 8, 0, 0);
    f_TextStream = new std::ostream(f_TextGFX);
    std::copy(f_Screen_Main, f_Screen_Main + f_Screen_Main_Len, f_TextGFX->bg_Buffer());
    // Initialize simulation
    f_Editor = new Editor(3, 9, 0, 2);
    // Initialize main palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE, assets::Palette::size);
    *BG_PALETTE = 0;
    // Initialize main tileset
	DC_FlushRange(assets::TextTileset::data, assets::TextTileset::size);
    dmaCopy(assets::TextTileset::data, f_TextGFX->bg_GFX(), assets::TextTileset::size);
    // Initialize sub palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE_SUB, assets::Palette::size);
    *BG_PALETTE_SUB = 0;
    // Initialize sub tileset
	DC_FlushRange(assets::EditTileset::data, assets::EditTileset::size);
    dmaCopy(assets::EditTileset::data, f_Editor->bg_GFX(), assets::EditTileset::size);
    // Start timer
    timerStart(0, ClockDivider_1024, 0, nullptr);
    // Turn on screen
    DS_SCREEN_ON
}

void Scene::m_exit()
{
    // Stop timer
    timerStop(0);
    // Delete
    DELETE_OBJECT(f_Editor)
    DELETE_OBJECT(f_TextStream)
    DELETE_OBJECT(f_TextGFX)
    DELETE_ARRAY(f_Screen_Pause)
    DELETE_ARRAY(f_Screen_Main)
    // Base
    engine::scenes::Scene::m_exit();
}

void Scene::m_update()
{
    engine::scenes::Scene::m_update();
    // Get delta
    u16 delta = timerElapsed(0);
    // Scan input
    touchRead(&f_TouchPos);
    scanKeys();
    if (keysDown() & KEY_START)
    {
        // Save pattern
        f_Editor->savePattern();
        // Goto simulation scene
        game::scns::sim::Scene* scene = new game::scns::sim::Scene();
        scene->deleteOnExit(true);
        engine::scenes::gotoScene(scene);
    }
    else
    {
        // Zoom
        if (keysCurrent() & KEY_L)
        {
            f_Editor->view_Zoom(f_Editor->view_Zoom() - 8);
        }
        if (keysCurrent() & KEY_R)
        {
            f_Editor->view_Zoom(f_Editor->view_Zoom() + 8);
        }
        // Pan
        s32 inc = 1024 / f_Editor->view_W();
        if (keysCurrent() & KEY_LEFT)
        {
            f_Editor->view_X(f_Editor->view_X() - inc);
        }
        if (keysCurrent() & KEY_RIGHT)
        {
            f_Editor->view_X(f_Editor->view_X() + inc);
        }
        if (keysCurrent() & KEY_UP)
        {
            f_Editor->view_Y(f_Editor->view_Y() - inc);
        }
        if (keysCurrent() & KEY_DOWN)
        {
            f_Editor->view_Y(f_Editor->view_Y() + inc);
        }
    }
    // VBlank
    swiWaitForVBlank();
    f_Editor->vblank();
    f_TextGFX->vblank();
    // Update backgrounds
    bgUpdate();
}

#pragma endregion