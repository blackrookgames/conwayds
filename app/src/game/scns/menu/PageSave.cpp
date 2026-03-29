#include "game/scns/menu/PageSave.h"

#include <cstdlib>
#include <sstream>

#include "engine/data/RLE.h"
#include "engine/helper/StrUtil.h"
#include "game/FileUtil.h"
#include "game/Global.h"
#include "game/ScreenUtil.h"
#include "game/assets/MenuSave.h"
#include "game/scns/menu/PageMain.h"
#include "game/scns/menu/PageMsgOK.h"
#include "game/scns/menu/PageMsgYN.h"
#include "game/scns/menu/Scene.h"

#include "game/scns/edit/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region init

PageSave::PageSave(Scene& scene, const std::string* initialName) : Page(scene)
{
    // Initial name
    f_InitialName = initialName;
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
    f_Widget_Keyboard->widget_L(f_Widget_OK);
    f_Widget_Keyboard->widget_R(f_Widget_Cancel);
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

#pragma region fields

std::string PageSave::f_Chosen = "";
engine::io::Path PageSave::f_Chosen_Path = engine::io::Path();

const std::string PageSave::f_BadNames[] = 
{
    "CON", "PRN", "AUX", "NUL", 
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", 
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
};

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
    // Initialize name
    if (!f_InitialName)
    {
        size_t index = engine::helper::StrUtil::findChar(Global::pattern_Path().displayName(), ':');
        f_Name = Global::pattern_Path().displayName().substr(index + 1);
    }
    else f_Name = *f_InitialName;
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
    // Refresh name field
    u16* beg = scene().textGFX().bg_Buffer() + ass::MenuSave::field_x + ass::MenuSave::field_y * DS_SCREEN_COLS;
    u16* end = beg + ass::MenuSave::field_len;
    for (auto iptr = f_Name.begin(); iptr != f_Name.end(); ++iptr)
    {
        if (beg >= end) break;
        *(beg++) = *iptr;
    }
    if (beg < end)
    {
        *(beg++) = '_'; // Cursor
        while (beg < end) *(beg++) = 0x00; // Padding
    }
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageSave::m_OK(PageSaveButton& button, Scene& scene, PageSave& page)
{
    f_Chosen = page.f_Name;
    // Make sure name is valid
    if (f_Chosen == "")
    {
        PageMsgOK* nextpage = new PageMsgOK(scene,
            "Save name cannot be empty.",
            m_Msg_No);
        nextpage->deleteOnExit(true);
        scene.gotoPage(nextpage);
        return;
    }
    for (u8 i = 0; i < f_BadNames_Count; ++i)
    {
        if (!engine::helper::StrUtil::noCaseEqu(f_Chosen, f_BadNames[i]))
            continue;
        PageMsgOK* nextpage = new PageMsgOK(scene,
            "The name \"" + f_BadNames[i] + "\" is reserved and cannot be used for a save name.",
            m_Msg_No);
        nextpage->deleteOnExit(true);
        scene.gotoPage(nextpage);
        return;
    }
    // Compute path
    f_Chosen_Path.fullPath() = FileUtil::user_Dir + "/" + f_Chosen + FileUtil::extension;
    f_Chosen_Path.displayName() = FileUtil::user_Prefix + f_Chosen;
    // Does path already exist?
    engine::io::Path* paths; u16 paths_Count;
    FileUtil::getPatterns(paths, paths_Count);
    for (u16 i = 0; i < paths_Count; ++i)
    {
        if (f_Chosen_Path.fullPath() != paths[i].fullPath())
            continue;
        PageMsgYN* nextpage = new PageMsgYN(scene,
            "Overwrite \"" + f_Chosen_Path.displayName() + "\"?",
            m_Msg_Save, m_Msg_No);
        nextpage->deleteOnExit(true);
        scene.gotoPage(nextpage);
        return;
    }
    // Make sure maximum capacity has not been reached
    if (paths_Count >= FileUtil::capacity)
    {
        std::ostringstream msg;
        msg << "The file limit of " << (int)FileUtil::capacity << " has been reached.";
        PageMsgOK* nextpage = new PageMsgOK(scene, msg.str(), m_Msg_No);
        nextpage->deleteOnExit(true);
        scene.gotoPage(nextpage);
        return;
    }
    // Save
    m_Msg_Save(scene);
}

void PageSave::m_Cancel(PageSaveButton& button, Scene& scene, PageSave& page)
{
    PageMain* nextpage = new PageMain(scene);
    nextpage->deleteOnExit(true);
    scene.gotoPage(nextpage);
}

void PageSave::m_Input(PageSaveKeyboard& keyboard, Scene& scene, PageSave& page, char chr)
{
    if (chr >= ' ' && chr < 0xFF)
    {
        if (page.f_Name.length() < ass::MenuSave::field_len)
            page.f_Name.push_back(chr);
    }
    else if (chr == 0x08) // Backspace
    {
        if (page.f_Name.length() > 0)
            page.f_Name.pop_back();
    }
}

void PageSave::m_Msg_OK(Scene& scene)
{
    // Goto edit scene
    game::scns::edit::Scene* editScene = new game::scns::edit::Scene();
    editScene->deleteOnExit(true);
    engine::scenes::gotoScene(editScene);
}

void PageSave::m_Msg_Save(Scene& scene)
{
    if (Global::pattern()->save_file(f_Chosen_Path.fullPath().c_str()))
    {
        Global::pattern_Path(f_Chosen_Path);
        PageMsgOK* nextpage = new PageMsgOK(scene, 
            "Successfully saved \"" + f_Chosen_Path.displayName() + "\".",
            m_Msg_OK);
        nextpage->deleteOnExit(true);
        scene.gotoPage(nextpage);
    }
    else
    {
        PageMsgOK* nextpage = new PageMsgOK(scene, 
            "Failed to save \"" + f_Chosen_Path.displayName() + "\".",
            m_Msg_No);
        nextpage->deleteOnExit(true);
        scene.gotoPage(nextpage);
    }
}

void PageSave::m_Msg_No(Scene& scene)
{
    PageSave* page = new PageSave(scene, &f_Chosen);
    page->deleteOnExit(true);
    scene.gotoPage(page);
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