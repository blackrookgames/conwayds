#include "game/scns/menu/Scene.h"

#include <cstdio>
#include <cstring>
#include <iomanip>
#include <nds/debug.h>

#include <__.h>
#include "engine/data/Pattern.h"
#include "engine/data/RLE.h"
#include "engine/helper/ArrayUtil.h"
#include "game/Global.h"
#include "game/assets/MenuMain.h"
#include "game/assets/MenuTitle.h"
#include "game/assets/Palette.h"
#include "game/assets/TextTileset.h"

#include "game/scns/edit/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region helper

namespace game::scns::menu
{
    #pragma region functions

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

    #pragma endregion
}

#pragma endregion


#pragma region init

Scene::Scene()
{
    f_Screen_Main = nullptr;
    f_BScr_TextGFX = nullptr;
    f_BScr_TextStream = nullptr;
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
    videoSetModeSub(MODE_0_2D);
    vramSetBankC(VRAM_C_SUB_BG_0x06200000);
    // Initialize screen data
    loadScreenData(
        ass::MenuMain::data, ass::MenuMain::size,
        f_Screen_Main, f_Screen_Main_Len);
    loadScreenData(
        ass::MenuTitle::data, ass::MenuTitle::size,
        f_Screen_Title, f_Screen_Title_Len);
    // Initialize top screen
    f_TScr = bgInit(0, BgType_Text4bpp, BgSize_T_256x256, 8, 0);
    f_TScr_Map = bgGetMapPtr(f_TScr);
    std::copy(f_Screen_Title, f_Screen_Title + f_Screen_Title_Len, f_TScr_Map);
    // Initialize top screen palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE, assets::Palette::size);
    *BG_PALETTE = 0;
    // Initialize top screen tileset
	DC_FlushRange(assets::TextTileset::data, assets::TextTileset::size);
    dmaCopy(assets::TextTileset::data, bgGetGfxPtr(f_TScr), assets::TextTileset::size);
    // Initialize bottom screen
    f_BScr_TextGFX = new engine::gfx::TextGFX(true, 0, 8, 0, 0);
    f_BScr_TextStream = new std::ostream(f_BScr_TextGFX);
    std::copy(f_Screen_Main, f_Screen_Main + f_Screen_Main_Len, f_BScr_TextGFX->bg_Buffer());
    // Initialize bottom screen palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE_SUB, assets::Palette::size);
    *BG_PALETTE_SUB = 0;
    // Initialize bottom screen tileset
	DC_FlushRange(assets::TextTileset::data, assets::TextTileset::size);
    dmaCopy(assets::TextTileset::data, f_BScr_TextGFX->bg_GFX(), assets::TextTileset::size);
    // Set backdrop colors
    setBackdropColor(RGB15(0, 0, 0));
    setBackdropColorSub(RGB15(0, 0, 0));
    // Turn on screen
    DS_SCREEN_ON
}

void Scene::m_exit()
{
    // Delete
    DELETE_OBJECT(f_BScr_TextStream)
    DELETE_OBJECT(f_BScr_TextGFX)
    DELETE_ARRAY(f_Screen_Title)
    DELETE_ARRAY(f_Screen_Main)
    // Base
    engine::scenes::Scene::m_exit();
}

void Scene::m_update()
{
    engine::scenes::Scene::m_update();
    // Scan input
    touchRead(&f_TouchPos);
    scanKeys();
    u32 inputDown = keysDown();
    if (inputDown & KEY_START)
    {
        // Goto simulation scene
        game::scns::edit::Scene* scene = new game::scns::edit::Scene();
        scene->deleteOnExit(true);
        engine::scenes::gotoScene(scene);
    }
    else
    {
        // Navigate
        if (inputDown & KEY_LEFT)
        {
        }
        if (inputDown & KEY_RIGHT)
        {
        }
        if (inputDown & KEY_UP)
        {
        }
        if (inputDown & KEY_DOWN)
        {
        }
        // Touch
        if (keysHeld() & KEY_TOUCH)
        {
        }
    }
    // VBlank
    swiWaitForVBlank();
    f_BScr_TextGFX->vblank();
    // Update backgrounds
    bgUpdate();
}

#pragma endregion