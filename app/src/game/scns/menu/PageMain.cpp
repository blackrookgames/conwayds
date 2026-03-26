#include "game/scns/menu/PageMain.h"

#include "game/assets/MenuMain.h"
#include "game/scns/menu/Scene.h"
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
    f_Screen_Main = nullptr;
}

PageMain::~PageMain()
{
    DELETE_ARRAY(f_Screen_Main)
}

#pragma endregion

#pragma region helper functions

void PageMain::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    loadScreenData2(ass::MenuMain::data, ass::MenuMain::size, f_Screen_Main, f_Screen_Main_Len);
    std::copy(f_Screen_Main, f_Screen_Main + f_Screen_Main_Len, scene().textGFX().bg_Buffer());
}

void PageMain::m_exit()
{
    Page::m_exit();
}

void PageMain::m_update()
{
    Page::m_update();
    // Get input
    if (scene().input_Down() & KEY_START)
    {
        // Goto simulation scene
        game::scns::edit::Scene* scene = new game::scns::edit::Scene();
        scene->deleteOnExit(true);
        engine::scenes::gotoScene(scene);
    }
    else if (scene().input_Down() & KEY_LEFT)
    {
    }
    else if (scene().input_Down() & KEY_RIGHT)
    {
    }
    else if (scene().input_Down() & KEY_UP)
    {
    }
    else if (scene().input_Down() & KEY_DOWN)
    {
    }
    // Touch
    else if (scene().input_Touch())
    {
    }
}

void PageMain::m_vblank()
{
    Page::m_vblank();
}

#pragma endregion