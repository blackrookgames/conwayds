#include "game/scns/menu/PageRandom.h"

#include "game/Global.h"
#include "game/assets/MenuRandom.h"
#include "game/scns/menu/Scene.h"
#include "engine/data/RLE.h"

#include "game/scns/edit/Scene.h"

#include <cstdlib>

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region helper

namespace game::scns::menu
{
    #pragma region functions

    void loadScreenData4(const u16* in_data, size_t in_len, u16*& out_data, size_t& out_len)
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

PageRandom::PageRandom(Scene& scene, std::string msg, ButtonAction yes, ButtonAction no) : Page(scene)
{
    f_Screen = nullptr;
    f_Msg = std::move(msg);
    f_Yes = yes;
    f_No = no;
}

PageRandom::~PageRandom()
{
    DELETE_ARRAY(f_Screen)
}

#pragma endregion

#pragma region helper functions

void PageRandom::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    loadScreenData4(ass::MenuRandom::data, ass::MenuRandom::size, f_Screen, f_Screen_Len);
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Initialize index
    f_Sel_Index = 1; // Select No by default
    f_Sel_Touch = 0xFFFF;
    f_Sel_Touching = false;
    // Post-init
    m_Refresh_Msg();
    m_Refresh_Buttons();
}

void PageRandom::m_exit()
{
    // Call base
    Page::m_exit();
}

void PageRandom::m_update()
{
    Page::m_update();
    // Get touch
    if (scene().input_Touch())
    {
        s16 touch_X = ((s16)(scene().input_Touch_Pos().px / 8) - (s16)ass::MenuRandom::button_x) / (s16)ass::MenuRandom::button_w;
        s16 touch_Y = ((s16)(scene().input_Touch_Pos().py / 8) - (s16)ass::MenuRandom::button_y) / (s16)ass::MenuRandom::button_h;
        f_Sel_Touch = (touch_X < 0 || touch_Y < 0 || touch_X >= ass::MenuRandom::columns) ? 
            0xFFFF : (touch_X + touch_Y * ass::MenuRandom::columns);
    }
    // Get input
    if (scene().input_Down() & KEY_A)
    {
        m_Button_Action();
    }
    else if (scene().input_Down() & KEY_B)
    {
        f_No(scene());
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
        if ((f_Sel_Index + 1) < ass::MenuRandom::buttons)
        {
            ++f_Sel_Index;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_UP)
    {
        if (f_Sel_Index >= ass::MenuRandom::columns)
        {
            f_Sel_Index -= ass::MenuRandom::columns;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_DOWN)
    {
        if ((f_Sel_Index + ass::MenuRandom::columns) < ass::MenuRandom::buttons)
        {
            f_Sel_Index += ass::MenuRandom::columns;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_TOUCH)
    {
        if (f_Sel_Touch < ass::MenuRandom::buttons)
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

void PageRandom::m_vblank()
{
    Page::m_vblank();
}

void PageRandom::m_Print_Text(u16& x, u16& y, const char* beg, const char* end, char endChar)
{
    u16 len = end - beg;
    end = beg + len; // Fix end in case an overflow occurs
    // Newline needed?
    if ((x + len) > ass::MenuRandom::msg_w) { x = 0; ++y; }
    // Make sure there's room
    u16 i = x + y * ass::MenuRandom::msg_w;
    if (i >= (ass::MenuRandom::msg_w * ass::MenuRandom::msg_h)) return;
    // Draw text
    if (len <= ass::MenuRandom::msg_w)
    {
        u16* optr = scene().textGFX().bg_Buffer() + (ass::MenuRandom::msg_x + x) + (ass::MenuRandom::msg_y + y) * DS_SCREEN_COLS;
        while (beg < end) { *(optr++) = *(beg++); ++x; }
    }
    else
    {
        u16* optr = scene().textGFX().bg_Buffer() + (ass::MenuRandom::msg_x + x) + (ass::MenuRandom::msg_y + y) * DS_SCREEN_COLS;
        while (beg < end)
        {
            // Newline?
            if (x >= ass::MenuRandom::msg_w)
            {
                x = 0; ++y;
                optr = scene().textGFX().bg_Buffer() + (ass::MenuRandom::msg_x + x) + (ass::MenuRandom::msg_y + y) * DS_SCREEN_COLS;
            }
            // No more room?
            if (y >= ass::MenuRandom::msg_h) return;
            // Draw character
            if ((x + 1) == ass::MenuRandom::msg_w && (beg + 1) != end)
                *(optr++) = '-';
            else
                *(optr++) = *(beg++);
            // Next
            ++x;
        }
    }
    // Draw end character
    if (x < ass::MenuRandom::msg_w)
    {
        u16* optr = scene().textGFX().bg_Buffer() + (ass::MenuRandom::msg_x + x) + (ass::MenuRandom::msg_y + y) * DS_SCREEN_COLS;
        if (endChar == '\n') { x = 0; ++y; }
        else if (endChar >= 0x20) { *optr = endChar; ++x; }
        else { *optr = 0x00; ++x; }
    }
}

void PageRandom::m_Button_Action()
{
    switch (f_Sel_Index)
    {
        // Yes
        case 0: f_Yes(scene()); break;
        // No
        case 1: f_No(scene()); break;
    }
}

void PageRandom::m_Refresh_Msg()
{
    // Reset button tiles
    std::copy(f_Screen, f_Screen + ass::MenuRandom::button_y * DS_SCREEN_COLS, scene().textGFX().bg_Buffer());
    // Print text
    const char* beg = f_Msg.c_str();
    const char* end = f_Msg.c_str() + f_Msg.length();
    u16 x = 0;
    u16 y = 0;
    while (beg < end)
    {
        const char* ptr = beg;
        while (ptr < end)
        {
            if (*ptr <= 0x20) break;
            ++ptr;
        }
        m_Print_Text(x, y, beg, ptr, (ptr >= end) ? 0x00 : *ptr);
        beg = ptr + 1;
    }
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageRandom::m_Refresh_Buttons()
{
    // Reset button tiles
    u16 offset = ass::MenuRandom::button_y * DS_SCREEN_COLS;
    std::copy(f_Screen + offset, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer() + offset);
    // Highlight selected
    u16 index_x = f_Sel_Index % ass::MenuRandom::columns;
    u16 index_y = f_Sel_Index / ass::MenuRandom::columns;
    u16 off = ass::MenuRandom::button_x + ass::MenuRandom::button_w * index_x + 
        (ass::MenuRandom::button_y + ass::MenuRandom::button_h * index_y) * DS_SCREEN_COLS;
    u16 highlight = (f_Sel_Touching ? 0x2 : 0x1) << 12;
    for (u16 y = 0; y < ass::MenuRandom::button_h; ++y)
    {
        u16 i = off + y * DS_SCREEN_COLS;
        for (u16 x = 0; x < ass::MenuRandom::button_w; ++x)
            scene().textGFX().bg_Buffer()[i + x] |= highlight;
    }
    // Mark dirty
    scene().textGFX().markDirty();
}

#pragma endregion