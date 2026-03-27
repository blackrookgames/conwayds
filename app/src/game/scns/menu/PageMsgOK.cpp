#include "game/scns/menu/PageMsgOK.h"

#include "game/Global.h"
#include "game/ScreenUtil.h"
#include "game/assets/MenuMsgOK.h"
#include "game/scns/menu/Scene.h"
#include "engine/data/RLE.h"

#include "game/scns/edit/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region init

PageMsgOK::PageMsgOK(Scene& scene, std::string msg, ButtonAction action) : Page(scene)
{
    f_Screen = nullptr;
    f_Msg = std::move(msg);
    f_Action = action;
}

PageMsgOK::~PageMsgOK()
{
    DELETE_ARRAY(f_Screen)
}

#pragma endregion

#pragma region helper functions

void PageMsgOK::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    ScreenUtil::load(ass::MenuMsgOK::data, ass::MenuMsgOK::size, f_Screen, f_Screen_Len);
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Initialize index
    f_Sel_Index = 0;
    f_Sel_Touch = 0xFFFF;
    f_Sel_Touching = false;
    // Post-init
    m_Refresh_Msg();
    m_Refresh_Buttons();
}

void PageMsgOK::m_exit()
{
    // Call base
    Page::m_exit();
}

void PageMsgOK::m_update()
{
    Page::m_update();
    // Get touch
    if (scene().input_Touch())
    {
        s16 touch_X = ((s16)(scene().input_Touch_Pos().px / 8) - (s16)ass::MenuMsgOK::button_x) / (s16)ass::MenuMsgOK::button_w;
        s16 touch_Y = ((s16)(scene().input_Touch_Pos().py / 8) - (s16)ass::MenuMsgOK::button_y) / (s16)ass::MenuMsgOK::button_h;
        f_Sel_Touch = (touch_X < 0 || touch_Y < 0 || touch_X >= ass::MenuMsgOK::columns) ? 
            0xFFFF : (touch_X + touch_Y * ass::MenuMsgOK::columns);
    }
    // Get input
    if (scene().input_Down() & KEY_A)
    {
        f_Action(scene());
    }
    else if (scene().input_Down() & KEY_B)
    {
        f_Action(scene());
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
        if ((f_Sel_Index + 1) < ass::MenuMsgOK::buttons)
        {
            ++f_Sel_Index;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_UP)
    {
        if (f_Sel_Index >= ass::MenuMsgOK::columns)
        {
            f_Sel_Index -= ass::MenuMsgOK::columns;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_DOWN)
    {
        if ((f_Sel_Index + ass::MenuMsgOK::columns) < ass::MenuMsgOK::buttons)
        {
            f_Sel_Index += ass::MenuMsgOK::columns;
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_TOUCH)
    {
        if (f_Sel_Touch < ass::MenuMsgOK::buttons)
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
            f_Action(scene());
        }
        else
        {
            f_Sel_Touching = false;
            m_Refresh_Buttons();
        }
    }
}

void PageMsgOK::m_vblank()
{
    Page::m_vblank();
}

void PageMsgOK::m_Print_Text(u16& x, u16& y, const char* beg, const char* end, char endChar)
{
    u16 len = end - beg;
    end = beg + len; // Fix end in case an overflow occurs
    // Newline needed?
    if ((x + len) > ass::MenuMsgOK::msg_w) { x = 0; ++y; }
    // Make sure there's room
    u16 i = x + y * ass::MenuMsgOK::msg_w;
    if (i >= (ass::MenuMsgOK::msg_w * ass::MenuMsgOK::msg_h)) return;
    // Draw text
    if (len <= ass::MenuMsgOK::msg_w)
    {
        u16* optr = scene().textGFX().bg_Buffer() + (ass::MenuMsgOK::msg_x + x) + (ass::MenuMsgOK::msg_y + y) * DS_SCREEN_COLS;
        while (beg < end) { *(optr++) = *(beg++); ++x; }
    }
    else
    {
        u16* optr = scene().textGFX().bg_Buffer() + (ass::MenuMsgOK::msg_x + x) + (ass::MenuMsgOK::msg_y + y) * DS_SCREEN_COLS;
        while (beg < end)
        {
            // Newline?
            if (x >= ass::MenuMsgOK::msg_w)
            {
                x = 0; ++y;
                optr = scene().textGFX().bg_Buffer() + (ass::MenuMsgOK::msg_x + x) + (ass::MenuMsgOK::msg_y + y) * DS_SCREEN_COLS;
            }
            // No more room?
            if (y >= ass::MenuMsgOK::msg_h) return;
            // Draw character
            if ((x + 1) == ass::MenuMsgOK::msg_w && (beg + 1) != end)
                *(optr++) = '-';
            else
                *(optr++) = *(beg++);
            // Next
            ++x;
        }
    }
    // Draw end character
    if (x < ass::MenuMsgOK::msg_w)
    {
        u16* optr = scene().textGFX().bg_Buffer() + (ass::MenuMsgOK::msg_x + x) + (ass::MenuMsgOK::msg_y + y) * DS_SCREEN_COLS;
        if (endChar == '\n') { x = 0; ++y; }
        else if (endChar >= 0x20) { *optr = endChar; ++x; }
        else { *optr = 0x00; ++x; }
    }
}

void PageMsgOK::m_Refresh_Msg()
{
    // Reset button tiles
    std::copy(f_Screen, f_Screen + ass::MenuMsgOK::button_y * DS_SCREEN_COLS, scene().textGFX().bg_Buffer());
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

void PageMsgOK::m_Refresh_Buttons()
{
    // Reset button tiles
    u16 offset = ass::MenuMsgOK::button_y * DS_SCREEN_COLS;
    std::copy(f_Screen + offset, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer() + offset);
    // Highlight selected
    u16 index_x = f_Sel_Index % ass::MenuMsgOK::columns;
    u16 index_y = f_Sel_Index / ass::MenuMsgOK::columns;
    u16 off = ass::MenuMsgOK::button_x + ass::MenuMsgOK::button_w * index_x + 
        (ass::MenuMsgOK::button_y + ass::MenuMsgOK::button_h * index_y) * DS_SCREEN_COLS;
    u16 highlight = (f_Sel_Touching ? 0x2 : 0x1) << 12;
    for (u16 y = 0; y < ass::MenuMsgOK::button_h; ++y)
    {
        u16 i = off + y * DS_SCREEN_COLS;
        for (u16 x = 0; x < ass::MenuMsgOK::button_w; ++x)
            scene().textGFX().bg_Buffer()[i + x] |= highlight;
    }
    // Mark dirty
    scene().textGFX().markDirty();
}

#pragma endregion