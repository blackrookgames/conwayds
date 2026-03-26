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
#include "game/assets/MenuTitle.h"
#include "game/assets/Palette.h"
#include "game/assets/TextTileset.h"
#include "game/scns/menu/PageMain.h"

#include "game/scns/edit/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region macros

#define PAGE_ENTER \
    /* Enter page */ \
    f_NextPage->m__enter(); \
    /* Set pointer for active page */ \
    f_ActivePage = f_NextPage; \
    /* Reset pointer for next page */ \
    f_NextPage = nullptr;

#define PAGE_EXIT \
    /* Exit page */ \
    f_ActivePage->m__exit(); \
    /* Delete if requested*/ \
    if (f_ActivePage->deleteOnExit()) delete f_ActivePage; \
    /* Reset pointer for active page */ \
    f_ActivePage = nullptr;

#pragma endregion

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
    // Text
    f_TextGFX = nullptr;
    f_TextStream = nullptr;
    // Pages
    f_ActivePage = nullptr;
    f_NextPage = nullptr;
}

Scene::~Scene()
{
    // Text
    DELETE_OBJECT(f_TextGFX)
    DELETE_OBJECT(f_TextStream)
}

#pragma endregion

#pragma region properties

u16 Scene::input_Down() const { return f_Input_Down; }

u16 Scene::input_Held() const { return f_Input_Held; }

bool Scene::input_Touch() const { return f_Input_Touch; }

touchPosition Scene::input_Touch_Pos() const { return f_Input_Touch_Pos; }

const engine::gfx::TextGFX& Scene::textGFX() const { return *f_TextGFX; }
engine::gfx::TextGFX& Scene::textGFX() { return *f_TextGFX; }

const std::ostream& Scene::textStream() const { return *f_TextStream; }
std::ostream& Scene::textStream() { return *f_TextStream; }

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
    loadScreenData(ass::MenuTitle::data, ass::MenuTitle::size, f_Screen_Title, f_Screen_Title_Len);
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
    f_TextGFX = new engine::gfx::TextGFX(true, 0, 8, 0, 0);
    f_TextStream = new std::ostream(f_TextGFX);
    // Initialize bottom screen palette
    DC_FlushRange(assets::Palette::data, assets::Palette::size);
    dmaCopy(assets::Palette::data, BG_PALETTE_SUB, assets::Palette::size);
    *BG_PALETTE_SUB = 0;
    // Initialize bottom screen tileset
	DC_FlushRange(assets::TextTileset::data, assets::TextTileset::size);
    dmaCopy(assets::TextTileset::data, f_TextGFX->bg_GFX(), assets::TextTileset::size);
    // Set backdrop colors
    setBackdropColor(RGB15(0, 0, 0));
    setBackdropColorSub(RGB15(0, 0, 0));
    // Page
    f_NextPage = new PageMain(*this);
    f_NextPage->deleteOnExit(true);
    // Turn on screen
    DS_SCREEN_ON
}

void Scene::m_exit()
{
    // Exit active page
    if (f_ActivePage) { PAGE_EXIT }
    // Delete
    DELETE_ARRAY(f_Screen_Title)
    // Base
    engine::scenes::Scene::m_exit();
}

void Scene::m_update()
{
    engine::scenes::Scene::m_update();
    // Switch pages (if requested)
    if (f_NextPage)
    {
        // Exit active page
        if (f_ActivePage) { PAGE_EXIT }
        // Enter next page
        PAGE_ENTER
    }
    // Scan input
    scanKeys();
    f_Input_Down = keysDown();
    f_Input_Held = keysHeld();
    f_Input_Touch = touchRead(&f_Input_Touch_Pos);
    // Update page
    if (f_ActivePage) f_ActivePage->m__update();
    // VBlank
    swiWaitForVBlank();
    if (f_ActivePage) f_ActivePage->m__vblank();
    f_TextGFX->vblank();
    // Update backgrounds
    bgUpdate();
}

#pragma endregion

#pragma region methods

void Scene::gotoPage(Page* page)
{
    f_NextPage = page;
}

#pragma endregion