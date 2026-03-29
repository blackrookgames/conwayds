#include "game/scns/menu/PageSaveKeyboard.h"

#include "game/assets/MenuSave.h"
#include "game/scns/menu/PageSave.h"
#include "game/scns/menu/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region macros

#define BADCHAR 0x99

#define NOKEY \
    { \
        .cap = false, \
        .lo = 0x00, \
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
    f_CapsLock = false;
    f_Shift = false;
    f_Sel_X = 0xFFFF;
    f_Sel_Y = 0xFFFF;
    f_Sel_Key = nullptr;
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
            if (ptr->cap)
            {
                u8 chr = m_GetChar(*ptr);
                p_Scene().textGFX().bg_Buffer()[ptr->off] = (chr != 0x00) ? chr : BADCHAR;
            }
            ++ptr;
        }
    }
}

void PageSaveKeyboard::m_Highlight(bool touching)
{
    PageSaveWidget::m_Highlight(touching);
    // Highlight key
    if (f_Sel_Key)
    {
        u16 color = (touching ? 0x02 : 0x01) << 12;
        u16* optr = p_Scene().textGFX().bg_Buffer() + f_Sel_Key->off;
        for (u16 i = 0; i < f_Sel_Key->len; ++i) *(optr++) |= color;
    }
}

void PageSaveKeyboard::m_Enter(PageSaveWidget* prev)
{
    PageSaveWidget::m_Enter(prev);
    // Set selection
    u16 x;
    if (prev)
    {
        x = prev->x() + prev->w() / 2;
        x = ((x < ass::MenuSave::keyboard_x) ? 0 : (x - ass::MenuSave::keyboard_x)) / ass::MenuSave::keyboard_cell_tile_w;
        x = (x < ass::MenuSave::keygrid_split) ? 0 : (ass::MenuSave::keygrid_cols - 1);
    }
    else x = 0;
    m_Set_Selection(x, ass::MenuSave::keygrid_rows - 1);
}

void PageSaveKeyboard::m_Exit(PageSaveWidget* next)
{
    PageSaveWidget::m_Exit(next);
}

void PageSaveKeyboard::m_Touch(u16 touch_X, u16 touch_Y)
{
    PageSaveWidget::m_Touch(touch_X, touch_Y);
    // Determine key
    u16 x = ((touch_X < ass::MenuSave::keyboard_x0) ? 0 : (touch_X - ass::MenuSave::keyboard_x0)) / ass::MenuSave::keyboard_cell_w;
    if (x >= ass::MenuSave::keygrid_cols) x = ass::MenuSave::keygrid_cols - 1;
    u16 y = ((touch_Y < ass::MenuSave::keyboard_y0) ? 0 : (touch_Y - ass::MenuSave::keyboard_y0)) / ass::MenuSave::keyboard_cell_h;
    if (y >= ass::MenuSave::keygrid_rows) y = ass::MenuSave::keygrid_rows - 1;
    m_Set_Selection(x, y);
    // Input
    m_Input();
}

void PageSaveKeyboard::m_Input_A()
{
    PageSaveWidget::m_Input_A();
    m_Input();
}

void PageSaveKeyboard::m_Input_Left()
{
    PageSaveWidget::m_Input_Left();
    m_Inc_Selection(ass::MenuSave::keygrid_cols - 1);
}

void PageSaveKeyboard::m_Input_Right()
{
    PageSaveWidget::m_Input_Right();
    m_Inc_Selection(1);
}

void PageSaveKeyboard::m_Input_Up()
{
    PageSaveWidget::m_Input_Up();
    if (f_Sel_Y > 0) m_Set_Selection(f_Sel_X, f_Sel_Y - 1);
}

void PageSaveKeyboard::m_Input_Down()
{
    PageSaveWidget::m_Input_Down();
    if ((f_Sel_Y + 1) < ass::MenuSave::keygrid_rows)
    {
        m_Set_Selection(f_Sel_X, f_Sel_Y + 1);
    }
    else
    {
        if (f_Sel_X < ass::MenuSave::keygrid_split)
        {
            if (f_Widget_L) p_Page().focus(f_Widget_L);
        }
        else
        {
            if (f_Widget_R) p_Page().focus(f_Widget_R);
        }
    }
}

u8 PageSaveKeyboard::m_GetChar(const Key& key)
{
    if (key.up >= 'A' && key.up <= 'Z')
        return (f_Shift != f_CapsLock) ? key.up : key.lo;
    return (key.cap && f_Shift) ? key.up : key.lo;
}

void PageSaveKeyboard::m_Set_Selection(u16 x, u16 y)
{
    // Position
    f_Sel_X = x;
    f_Sel_Y = y;
    // Key
    f_Sel_Key = nullptr;
    if (f_Sel_X < ass::MenuSave::keygrid_cols && f_Sel_Y < ass::MenuSave::keygrid_rows)
    {
        u8 key = ass::MenuSave::keygrid[f_Sel_X + f_Sel_Y * ass::MenuSave::keygrid_cols];
        if (key < f_Keys_Count) f_Sel_Key = (f_Keys + key);
    }
}

void PageSaveKeyboard::m_Inc_Selection(u16 x)
{
    // Don't increment unless a key is currently selected
    if (!f_Sel_Key) return;
    // Goto next key
    const Key* prev = f_Sel_Key;
    u8 i = 0; // Fail safe (for spacebar)
    while (f_Sel_Key == prev && i < ass::MenuSave::keygrid_cols)
    {
        m_Set_Selection((f_Sel_X + x) % ass::MenuSave::keygrid_cols, f_Sel_Y);
        ++i;
    }
}

void PageSaveKeyboard::m_Input()
{
    if (!f_Sel_Key) return;
    // Get character
    u8 chr = m_GetChar(*f_Sel_Key);
    switch (chr)
    {
        // Nothing (ignore?
        case 0x00: break;
        // Shift?
        case 0x10: f_Shift = !f_Shift; break;
        // Caps lock?
        case 0x14: f_CapsLock = !f_CapsLock; break;
        // Everything else (including backspace)?
        default:
            f_Input(*this, p_Scene(), p_Page(), chr);
            f_Shift = false; // Reset shift
            break;
    }
}

#pragma endregion