#include "game/scns/edit/Scene.h"

#include <cstdio>
#include <cstring>
#include <iomanip>
#include <nds/debug.h>

#include <__.h>
#include "engine/data/Pattern.h"
#include "engine/data/RLE.h"
#include "engine/helper/ArrayUtil.h"
#include "game/assets/EditScreen.h"
#include "game/assets/EditTileset.h"
#include "game/assets/Palette.h"
#include "game/assets/TextTileset.h"

#include "game/scns/sim/Scene.h"

using namespace game::scns::edit;
namespace ass = game::assets;

#pragma region helper

namespace game::scns::edit
{
    #pragma region const

    static const std::string tool_Draw(
        "   DRAW MODE");
    static const std::string tool_Erase(
        "  ERASE MODE");

    #pragma endregion

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
    f_TextGFX = nullptr;
    f_TextStream = nullptr;
    f_Editor = nullptr;
}

Scene::~Scene() { }

#pragma endregion

#pragma region helper const

const engine::helper::RRValue48p16 Scene::f_0 = engine::helper::RRValue48p16(0, 0);
const engine::helper::RRValue48p16 Scene::f_1 = engine::helper::RRValue48p16(1, 0);

const engine::helper::RRValue48p16 Scene::f_Inc_Pos = engine::helper::RRValue48p16(4, 0);
const engine::helper::RRValue48p16 Scene::f_Inc_Zoom = engine::helper::RRValue48p16(5, 0);

const engine::helper::RRValue48p16 Scene::f_DS_Width = engine::helper::RRValue48p16(256, 0);
const engine::helper::RRValue48p16 Scene::f_DS_Height = engine::helper::RRValue48p16(192, 0);

const engine::helper::RRValue48p16 Scene::f_Pattern_Cols = engine::helper::RRValue48p16(254, 0);
const engine::helper::RRValue48p16 Scene::f_Pattern_Rows = engine::helper::RRValue48p16(254, 0);
const engine::helper::RRValue48p16 Scene::f_Pattern_Last_Col = f_Pattern_Cols - f_1;
const engine::helper::RRValue48p16 Scene::f_Pattern_Last_Row = f_Pattern_Rows - f_1;

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
        ass::EditScreen::data, ass::EditScreen::size,\
        f_Screen_Main, f_Screen_Main_Len);
    // Initialize text graphics
    f_TextGFX = new engine::gfx::TextGFX(false, 0, 8, 0, 0);
    f_TextStream = new std::ostream(f_TextGFX);
    std::copy(f_Screen_Main, f_Screen_Main + f_Screen_Main_Len, f_TextGFX->bg_Buffer());
    // Initialize simulation
    f_Editor = new Editor(3, 9, 0, 2);
    // Tool
    f_Tool = Tool::DRAW;
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
    // Post-init
    m_Refresh_ToolDisplay();
    // Start timer
    timerStart(0, ClockDivider_1024, 0, nullptr);
    // Set backdrop colors
    setBackdropColor(RGB15(0, 0, 0));
    setBackdropColorSub(RGB15(0, 0, 16));
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
    u32 inputDown = keysDown();
    if (inputDown & KEY_START)
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
        // Switch tool
        if (inputDown & KEY_X)
        {
            f_Tool = static_cast<Tool>((static_cast<u8>(f_Tool) + 1) % toolCount);
            m_Refresh_ToolDisplay();
        }
        // Toggle grid
        if (inputDown & KEY_Y)
        {
            f_Editor->grid(!f_Editor->grid());
        }
        // Zoom
        if (keysCurrent() & KEY_L)
        {
            f_Editor->view_Zoom(f_Editor->view_Zoom() - f_Inc_Zoom);
        }
        if (keysCurrent() & KEY_R)
        {
            f_Editor->view_Zoom(f_Editor->view_Zoom() + f_Inc_Zoom);
        }
        // Pan
        if (keysCurrent() & KEY_LEFT)
        {
            f_Editor->view_X(f_Editor->view_X() - f_Inc_Pos);
        }
        if (keysCurrent() & KEY_RIGHT)
        {
            f_Editor->view_X(f_Editor->view_X() + f_Inc_Pos);
        }
        if (keysCurrent() & KEY_UP)
        {
            f_Editor->view_Y(f_Editor->view_Y() + f_Inc_Pos);
        }
        if (keysCurrent() & KEY_DOWN)
        {
            f_Editor->view_Y(f_Editor->view_Y() - f_Inc_Pos);
        }
        // Touch
        if (keysHeld() & KEY_TOUCH)
        {
            engine::helper::RRValue48p16 tx((s64)f_TouchPos.px, 0);
            engine::helper::RRValue48p16 ty((s64)f_TouchPos.py, 0);
            // Determine X-coordinate of cell
            engine::helper::RRValue48p16 cell_x = MATH_SCALE2(
                f_0, f_DS_Width, 
                f_Editor->view().cam_X0(), f_Editor->view().cam_X1(), 
                tx);
            cell_x = MATH_SCALE2(
                Editor::bound_X0, Editor::bound_X1,
                f_0, f_Pattern_Cols,
                cell_x);
            cell_x = MATH_CLAMP(f_0, f_Pattern_Last_Col, cell_x);
            // Determine Y-coordinate of cell
            engine::helper::RRValue48p16 cell_y = MATH_SCALE2(
                f_DS_Height, f_0, 
                f_Editor->view().cam_Y0(), f_Editor->view().cam_Y1(), 
                ty);
            cell_y = MATH_SCALE2(
                Editor::bound_Y1, Editor::bound_Y0,
                f_0, f_Pattern_Rows,
                cell_y);
            cell_y = MATH_CLAMP(f_0, f_Pattern_Last_Row, cell_y);
            // Use tool
            switch (f_Tool)
            {
                case Tool::DRAW:
                    f_Editor->setcell((u16)cell_x.floorToWhole(), (u16)cell_y.floorToWhole(), true);
                    break;
                case Tool::ERASE:
                    f_Editor->setcell((u16)cell_x.floorToWhole(), (u16)cell_y.floorToWhole(), false);
                    break;
            }
        }
    }
    // Draw stats
    {
        // Live cells
        f_TextGFX->setCursor(ass::EditScreen::live_x, ass::EditScreen::live_y);
        *f_TextStream << STREAM_ALIGN_L(12) << f_Editor->numLive();
        f_TextStream->flush();
        // X-coordinate
        f_TextGFX->setCursor(ass::EditScreen::coordx_x, ass::EditScreen::coordx_y);
        *f_TextStream << STREAM_ALIGN_L(12) << f_Editor->view_X().toStr(2);
        f_TextStream->flush();
        // X-coordinate
        f_TextGFX->setCursor(ass::EditScreen::coordy_x, ass::EditScreen::coordy_y);
        *f_TextStream << STREAM_ALIGN_L(12) << f_Editor->view_Y().toStr(2);
        f_TextStream->flush();
        // Zoom
        STREAM_STRING(zoomStr, f_Editor->view_Zoom().toStr(1) << "%")
        f_TextGFX->setCursor(ass::EditScreen::zoom_x, ass::EditScreen::zoom_y);
        *f_TextStream << STREAM_ALIGN_L(12) << zoomStr.str();
        f_TextStream->flush();
        // Mark dirty
        f_TextGFX->markDirty();
    }
    // VBlank
    swiWaitForVBlank();
    f_Editor->vblank();
    f_TextGFX->vblank();
    // Update backgrounds
    bgUpdate();
}

void Scene::m_Refresh_ToolDisplay()
{
    const std::string* str = nullptr;
    switch (f_Tool)
    {
        case Tool::DRAW: str = &tool_Draw; break;
        case Tool::ERASE: str = &tool_Erase; break;
    } 
    f_TextGFX->setCursor(ass::EditScreen::tool_x - str->length(), ass::EditScreen::tool_y);
    *f_TextStream << *str; f_TextStream->flush();
    f_TextGFX->markDirty();
}

#pragma endregion