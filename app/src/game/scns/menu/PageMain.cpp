#include "game/scns/menu/PageMain.h"

#include "game/Global.h"
#include "game/assets/MenuMain.h"
#include "game/scns/menu/Scene.h"
#include "game/scns/menu/PageMsgYN.h"
#include "engine/data/RLE.h"

#include "game/scns/edit/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region helper

namespace game::scns::menu
{
    #pragma region functions

    void loadScreenData2(const u16* in_data, size_t in_len, u16*& out_data, size_t& out_len)
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

PageMain::PageMain(Scene& scene) : Page(scene)
{
    f_Screen = nullptr;
}

PageMain::~PageMain()
{
    DELETE_ARRAY(f_Screen)
}

#pragma endregion

#pragma region helper functions

void PageMain::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    loadScreenData2(ass::MenuMain::data, ass::MenuMain::size, f_Screen, f_Screen_Len);
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Initialize index
    f_Sel_Index = Global::menu_Main_Index();
    f_Sel_Touch = 0xFFFF;
    f_Sel_Touching = false;
    // Post-init
    m_Refresh_Buttons();
}

void PageMain::m_exit()
{
    // Persist selected index
    Global::menu_Main_Index(f_Sel_Index);
    // Call base
    Page::m_exit();
}

void PageMain::m_update()
{
    Page::m_update();
    // Get input
    if (scene().input_Touch())
    {
        s16 touch_X = ((s16)(scene().input_Touch_Pos().px / 8) - (s16)ass::MenuMain::button_x) / (s16)ass::MenuMain::button_w;
        s16 touch_Y = ((s16)(scene().input_Touch_Pos().py / 8) - (s16)ass::MenuMain::button_y) / (s16)ass::MenuMain::button_h;
        f_Sel_Touch = (touch_X < 0 || touch_Y < 0 || touch_X >= ass::MenuMain::columns) ? 
            0xFFFF : (touch_X + touch_Y * ass::MenuMain::columns);
    }
    if (scene().input_Down() & KEY_START)
    {
        m_Close();
    }
    else if (scene().input_Down() & KEY_A)
    {
        m_Button_Action();
    }
    else if (scene().input_Down() & KEY_B)
    {
        m_Close();
    }
    else if (scene().input_Down() & KEY_LEFT)
    {
        if (f_Sel_Index > 0)
        {
            --f_Sel_Index;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_RIGHT)
    {
        if ((f_Sel_Index + 1) < ass::MenuMain::buttons)
        {
            ++f_Sel_Index;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_UP)
    {
        if (f_Sel_Index >= ass::MenuMain::columns)
        {
            f_Sel_Index -= ass::MenuMain::columns;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_DOWN)
    {
        if ((f_Sel_Index + ass::MenuMain::columns) < ass::MenuMain::buttons)
        {
            f_Sel_Index += ass::MenuMain::columns;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_TOUCH)
    {
        if (f_Sel_Touch < ass::MenuMain::buttons)
        {
            f_Sel_Index = f_Sel_Touch;
            f_Sel_Touching = true;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Up() & KEY_TOUCH)
    {
        if (f_Sel_Touch == f_Sel_Index)
        {
            m_Button_Action();
        }
        else
        {
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
}

void PageMain::m_vblank()
{
    Page::m_vblank();
}

void PageMain::m_Close()
{
    // Reset selected index
    f_Sel_Index = 0;
    // Goto edit scene
    game::scns::edit::Scene* scene = new game::scns::edit::Scene();
    scene->deleteOnExit(true);
    engine::scenes::gotoScene(scene);
}

void PageMain::m_Button_Action()
{
    switch (f_Sel_Index)
    {
        // Load
        case 0:
            m_Close(); // TODO: Change
            break;
        // Save
        case 1:
            m_Close(); // TODO: Change
            break;
        // Clear
        case 2:
            {
                PageMsgYN* page = new PageMsgYN(scene(),
                    "The current pattern will be cleared. Is this OK?",
                    m_Msg_Clear, m_Msg_No);
                page->deleteOnExit(true);
                scene().gotoPage(page);
            }
            break;
        // Random
        case 3:
            m_Close(); // TODO: Change
            break;
        // About
        case 4:
            m_Close(); // TODO: Change
            break;
        // Close
        case 5:
            m_Close();
            break;
    }
}

void PageMain::m_Refresh_Buttons()
{
    // Reset all tiles
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Highlight selected
    u16 index_x = f_Sel_Index % ass::MenuMain::columns;
    u16 index_y = f_Sel_Index / ass::MenuMain::columns;
    u16 off = ass::MenuMain::button_x + ass::MenuMain::button_w * index_x + 
        (ass::MenuMain::button_y + ass::MenuMain::button_h * index_y) * DS_SCREEN_COLS;
    u16 highlight = (f_Sel_Touching ? 0x2 : 0x1) << 12;
    for (u16 y = 0; y < ass::MenuMain::button_h; ++y)
    {
        u16 i = off + y * DS_SCREEN_COLS;
        for (u16 x = 0; x < ass::MenuMain::button_w; ++x)
            scene().textGFX().bg_Buffer()[i + x] |= highlight;
    }
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageMain::m_Msg_No(Scene& scene)
{
    PageMain* page = new PageMain(scene);
    page->deleteOnExit(true);
    scene.gotoPage(page);
}

void PageMain::m_Msg_Clear(Scene& scene)
{
    // Clear pattern
    std::fill(Global::pattern()->cells(), Global::pattern()->cells() + PATTERN_AREA, false);
    // Reset selected index
    Global::menu_Main_Index(0);
    // Goto edit scene
    game::scns::edit::Scene* editScene = new game::scns::edit::Scene();
    editScene->deleteOnExit(true);
    engine::scenes::gotoScene(editScene);
}

#pragma endregion