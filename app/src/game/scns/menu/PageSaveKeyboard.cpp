#include "game/scns/menu/PageSaveKeyboard.h"

#include "game/assets/MenuSave.h"
#include "game/scns/menu/PageSave.h"
#include "game/scns/menu/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region macros

#define NOKEY \
    { \
        .cap = false, \
    }

#define KEY(v_lo, v_up, v_x, v_y) \
    { \
        .cap = true, \
        .lo = v_lo, \
        .up = v_up, \
        .off = v_x + v_y * DS_SCREEN_COLS, \
        .len = 1, \
    }

#define KEY2(v_char, v_x, v_y, v_len) \
    { \
        .cap = false, \
        .lo = v_char, \
        .up = 0x00, \
        .off = v_x + v_y * DS_SCREEN_COLS, \
        .len = v_len, \
    }

#pragma endregion

#pragma region init

PageSaveKeyboard::PageSaveKeyboard(Scene& scene, PageSave& page, Input input) : PageSaveWidget(scene, page)
{
    f_Input = input;
    f_Widget_L = nullptr;
    f_Widget_R = nullptr;
    f_Widget_U = nullptr;
    f_Widget_D = nullptr;
    f_CapsLock = false;
    f_Shift = false;
    f_SelectedIndex = 0xFFFF;
}

PageSaveKeyboard::~PageSaveKeyboard() { }

#pragma endregion

#pragma region fields

const PageSaveKeyboard::Key PageSaveKeyboard::f_Keys[] = 
{
    // 0x00 - 0x07
    NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY,
    // Backspace
    KEY2(0x08, 25, 7, 3),
    // 0x09 - 0x0F
    NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY,
    // Shift
    KEY2(0x10, 3, 13, 3),
    // 0x11 - 0x13
    NOKEY, NOKEY, NOKEY,
    // Caps Lock
    KEY2(0x14, 3, 11, 3),
    // 0x15 - 0x1F
    NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY,
    // Space
    KEY2(0x20, 7, 15, 17),
    // Exclamation point
    KEY('!', 0x00, 25, 11),
    // 0x22 - 0x27
    NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, NOKEY, 
    // Parentheses
    KEY('(', 0x00, 25, 13), KEY(')', 0x00, 27, 13),
    // 0x2A - 0x2B
    NOKEY, NOKEY,
    // Comma, dash, period
    KEY(',', 0x00, 21, 13), KEY('-', '_', 27, 9), KEY('.', 0x00, 23, 13),
    // 0x2F
    NOKEY,
    // Digits
    KEY('0', ')', 23, 7), KEY('1', '!', 5, 7), KEY('2', '@', 7, 7), KEY('3', '#', 9, 7), KEY('4', '$', 11, 7),
    KEY('5', '%', 13, 7), KEY('6', '^', 15, 7), KEY('7', '&', 17, 7), KEY('8', 0x00, 19, 7), KEY('9', '(', 21, 7),
    // 0x3A - 0x3C
    NOKEY, NOKEY, NOKEY,
    // Equals
    KEY('=', '+', 27, 11),
    // 0x3E - 0x40
    NOKEY, NOKEY, NOKEY,
    // Alphabet
    KEY('a', 'A', 7, 11), KEY('b', 'B', 15, 13), KEY('c', 'C', 11, 13), KEY('d', 'D', 11, 11),
    KEY('e', 'E', 7, 9), KEY('f', 'F', 13, 11), KEY('g', 'G', 15, 11), KEY('h', 'H', 17, 11),
    KEY('i', 'I', 17, 9), KEY('j', 'J', 19, 11), KEY('k', 'K', 21, 11), KEY('l', 'L', 23, 11),
    KEY('m', 'M', 19, 13), KEY('n', 'N', 17, 13), KEY('o', 'O', 19, 9), KEY('p', 'P', 21, 9),
    KEY('q', 'Q', 3, 9), KEY('r', 'R', 9, 9), KEY('s', 'S', 9, 11), KEY('t', 'T', 11, 9),
    KEY('u', 'U', 15, 9), KEY('v', 'V', 13, 13), KEY('w', 'W', 5, 9), KEY('x', 'X', 9, 13),
    KEY('y', 'Y', 13, 9), KEY('z', 'Z', 7, 13), 
    // Open bracket
    KEY('[', '{', 23, 9), 
    // 0x5C
    NOKEY, 
    // Close bracket
    KEY(']', '}', 25, 9),
    // 0x5E - 0x5F
    NOKEY, NOKEY, 
    // Accent
    KEY('`', '~', 3, 7),
};

#pragma endregion

#pragma region helper properties

u16 PageSaveKeyboard::p_x0() const { return ass::MenuSave::keyboard_x0; }

u16 PageSaveKeyboard::p_y0() const { return ass::MenuSave::keyboard_y0; }

u16 PageSaveKeyboard::p_x1() const { return ass::MenuSave::keyboard_x1; }

u16 PageSaveKeyboard::p_y1() const { return ass::MenuSave::keyboard_y1; }

#pragma endregion

#pragma region properties

const PageSaveWidget* PageSaveKeyboard::widget_L() const { return f_Widget_L; }
PageSaveWidget* PageSaveKeyboard::widget_L() { return f_Widget_L; }
void PageSaveKeyboard::widget_L(PageSaveWidget* value) { f_Widget_L = value; }

const PageSaveWidget* PageSaveKeyboard::widget_R() const { return f_Widget_R; }
PageSaveWidget* PageSaveKeyboard::widget_R() { return f_Widget_R; }
void PageSaveKeyboard::widget_R(PageSaveWidget* value) { f_Widget_R = value; }

const PageSaveWidget* PageSaveKeyboard::widget_U() const { return f_Widget_U; }
PageSaveWidget* PageSaveKeyboard::widget_U() { return f_Widget_U; }
void PageSaveKeyboard::widget_U(PageSaveWidget* value) { f_Widget_U = value; }

const PageSaveWidget* PageSaveKeyboard::widget_D() const { return f_Widget_D; }
PageSaveWidget* PageSaveKeyboard::widget_D() { return f_Widget_D; }
void PageSaveKeyboard::widget_D(PageSaveWidget* value) { f_Widget_D = value; }

u16 PageSaveKeyboard::x() const { return ass::MenuSave::keyboard_x; }

u16 PageSaveKeyboard::y() const { return ass::MenuSave::keyboard_y; }

u16 PageSaveKeyboard::w() const { return ass::MenuSave::keyboard_w; }

u16 PageSaveKeyboard::h() const { return ass::MenuSave::keyboard_h; }

#pragma endregion

#pragma region helper functions

void PageSaveKeyboard::m_Refresh()
{
    PageSaveWidget::m_Refresh();
    // Caps Lock
    if (!f_CapsLock)
    {
        u16* ptr = p_Scene().textGFX().bg_Buffer() + ass::MenuSave::caps_x + ass::MenuSave::caps_y * DS_SCREEN_COLS;
        std::fill(ptr, ptr + ass::MenuSave::caps_len, 0);
    }
    // Shift
    if (!f_Shift)
    {
        u16* ptr = p_Scene().textGFX().bg_Buffer() + ass::MenuSave::shift_x + ass::MenuSave::shift_y * DS_SCREEN_COLS;
        std::fill(ptr, ptr + ass::MenuSave::shift_len, 0);
    }
    // Keys
    {
        const Key* ptr = f_Keys;
        for (u16 i = 0; i < f_Keys_Count; ++i)
        {
            if (ptr->cap) p_Scene().textGFX().bg_Buffer()[ptr->off] = (f_CapsLock != f_Shift) ? ptr->up : ptr->lo;
            ++ptr;
        }
    }
}

void PageSaveKeyboard::m_Highlight(bool touching)
{
    PageSaveWidget::m_Highlight(touching);
    /*
    u16 color = (touching ? 0x02 : 0x01) << 12;
    u16* row = p_Scene().textGFX().bg_Buffer() + f_X + f_Y * DS_SCREEN_COLS;
    for (u16 y = 0; y < f_H; ++y)
    {
        u16* optr = row;
        for (u16 x = 0; x < f_W; ++x) *(optr++) |= color;
        row += DS_SCREEN_COLS;
    }
    */
}

void PageSaveKeyboard::m_Enter(PageSaveWidget* prev)
{
    PageSaveWidget::m_Enter(prev);
}

void PageSaveKeyboard::m_Exit(PageSaveWidget* next)
{
    PageSaveWidget::m_Exit(next);
}

void PageSaveKeyboard::m_Touch(u16 touch_X, u16 touch_Y)
{
    PageSaveWidget::m_Touch(touch_X, touch_Y);
}

void PageSaveKeyboard::m_Input_A()
{
    PageSaveWidget::m_Input_A();
}

void PageSaveKeyboard::m_Input_Left()
{
    PageSaveWidget::m_Input_Left();
    if (f_Widget_L) p_Page().focus(f_Widget_L);
}

void PageSaveKeyboard::m_Input_Right()
{
    PageSaveWidget::m_Input_Right();
    if (f_Widget_R) p_Page().focus(f_Widget_R);
}

void PageSaveKeyboard::m_Input_Up()
{
    PageSaveWidget::m_Input_Up();
    if (f_Widget_U) p_Page().focus(f_Widget_U);
}

void PageSaveKeyboard::m_Input_Down()
{
    PageSaveWidget::m_Input_Down();
    if (f_Widget_D) p_Page().focus(f_Widget_D);
}

#pragma endregion