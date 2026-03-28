#include "game/scns/menu/PageRandom.h"

#include "game/Global.h"
#include "game/ScreenUtil.h"
#include "game/assets/MenuRandom.h"
#include "game/scns/menu/PageMain.h"
#include "game/scns/menu/PageMsgYN.h"
#include "game/scns/menu/Scene.h"
#include "engine/data/RLE.h"

#include "game/scns/edit/Scene.h"

#include <cstdlib>

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region init

PageRandom::PageRandom(Scene& scene, u32 seed) : Page(scene)
{
    // Seed
    f_Seed = seed;
    f_Digits = m_Digits(f_Seed);
    // Screen
    f_Screen = nullptr;
}

PageRandom::~PageRandom()
{
    DELETE_ARRAY(f_Screen)
}

#pragma endregion

#pragma region fields

PageRandom::ButtonAction PageRandom::f_ButtonActions[] = 
{
    m_Action_0, m_Action_1, m_Action_2, m_Action_3, 
    m_Action_4, m_Action_5, m_Action_6, m_Action_7, 
    m_Action_8, m_Action_9, m_Action_A, m_Action_B, 
    m_Action_C, m_Action_D, m_Action_E, m_Action_F, 
    m_Action_Backspace, m_Action_OK, m_Action_Cancel,
};

u32 PageRandom::f_RandSeed = 0;

#pragma endregion

#pragma region helper functions

void PageRandom::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    ScreenUtil::load(ass::MenuRandom::data, ass::MenuRandom::size, f_Screen, f_Screen_Len);
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Initialize index
    f_Sel_Index = 0x11; // Select OK by default
    f_Sel_Touch = 0xFFFF;
    f_Sel_Touching = false;
    // Post-init
    m_Refresh();
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
        f_Sel_Touch = 0xFFFF;
        u16 touch_X = scene().input_Touch_Pos().px / 4;
        u16 touch_Y = scene().input_Touch_Pos().py / 4;
        for (u16 i = 0; i < ass::MenuRandom::buttons; ++i)
        {
            if (touch_X < ass::MenuRandom::buttons_x0[i]) continue;
            if (touch_Y < ass::MenuRandom::buttons_y0[i]) continue;
            if (touch_X >= ass::MenuRandom::buttons_x1[i]) continue;
            if (touch_Y >= ass::MenuRandom::buttons_y1[i]) continue;
            f_Sel_Touch = i; break;
        }
    }
    // Get input
    if (scene().input_Down() & KEY_A)
    {
        m_Button_Action();
    }
    else if (scene().input_Down() & KEY_B)
    {
        m_Action_Cancel(*this);
    }
    else if (scene().input_Down() & KEY_LEFT)
    {
        if (f_Sel_Index < ass::MenuRandom::buttons)
        {
            u16 next = ass::MenuRandom::buttons_l[f_Sel_Index];
            if (next < ass::MenuRandom::buttons)
            {
                f_Sel_Index = next;
                f_Sel_Touching = false;
                m_Refresh();
            }
        }
    }
    else if (scene().input_Down() & KEY_RIGHT)
    {
        if (f_Sel_Index < ass::MenuRandom::buttons)
        {
            u16 next = ass::MenuRandom::buttons_r[f_Sel_Index];
            if (next < ass::MenuRandom::buttons)
            {
                f_Sel_Index = next;
                f_Sel_Touching = false;
                m_Refresh();
            }
        }
    }
    else if (scene().input_Down() & KEY_UP)
    {
        if (f_Sel_Index < ass::MenuRandom::buttons)
        {
            u16 next = ass::MenuRandom::buttons_u[f_Sel_Index];
            if (next < ass::MenuRandom::buttons)
            {
                f_Sel_Index = next;
                f_Sel_Touching = false;
                m_Refresh();
            }
        }
    }
    else if (scene().input_Down() & KEY_DOWN)
    {
        if (f_Sel_Index < ass::MenuRandom::buttons)
        {
            u16 next = ass::MenuRandom::buttons_d[f_Sel_Index];
            if (next < ass::MenuRandom::buttons)
            {
                f_Sel_Index = next;
                f_Sel_Touching = false;
                m_Refresh();
            }
        }
    }
    else if (scene().input_Down() & KEY_TOUCH)
    {
        if (f_Sel_Touch < ass::MenuRandom::buttons)
        {
            f_Sel_Index = f_Sel_Touch;
            f_Sel_Touching = true;
            m_Refresh();
        }
    }
    else if (scene().input_Up() & KEY_TOUCH)
    {
        if (f_Sel_Touch == f_Sel_Index) m_Button_Action();
        f_Sel_Touching = false;
        m_Refresh();
    }
}

void PageRandom::m_vblank()
{
    Page::m_vblank();
}

void PageRandom::m_Button_Action()
{
    if (f_Sel_Index < ass::MenuRandom::buttons) f_ButtonActions[f_Sel_Index](*this);
}

void PageRandom::m_Refresh()
{
    u16 off;
    // Reset tiles
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Print seed
    off = ass::MenuRandom::seed_x + ass::MenuRandom::seed_y * DS_SCREEN_COLS;
    {
        // Compute location
        u16* beg = scene().textGFX().bg_Buffer() + off;
        u16* end = beg + ass::MenuRandom::seed_len;
        // Draw digits
        for (u16 i = 0; i < f_Digits; ++i)
        {
            u16 digit = (f_Seed >> (4 * (f_Digits - 1 - i))) & 0xF;
            if (digit < 10) *(beg++) = 0x30 + digit;
            else *(beg++) = 0x41 + digit - 10;
        }
        // Draw blanks
        if (beg < end)
        {
            *(beg++) = 0x0F;
            while (beg < end) *(beg++) = '_';
        }
    }
    // Highlight selected
    if (f_Sel_Index < ass::MenuRandom::buttons)
    {
        u16 button_x = ass::MenuRandom::buttons_x[f_Sel_Index];
        u16 button_y = ass::MenuRandom::buttons_y[f_Sel_Index];
        u16 button_w = ass::MenuRandom::buttons_w[f_Sel_Index];
        u16 button_h = ass::MenuRandom::buttons_h[f_Sel_Index];
        u16 highlight = (f_Sel_Touching ? 0x2 : 0x1) << 12;
        off = button_x + button_y * DS_SCREEN_COLS;
        for (u16 y = 0; y < button_h; ++y)
        {
            u16 i = off + y * DS_SCREEN_COLS;
            for (u16 x = 0; x < button_w; ++x)
                scene().textGFX().bg_Buffer()[i + x] |= highlight;
        }
    }
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageRandom::m_InputDigit(u32 digit)
{
    if (f_Digits >= ass::MenuRandom::seed_len) return;
    f_Seed <<= 4; f_Seed |= digit; ++f_Digits;
    m_Refresh();
}

u16 PageRandom::m_Digits(u32 value)
{
    u16 digits = 1;
    while (true)
    {
        value >>= 4;
        if (value == 0) break;
        ++digits;
    }
    return digits;
}

void PageRandom::m_Msg_No(Scene& scene)
{
    PageRandom* page = new PageRandom(scene, f_RandSeed);
    page->deleteOnExit(true);
    scene.gotoPage(page);
}

void PageRandom::m_Msg_Yes(Scene& scene)
{
    srand(f_RandSeed);
    // Clear pattern
    std::fill(Global::pattern()->cells(), Global::pattern()->cells() + PATTERN_AREA, false);
    Global::pattern_Path(engine::io::Path());
    // Determine content area
    static constexpr u16 dim_min = 16;
    static constexpr u16 dim_max = 64;
    u16 content_w = dim_min + rand() % (dim_max - dim_min);
    u16 content_h = dim_min + rand() % (dim_max - dim_min);
    u16 content_x = (PATTERN_WIDTH - content_w) / 2;
    u16 content_y = (PATTERN_HEIGHT - content_h) / 2;
    // Plot cells
    static constexpr u16 chance_min = 2;
    static constexpr u16 chance_max = 8;
    u16 chance = chance_min + rand() % (chance_max - chance_min);
    for (u16 y = 0; y < content_h; y++)
    {
        for (u16 x = 0; x < content_w; x++)
        {
            if ((rand() % chance) == 0)
                Global::pattern()->setcell(content_x + x, content_y + y, true);
        }
    }
    // Goto edit scene
    game::scns::edit::Scene* editScene = new game::scns::edit::Scene();
    editScene->deleteOnExit(true);
    engine::scenes::gotoScene(editScene);
}

void PageRandom::m_Action_0(PageRandom& page)
{
    page.m_InputDigit(0);
}

void PageRandom::m_Action_1(PageRandom& page)
{
    page.m_InputDigit(1);
}

void PageRandom::m_Action_2(PageRandom& page)
{
    page.m_InputDigit(2);
}

void PageRandom::m_Action_3(PageRandom& page)
{
    page.m_InputDigit(3);
}

void PageRandom::m_Action_4(PageRandom& page)
{
    page.m_InputDigit(4);
}

void PageRandom::m_Action_5(PageRandom& page)
{
    page.m_InputDigit(5);
}

void PageRandom::m_Action_6(PageRandom& page)
{
    page.m_InputDigit(6);
}

void PageRandom::m_Action_7(PageRandom& page)
{
    page.m_InputDigit(7);
}

void PageRandom::m_Action_8(PageRandom& page)
{
    page.m_InputDigit(8);
}

void PageRandom::m_Action_9(PageRandom& page)
{
    page.m_InputDigit(9);
}

void PageRandom::m_Action_A(PageRandom& page)
{
    page.m_InputDigit(0xA);
}

void PageRandom::m_Action_B(PageRandom& page)
{
    page.m_InputDigit(0xB);
}

void PageRandom::m_Action_C(PageRandom& page)
{
    page.m_InputDigit(0xC);
}

void PageRandom::m_Action_D(PageRandom& page)
{
    page.m_InputDigit(0xD);
}

void PageRandom::m_Action_E(PageRandom& page)
{
    page.m_InputDigit(0xE);
}

void PageRandom::m_Action_F(PageRandom& page)
{
    page.m_InputDigit(0xF);
}

void PageRandom::m_Action_Backspace(PageRandom& page)
{
    if (page.f_Digits == 0) return;
    page.f_Seed >>= 4; --page.f_Digits;
    page.m_Refresh();
}

void PageRandom::m_Action_OK(PageRandom& page)
{
    f_RandSeed = page.f_Seed;
    PageMsgYN* nextpage = new PageMsgYN(page.scene(),
        "The current pattern will be cleared. Is this OK?",
        m_Msg_Yes, m_Msg_No);
    nextpage->deleteOnExit(true);
    page.scene().gotoPage(nextpage);
}

void PageRandom::m_Action_Cancel(PageRandom& page)
{
    PageMain* nextpage = new PageMain(page.scene());
    nextpage->deleteOnExit(true);
    page.scene().gotoPage(nextpage);
}

#pragma endregion