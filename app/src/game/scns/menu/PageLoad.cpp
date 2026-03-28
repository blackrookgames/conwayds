#include "game/scns/menu/PageLoad.h"

#include <sstream>

#include "game/Global.h"
#include "game/ScreenUtil.h"
#include "game/assets/MenuLoad.h"
#include "game/scns/menu/PageMain.h"
#include "game/scns/menu/PageMsgOK.h"
#include "game/scns/menu/PageMsgYN.h"
#include "game/scns/menu/Scene.h"
#include "engine/data/RLE.h"
#include "engine/helper/DirUtil.h"

#include "game/scns/edit/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region init

PageLoad::PageLoad(Scene& scene) : Page(scene)
{
    f_Screen = nullptr;
    f_List_Names = nullptr;
}

PageLoad::~PageLoad()
{
    DELETE_ARRAY(f_List_Names)
    DELETE_ARRAY(f_Screen)
}

#pragma endregion

#pragma region fields

std::string PageLoad::f_Chosen_Name = "";
std::string PageLoad::f_Chosen_Path = "";

#pragma endregion

#pragma region helper functions

void PageLoad::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    ScreenUtil::load(ass::MenuLoad::data, ass::MenuLoad::size, f_Screen, f_Screen_Len);
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Initialize button index
    f_But_Index = 0;
    f_But_Touch = 0xFFFF;
    f_But_Touch_Down = 0xFFFF;
    f_But_Touching = false;
    // Initialize list
    m_GetFileList(f_List_Names, f_List_Paths, f_List_Count);
    f_List_Index = (f_List_Count > 0) ? 0 : 0xFFFF;
    f_List_Offset = 0;
    // Post-init
    m_Refresh_List();
    m_Refresh_Buttons();
}

void PageLoad::m_exit()
{
    // Call base
    Page::m_exit();
}

void PageLoad::m_update()
{
    Page::m_update();
    // Get touch
    if (scene().input_Touch())
    {
        f_But_Touch = 0xFFFF;
        u16 touch_X = scene().input_Touch_Pos().px;
        u16 touch_Y = scene().input_Touch_Pos().py;
        for (u16 i = 0; i < ass::MenuLoad::buttons_count; ++i)
        {
            auto button = ass::MenuLoad::buttons[i];
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
        if ((f_But_Index + 1) < ass::MenuLoad::buttons_touch)
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
        if (f_But_Touch < ass::MenuLoad::buttons_count)
        {
            if (f_But_Touch < ass::MenuLoad::buttons_touch)
                f_But_Index = f_But_Touch;
            f_But_Touch_Down = f_But_Touch;
            f_But_Touching = true;
            m_Refresh_Buttons();
        }
        else
        {
            u16 x = scene().input_Touch_Pos().px / 8;
            u16 y = scene().input_Touch_Pos().py / 8;
            if (x >= ass::MenuLoad::list_x && y >= ass::MenuLoad::list_y)
            {
                x -= ass::MenuLoad::list_x; y -= ass::MenuLoad::list_y;
                if (x < ass::MenuLoad::list_w && y < ass::MenuLoad::list_h)
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

void PageLoad::m_vblank()
{
    Page::m_vblank();
}

void PageLoad::m_GetFileList(std::string*& names, std::string*& paths, u16& count)
{
    // Get samples
    std::string* samps; u16 samps_Count;
    engine::helper::DirUtil::getPaths("nitro:/samples", samps, samps_Count, true, true, false);
    // Create final array
    count = samps_Count;
    if (count > 0)
    {
        std::string* iptr;
        // Create array
        names = new std::string[count];
        paths = new std::string[count];
        std::string* nptr = names;
        std::string* pptr = paths;
        // Add samples
        iptr = samps;
        for (u16 i = 0; i < samps_Count; ++i)
        {
            // Find last slash
            size_t index = -1;
            for (u16 j = 0; j < iptr->length(); ++j) { if ((*iptr)[j] == '/') index = j; }
            // Add
            *nptr = "SAMP:" + iptr->substr(index + 1);
            *pptr = *iptr;
            // Next
            ++iptr; ++nptr; ++pptr;
        }
    }
    else { names = nullptr; paths = nullptr; }
    // Delete
    DELETE_ARRAY(samps)
}

void PageLoad::m_Button_Action(u16 index)
{
    switch (index)
    {
        case 0: m_OK(); break;
        case 1: m_Cancel(); break;
        case 2: m_Nav_Up(); break;
        case 3: m_Nav_Down(); break;
    }
}

void PageLoad::m_Refresh_List()
{
    u16 chr;
    u16 pos;
    // Fix offset
    if (f_List_Offset > f_List_Index)
        f_List_Offset = f_List_Index;
    if ((f_List_Offset + ass::MenuLoad::list_h) <= f_List_Index)
        f_List_Offset = f_List_Index - (ass::MenuLoad::list_h - 1);
    if (f_List_Offset < 0)
        f_List_Offset = 0;
    // Draw list
    u16* off = scene().textGFX().bg_Buffer() + ass::MenuLoad::list_x + ass::MenuLoad::list_y * DS_SCREEN_COLS;
    for (u16 y = 0; y < ass::MenuLoad::list_h; ++y)
    {
        u16 index = f_List_Offset + y;
        u16* row = off;
        u16 x = 0;
        // Determine color
        u16 color = ((f_List_Index == index) ? 0x04 : 0) << 12;
        // Item
        if (index < f_List_Count)
        {
            std::string item = f_List_Names[index];
            while (x < ass::MenuLoad::list_w)
            {
                if (x >= item.length()) break;
                *row = color | item[x];
                ++row; ++x;
            }
        }
        // Padding
        while (x < ass::MenuLoad::list_w)
        {
            *row = 0x00;
            ++row; ++x;
        }
        // Next
        off += DS_SCREEN_COLS;
    }
    // Draw up arrow
    pos = ass::MenuLoad::list_u_x + ass::MenuLoad::list_u_y * DS_SCREEN_COLS;
    if (f_List_Index != 0xFFFF && f_List_Offset > 0) chr = f_Screen[pos]; else chr = 0x00;
    scene().textGFX().bg_Buffer()[pos] = chr;
    // Draw down arrow
    pos = ass::MenuLoad::list_d_x + ass::MenuLoad::list_d_y * DS_SCREEN_COLS;
    if ((f_List_Offset + ass::MenuLoad::list_h) < f_List_Count) chr = f_Screen[pos]; else chr = 0x00;
    scene().textGFX().bg_Buffer()[pos] = chr;
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageLoad::m_Refresh_Buttons()
{
    static constexpr u16 mask = (1 << 12) - 1;
    // Set button colors
    for (u16 i = 0; i < ass::MenuLoad::buttons_count; ++i)
    {
        auto button = ass::MenuLoad::buttons[i];
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

void PageLoad::m_OK()
{
    if (f_List_Index < f_List_Count)
    {
        f_Chosen_Name = f_List_Names[f_List_Index];
        f_Chosen_Path = f_List_Paths[f_List_Index];
        // Warning message
        PageMsgYN* nextpage = new PageMsgYN(scene(),
            "The current pattern will be cleared. Is this OK?",
            m_Msg_Yes, m_Msg_No);
        nextpage->deleteOnExit(true);
        scene().gotoPage(nextpage);
    }
}

void PageLoad::m_Cancel()
{
    PageMain* nextpage = new PageMain(scene());
    nextpage->deleteOnExit(true);
    scene().gotoPage(nextpage);
}

void PageLoad::m_Nav_Up()
{
    if (f_List_Index <= 0) return;
    --f_List_Index;
    m_Refresh_List();
}

void PageLoad::m_Nav_Down()
{
    if ((f_List_Index + 1) >= f_List_Count) return;
    ++f_List_Index;
    m_Refresh_List();
}

void PageLoad::m_Msg_No(Scene& scene)
{
    PageLoad* page = new PageLoad(scene);
    page->deleteOnExit(true);
    scene.gotoPage(page);
}

void PageLoad::m_Msg_Yes(Scene& scene)
{
    // Load pattern
    bool result = Global::pattern()->load_file(f_Chosen_Path.c_str());
    if (!result) std::fill(Global::pattern()->cells(), Global::pattern()->cells() + PATTERN_AREA, false);
    // Confirm message
    std::ostringstream msg;
    msg << (result ? "Successfully loaded " : "Failed to load \"") << f_Chosen_Name << "\"";
    PageMsgOK* nextpage = new PageMsgOK(scene, msg.str(), m_Msg_OK);
    nextpage->deleteOnExit(true);
    scene.gotoPage(nextpage);
}

void PageLoad::m_Msg_OK(Scene& scene)
{
    // Goto edit scene
    game::scns::edit::Scene* editScene = new game::scns::edit::Scene();
    editScene->deleteOnExit(true);
    engine::scenes::gotoScene(editScene);
}

#pragma endregion