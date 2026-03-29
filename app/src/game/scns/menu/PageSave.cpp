#include "game/scns/menu/PageSave.h"

#include "game/Global.h"
#include "game/ScreenUtil.h"
#include "game/assets/MenuSave.h"
#include "game/scns/menu/PageMain.h"
#include "game/scns/menu/PageMsgYN.h"
#include "game/scns/menu/Scene.h"
#include "engine/data/RLE.h"

#include "game/scns/edit/Scene.h"

#include <cstdlib>

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region init

PageSave::PageSave(Scene& scene) : Page(scene)
{
    // Widgets
    f_Widgets_Count = 3;
    f_Widgets = new PageSaveWidget*[f_Widgets_Count];
    // OK Widget
    f_Widget_OK = new PageSaveButton(this->scene(), *this, m_OK, 
        ass::MenuSave::button_ok_x, ass::MenuSave::button_ok_y,
        ass::MenuSave::button_w, ass::MenuSave::button_h);
    f_Widgets[0] = f_Widget_OK;
    // Cancel Widget
    f_Widget_Cancel = new PageSaveButton(this->scene(), *this, m_Cancel, 
        ass::MenuSave::button_cancel_x, ass::MenuSave::button_cancel_y,
        ass::MenuSave::button_w, ass::MenuSave::button_h);
    f_Widgets[1] = f_Widget_Cancel;
    // Keyboard Widget
    f_Widget_Keyboard = new PageSaveKeyboard(this->scene(), *this, m_Input);
    f_Widgets[2] = f_Widget_Keyboard;
    // Widget connections
    f_Widget_OK->widget_L(f_Widget_Cancel);
    f_Widget_OK->widget_R(f_Widget_Cancel);
    f_Widget_OK->widget_U(f_Widget_Keyboard);
    f_Widget_Cancel->widget_L(f_Widget_OK);
    f_Widget_Cancel->widget_R(f_Widget_OK);
    f_Widget_Cancel->widget_U(f_Widget_Keyboard);
    // Screen
    f_Screen = nullptr;
}

PageSave::~PageSave()
{
    // Screen
    DELETE_ARRAY(f_Screen)
    // Widgets
    delete f_Widget_OK;
    delete f_Widget_Cancel;
    delete f_Widget_Keyboard;
    delete[] f_Widgets;
}

#pragma endregion

#pragma region properties

bool PageSave::touching() const { return f_Touching; }

#pragma endregion

#pragma region helper functions

void PageSave::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    ScreenUtil::load(ass::MenuSave::data, ass::MenuSave::size, f_Screen, f_Screen_Len);
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Initialize focus
    f_Widget_Focus = nullptr;
    f_Widget_Touch = nullptr;
    f_Touching = false;
    // Post-init
    m_Refresh();
    focus(f_Widget_OK);
}

void PageSave::m_exit()
{
    // Unfocus
    if (f_Widget_Focus) f_Widget_Focus->m_Exit(nullptr);
    // Call base
    Page::m_exit();
}

void PageSave::m_update()
{
    Page::m_update();
    // Get touch
    u16 touch_X = scene().input_Touch_Pos().px;
    u16 touch_Y = scene().input_Touch_Pos().py;
    if (scene().input_Touch())
    {
        f_Widget_Touch = nullptr;
        for (u16 i = 0; i < f_Widgets_Count; ++i)
        {
            PageSaveWidget* widget = f_Widgets[i];
            if (!widget) continue;
            NOCASHMESSAGE(widget)
            if (touch_X < widget->p_x0()) continue;
            if (touch_Y < widget->p_y0()) continue;
            if (touch_X >= widget->p_x1()) continue;
            if (touch_Y >= widget->p_y1()) continue;
            f_Widget_Touch = widget; break;
        }
    }
    // Get input
    if (scene().input_Down() & KEY_A)
    {
        auto widget = f_Widget_Focus; // In case focus changes
        if (widget)
        {
            widget->m_Action();
            widget->m_Input_A();
        }
        f_Touching = false;
        m_Refresh();
    }
    else if (scene().input_Down() & KEY_B)
    {
        m_Cancel(*f_Widget_Cancel, scene(), *this);
    }
    else if (scene().input_Repeat() & KEY_LEFT)
    {
        if (f_Widget_Focus) f_Widget_Focus->m_Input_Left();
        f_Touching = false;
        m_Refresh();
    }
    else if (scene().input_Repeat() & KEY_RIGHT)
    {
        if (f_Widget_Focus) f_Widget_Focus->m_Input_Right();
        f_Touching = false;
        m_Refresh();
    }
    else if (scene().input_Repeat() & KEY_UP)
    {
        if (f_Widget_Focus) f_Widget_Focus->m_Input_Up();
        f_Touching = false;
        m_Refresh();
    }
    else if (scene().input_Repeat() & KEY_DOWN)
    {
        if (f_Widget_Focus) f_Widget_Focus->m_Input_Down();
        f_Touching = false;
        m_Refresh();
    }
    else if (scene().input_Down() & KEY_TOUCH)
    {
        if (f_Widget_Touch)
        {
            focus(f_Widget_Touch);
            f_Widget_Touch->m_Touch(touch_X, touch_Y);
            f_Touching = true;
        }
        m_Refresh();
    }
    else if (scene().input_Up() & KEY_TOUCH)
    {
        if (f_Widget_Focus == f_Widget_Touch) f_Widget_Focus->m_Action();
        f_Touching = false;
        m_Refresh();
    }
}

void PageSave::m_vblank()
{
    Page::m_vblank();
}

void PageSave::m_Refresh()
{
    // Reset tiles
    std::copy(f_Screen, f_Screen + f_Screen_Len, scene().textGFX().bg_Buffer());
    // Refresh widgets
    for (u16 i = 0; i < f_Widgets_Count; ++i)
        f_Widgets[i]->m_Refresh();
    if (f_Widget_Focus)
        f_Widget_Focus->m_Highlight(touching());
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageSave::m_OK(PageSaveButton& button, Scene& scene, PageSave& page)
{
}

void PageSave::m_Cancel(PageSaveButton& button, Scene& scene, PageSave& page)
{
    PageMain* nextpage = new PageMain(scene);
    nextpage->deleteOnExit(true);
    scene.gotoPage(nextpage);
}

void PageSave::m_Input(PageSaveKeyboard& keyboard, Scene& scene, PageSave& page, char chr)
{
    if (chr >= ' ')
    {

    }
    else if (chr == 0x08) // Backspace
    {
        
    }
}

void PageSave::m_Msg_OK(Scene& scene)
{
    // Goto edit scene
    game::scns::edit::Scene* editScene = new game::scns::edit::Scene();
    editScene->deleteOnExit(true);
    engine::scenes::gotoScene(editScene);
}

#pragma endregion

#pragma region functions

void PageSave::focus(PageSaveWidget* widget)
{
    // Make sure we're switching focus
    if (widget == f_Widget_Focus) return;
    // Set variable
    PageSaveWidget* prev = f_Widget_Focus;
    f_Widget_Focus = widget;
    // Unfocus
    if (prev) prev->m_Exit(f_Widget_Focus);
    // Focus
    if (f_Widget_Focus) f_Widget_Focus->m_Enter(prev);
    // Refresh
    m_Refresh();
}

#pragma endregion