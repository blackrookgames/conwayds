#include "game/scns/sim/Scene.h"

#include <cstdio>
#include <cstring>
#include <iomanip>
#include <nds/debug.h>

#include <__.h>
#include "engine/data/Pattern.h"
#include "engine/data/RLE.h"
#include "engine/helper/ArrayUtil.h"
#include "game/assets/Palette.h"
#include "game/assets/SimScreen.h"
#include "game/assets/SimScreenPause.h"
#include "game/assets/SimScreenStart.h"
#include "game/assets/SimTileset.h"
#include "game/assets/TextTileset.h"
#include "game/scns/edit/Scene.h"

using namespace game::scns::sim;
namespace ass = game::assets;

#pragma region helper functions

namespace game::scns::sim
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
    f_Simulation = nullptr;
}

Scene::~Scene() { }

#pragma endregion

#pragma region helper const

const engine::helper::RRValue48p16 Scene::f_0 = engine::helper::RRValue48p16(0, 0);
const engine::helper::RRValue48p16 Scene::f_1 = engine::helper::RRValue48p16(1, 0);

const engine::helper::RRValue48p16 Scene::f_Inc_Pos = engine::helper::RRValue48p16(4, 0);
const engine::helper::RRValue48p16 Scene::f_Inc_Zoom = engine::helper::RRValue48p16(5, 0);

#pragma endregion

#pragma region helper functions

void Scene::m_enter()
{
    engine::scenes::Scene::m_enter();
    // Turn off screen
    DS_SCREEN_OFF
    // Initialize pause indicater
    f_Paused = true;
    // Initialize video
	videoSetMode(MODE_2_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);
    videoSetModeSub(MODE_0_2D);
    vramSetBankC(VRAM_C_SUB_BG_0x06200000);
    // Initialize screen data
    loadScreenData(\
        ass::SimScreen::data, ass::SimScreen::size,\
        f_Screen_Main, f_Screen_Main_Len);
    loadScreenData(\
        ass::SimScreenPause::data, ass::SimScreenPause::size,\
        f_Screen_Pause, f_Screen_Pause_Len);
    // Initialize text graphics
    f_TextGFX = new engine::gfx::TextGFX(true, 0, 8, 0, 0);
    f_TextStream = new std::ostream(f_TextGFX);
    {
        u16* screen;
        size_t screen_len;
        loadScreenData(\
            ass::SimScreenStart::data, ass::SimScreenStart::size,\
            screen, screen_len);
        std::copy(screen, screen + screen_len, f_TextGFX->bg_Buffer());
        delete[] screen;
    }
    // Initialize simulation
    f_Simulation = new Simulation(3, 9, 0, 2);
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
    // Delete
    DELETE_OBJECT(f_Simulation)
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
    // Update simulation
    f_Simulation->update(f_Paused ? 0 : delta);
    // Scan input
    touchRead(&f_TouchPos);
    scanKeys();
    u32 inputDown = keysDown();
    if (inputDown & KEY_START)
    {
        if (f_Paused)
        {
            // Unpause
            f_Paused = false;
            // Display normal screen
            std::copy(f_Screen_Main, f_Screen_Main + f_Screen_Main_Len, f_TextGFX->bg_Buffer());
            f_TextGFX->markDirty();
        }
        else
        {
            // Pause
            f_Paused = true;
            // Display pause screen
            std::copy(f_Screen_Pause, f_Screen_Pause + f_Screen_Pause_Len, f_TextGFX->bg_Buffer());
            f_TextGFX->markDirty();
        }
    }
    else
    {
        // Zoom
        if (keysCurrent() & KEY_L)
        {
            f_Simulation->view().cam_Zoom(f_Simulation->view().cam_Zoom() - f_Inc_Zoom);
        }
        if (keysCurrent() & KEY_R)
        {
            f_Simulation->view().cam_Zoom(f_Simulation->view().cam_Zoom() + f_Inc_Zoom);
        }
        // Pan
        if (keysCurrent() & KEY_LEFT)
        {
            f_Simulation->view().cam_X(f_Simulation->view().cam_X() - f_Inc_Pos);
        }
        if (keysCurrent() & KEY_RIGHT)
        {
            f_Simulation->view().cam_X(f_Simulation->view().cam_X() + f_Inc_Pos);
        }
        if (keysCurrent() & KEY_UP)
        {
            f_Simulation->view().cam_Y(f_Simulation->view().cam_Y() + f_Inc_Pos);
        }
        if (keysCurrent() & KEY_DOWN)
        {
            f_Simulation->view().cam_Y(f_Simulation->view().cam_Y() - f_Inc_Pos);
        }
        // Paused
        if (f_Paused)
        {
            // Stop
            if (inputDown & KEY_SELECT)
            {
                game::scns::edit::Scene* scene = new game::scns::edit::Scene();
                scene->deleteOnExit(true);
                engine::scenes::gotoScene(scene);
            }
        }
        // Unpaused
        else
        {
            // Speed
            static constexpr u32 speedStep = 8;
            if (keysDown() & KEY_X)
            {
                f_Simulation->speed(f_Simulation->speed() + speedStep);
            }
            if (keysDown() & KEY_Y)
            {
                if (f_Simulation->speed() < speedStep) f_Simulation->speed(Simulation::speed_Min);
                else f_Simulation->speed(f_Simulation->speed() - speedStep);
            }
            // Touch
            if (keysHeld() & KEY_TOUCH)
            {
                static constexpr u32 speed_x0 = (u32)ass::SimScreen::speed_x0 * 8;
                static constexpr u32 speed_y0 = (u32)ass::SimScreen::speed_y0 * 8;
                static constexpr u32 speed_x1 = (u32)ass::SimScreen::speed_x1 * 8;
                static constexpr u32 speed_y1 = (u32)ass::SimScreen::speed_y1 * 8;
                u32 touch_x = f_TouchPos.px;
                u32 touch_y = f_TouchPos.py;
                // Speed
                if (touch_y >= speed_y0 && touch_y < speed_y1)
                {
                    u32 input = MATH_CLAMP(speed_x0, speed_x1, touch_x);
                    f_Simulation->speed(MATH_SCALE2(speed_x0, speed_x1, Simulation::speed_Min, Simulation::speed_Max, input));
                }
            }
        }
    }
    // Draw stats
    if (!f_Paused)
    {
        // Update text
        f_TextGFX->setCursor(ass::SimScreen::gen_x, ass::SimScreen::gen_y);
        *f_TextStream << STREAM_ALIGN_L(12) << f_Simulation->sim_Gen();
        f_TextStream->flush();
        f_TextGFX->setCursor(ass::SimScreen::live_x, ass::SimScreen::live_y);
        *f_TextStream << STREAM_ALIGN_L(12) << f_Simulation->sim_Live();
        f_TextStream->flush();
        // Update speed bar
        {
            // Compute speed value
            static constexpr u32 ilen = Simulation::speed_Max - Simulation::speed_Min;
            u32 speed = f_Simulation->speed() - Simulation::speed_Min;
            // Compute display value
            static constexpr u8 olen_raw = ass::SimScreen::speed_x1 - ass::SimScreen::speed_x0;
            static constexpr u32 olen = (u32)olen_raw * 8;
            u32 value = (speed * olen) / ilen;
            u32 value_lo = value % 8;
            u32 value_hi = value / 8;
            // Draw value
            u16* optr0 = f_TextGFX->bg_Buffer() + ass::SimScreen::speed_x0 + ass::SimScreen::speed_y0 * 32;
            u16* optr1 = optr0 + 32;
            for (u8 i = 0; i < olen_raw; ++i)
            {
                // Draw tile
                if (i < value_hi) *optr0 = 0x88;
                else if (i > value_hi) *optr0 = 0x80;
                else *optr0 = 0x80 + value_lo;
                *optr1 = *optr0;
                // Next
                ++optr0;
                ++optr1;
            }
        }
        // Mark dirty
        f_TextGFX->markDirty();
    }
    // VBlank
    swiWaitForVBlank();
    f_Simulation->vblank();
    f_TextGFX->vblank();
    // Update backgrounds
    bgUpdate();
}

#pragma endregion