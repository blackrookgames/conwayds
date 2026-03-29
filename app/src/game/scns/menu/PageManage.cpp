#include "game/scns/menu/PageManage.h"

#include <sstream>

#include "game/FileUtil.h"
#include "game/Global.h"
#include "game/ScreenUtil.h"
#include "game/assets/MenuManage.h"
#include "game/scns/menu/PageMain.h"
#include "game/scns/menu/PageMsgOK.h"
#include "game/scns/menu/PageMsgYN.h"
#include "game/scns/menu/Scene.h"
#include "engine/data/RLE.h"
#include "engine/helper/StrUtil.h"

#include "game/scns/edit/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region init

PageManage::PageManage(Scene& scene, u16 initialIndex) : Page(scene)
{
    f_InitialIndex = initialIndex;
    f_Screen = nullptr;
    f_List = nullptr;
}

PageManage::~PageManage()
{
    DELETE_ARRAY(f_List)
    DELETE_ARRAY(f_Screen)
}

#pragma endregion

#pragma region fields

engine::io::Path PageManage::f_Chosen = engine::io::Path();
u16 PageManage::f_Chosen_Index = 0;

#pragma endregion

#pragma region helper functions

void PageManage::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    ScreenUtil::load(ass::MenuManage::data, ass::MenuManage::size, f_Screen, f_Screen_Len);
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Initialize button index
    f_But_Index = 0;
    f_But_Touch = 0xFFFF;
    f_But_Touch_Down = 0xFFFF;
    f_But_Touching = false;
    // Initialize list
    FileUtil::getPatterns(f_List, f_List_Count, false);
    f_List_Index = (f_List_Count > 0) ? MATH_MIN(f_List_Count - 1, f_InitialIndex) : 0xFFFF;
    f_List_Offset = 0;
    // Post-init
    m_Refresh_List();
    m_Refresh_Buttons();
}

void PageManage::m_exit()
{
    // Call base
    Page::m_exit();
}

void PageManage::m_update()
{
    Page::m_update();
    // Get touch
    if (scene().input_Touch())
    {
        f_But_Touch = 0xFFFF;
        u16 touch_X = scene().input_Touch_Pos().px;
        u16 touch_Y = scene().input_Touch_Pos().py;
        for (u16 i = 0; i < ass::MenuManage::buttons_count; ++i)
        {
            auto button = ass::MenuManage::buttons[i];
            if (touch_X < button.x0) continue;
            if (touch_Y < button.y0) continue;
            if (touch_X >= button.x1) continue;
            if (touch_Y >= button.y1) continue;
            f_But_Touch = i; break;
        }
    }
    // Get input
    if (scene().input_Down() & KEY_A)
    {
        m_Button_Action(f_But_Index);
    }
    else if (scene().input_Down() & KEY_B)
    {
        m_Cancel();
    }
    else if (scene().input_Down() & KEY_LEFT)
    {
        if (f_But_Index > 0)
        {
            --f_But_Index;
            f_But_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Down() & KEY_RIGHT)
    {
        if ((f_But_Index + 1) < ass::MenuManage::buttons_touch)
        {
            ++f_But_Index;
            f_But_Touching = false;
            m_Refresh_Buttons();
        }
    }
    else if (scene().input_Repeat() & KEY_UP)
    {
        m_Nav_Up();
    }
    else if (scene().input_Repeat() & KEY_DOWN)
    {
        m_Nav_Down();
    }
    else if (scene().input_Down() & KEY_TOUCH)
    {
        if (f_But_Touch < ass::MenuManage::buttons_count)
        {
            if (f_But_Touch < ass::MenuManage::buttons_touch)
                f_But_Index = f_But_Touch;
            f_But_Touch_Down = f_But_Touch;
            f_But_Touching = true;
            m_Refresh_Buttons();
        }
        else
        {
            u16 x = scene().input_Touch_Pos().px / 8;
            u16 y = scene().input_Touch_Pos().py / 8;
            if (x >= ass::MenuManage::list_x && y >= ass::MenuManage::list_y)
            {
                x -= ass::MenuManage::list_x; y -= ass::MenuManage::list_y;
                if (x < ass::MenuManage::list_w && y < ass::MenuManage::list_h)
                {
                    u16 index = f_List_Offset + y;
                    if (index < f_List_Count)
                    {
                        f_List_Index = index;
                        m_Refresh_List();
                    }
                }
            }
        }
    }
    else if (scene().input_Up() & KEY_TOUCH)
    {
        if (f_But_Touching && f_But_Touch == f_But_Touch_Down)
            m_Button_Action(f_But_Touch);
        f_But_Touch_Down = 0xFFFF;
        f_But_Touching = false;
        m_Refresh_Buttons();
    }
}

void PageManage::m_vblank()
{
    Page::m_vblank();
}

void PageManage::m_Button_Action(u16 index)
{
    switch (index)
    {
        case 0: m_OK(); break;
        case 1: m_Cancel(); break;
        case 2: m_Nav_Up(); break;
        case 3: m_Nav_Down(); break;
    }
}

void PageManage::m_Refresh_List()
{
    u16 chr;
    u16 pos;
    // Fix offset
    if (f_List_Offset > f_List_Index)
        f_List_Offset = f_List_Index;
    if ((f_List_Offset + ass::MenuManage::list_h) <= f_List_Index)
        f_List_Offset = f_List_Index - (ass::MenuManage::list_h - 1);
    if (f_List_Offset < 0)
        f_List_Offset = 0;
    // Draw list
    u16* off = scene().textGFX().bg_Buffer() + ass::MenuManage::list_x + ass::MenuManage::list_y * DS_SCREEN_COLS;
    for (u16 y = 0; y < ass::MenuManage::list_h; ++y)
    {
        u16 index = f_List_Offset + y;
        u16* row = off;
        u16 x = 0;
        // Determine color
        u16 color = ((f_List_Index == index) ? 0x04 : 0) << 12;
        // Item
        if (index < f_List_Count)
        {
            const engine::io::Path& item = f_List[index];
            while (x < ass::MenuManage::list_w)
            {
                if (x >= item.displayName().length()) break;
                *row = color | item.displayName()[x];
                ++row; ++x;
            }
        }
        // Padding
        while (x < ass::MenuManage::list_w)
        {
            *row = 0x00;
            ++row; ++x;
        }
        // Next
        off += DS_SCREEN_COLS;
    }
    // Draw up arrow
    pos = ass::MenuManage::list_u_x + ass::MenuManage::list_u_y * DS_SCREEN_COLS;
    if (f_List_Index != 0xFFFF && f_List_Offset > 0) chr = f_Screen[pos]; else chr = 0x00;
    scene().textGFX().bg_Buffer()[pos] = chr;
    // Draw down arrow
    pos = ass::MenuManage::list_d_x + ass::MenuManage::list_d_y * DS_SCREEN_COLS;
    if ((f_List_Offset + ass::MenuManage::list_h) < f_List_Count) chr = f_Screen[pos]; else chr = 0x00;
    scene().textGFX().bg_Buffer()[pos] = chr;
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageManage::m_Refresh_Buttons()
{
    static constexpr u16 mask = (1 << 12) - 1;
    // Set button colors
    for (u16 i = 0; i < ass::MenuManage::buttons_count; ++i)
    {
        auto button = ass::MenuManage::buttons[i];
        // Determine color
        u16 color = ((f_But_Touching && f_But_Touch_Down == i) ? 0x2 : ((f_But_Index == i) ? 0x1 : 0x0)) << 12;
        // Draw button
        u16* beg = scene().textGFX().bg_Buffer() + button.x + button.y * DS_SCREEN_COLS;
        for (u16 y = 0; y < button.h; ++y)
        {
            u16* ptr = beg;
            for (u16 x = 0; x < button.w; ++x)
            {
                *ptr &= mask; *ptr |= color; ++ptr;
            }
            beg += DS_SCREEN_COLS;
        }
    }
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageManage::m_OK()
{
    if (f_List_Index < f_List_Count)
    {
        f_Chosen = f_List[f_List_Index];
        f_Chosen_Index = f_List_Index;
        // Warning message
        PageMsgYN* nextpage = new PageMsgYN(scene(),
            "Are you sure you want to delete \"" + f_Chosen.displayName() + "\"?",
            m_Msg_Delete, m_Msg_Bk2Manage);
        nextpage->deleteOnExit(true);
        scene().gotoPage(nextpage);
    }
}

void PageManage::m_Cancel()
{
    PageMain* nextpage = new PageMain(scene());
    nextpage->deleteOnExit(true);
    scene().gotoPage(nextpage);
}

void PageManage::m_Nav_Up()
{
    if (f_List_Index <= 0) return;
    --f_List_Index;
    m_Refresh_List();
}

void PageManage::m_Nav_Down()
{
    if ((f_List_Index + 1) >= f_List_Count) return;
    ++f_List_Index;
    m_Refresh_List();
}

void PageManage::m_Msg_Delete(Scene& scene)
{
    // Delete pattern
    bool result = (remove(f_Chosen.fullPath().c_str()) == 0);
    // Confirm message
    std::string msg = result ? 
        ("Successfully deleted \"" + f_Chosen.displayName() + "\".") : 
        ("Failed to delete \"" + f_Chosen.displayName() + "\".");
    PageMsgOK* nextpage = new PageMsgOK(scene, msg, m_Msg_Bk2Manage);
    nextpage->deleteOnExit(true);
    scene.gotoPage(nextpage);
}

void PageManage::m_Msg_Bk2Manage(Scene& scene)
{
    PageManage* page = new PageManage(scene, f_Chosen_Index);
    page->deleteOnExit(true);
    scene.gotoPage(page);
}

#pragma endregion