#include "game/scns/menu/PageSaveButton.h"

#include "game/scns/menu/PageSave.h"
#include "game/scns/menu/Scene.h"

using namespace game::scns::menu;

#pragma region init

PageSaveButton::PageSaveButton(Scene& scene, PageSave& page, Action action, u16 x, u16 y, u16 w, u16 h) : PageSaveWidget(scene, page)
{
    f_Action = action;
    f_Widget_L = nullptr;
    f_Widget_R = nullptr;
    f_Widget_U = nullptr;
    f_Widget_D = nullptr;
    f_X = x;
    f_Y = y;
    f_W = w;
    f_H = h;
    f_X0 = f_X * 8;
    f_Y0 = f_Y * 8;
    f_X1 = f_X0 + f_W * 8;
    f_Y1 = f_Y0 + f_H * 8;
}

PageSaveButton::~PageSaveButton() { }

#pragma endregion

#pragma region helper properties

u16 PageSaveButton::p_x0() const { return f_X0; }

u16 PageSaveButton::p_y0() const { return f_Y0; }

u16 PageSaveButton::p_x1() const { return f_X1; }

u16 PageSaveButton::p_y1() const { return f_Y1; }

#pragma endregion

#pragma region properties

const PageSaveWidget* PageSaveButton::widget_L() const { return f_Widget_L; }
PageSaveWidget* PageSaveButton::widget_L() { return f_Widget_L; }
void PageSaveButton::widget_L(PageSaveWidget* value) { f_Widget_L = value; }

const PageSaveWidget* PageSaveButton::widget_R() const { return f_Widget_R; }
PageSaveWidget* PageSaveButton::widget_R() { return f_Widget_R; }
void PageSaveButton::widget_R(PageSaveWidget* value) { f_Widget_R = value; }

const PageSaveWidget* PageSaveButton::widget_U() const { return f_Widget_U; }
PageSaveWidget* PageSaveButton::widget_U() { return f_Widget_U; }
void PageSaveButton::widget_U(PageSaveWidget* value) { f_Widget_U = value; }

const PageSaveWidget* PageSaveButton::widget_D() const { return f_Widget_D; }
PageSaveWidget* PageSaveButton::widget_D() { return f_Widget_D; }
void PageSaveButton::widget_D(PageSaveWidget* value) { f_Widget_D = value; }

u16 PageSaveButton::x() const { return f_X; }

u16 PageSaveButton::y() const { return f_Y; }

u16 PageSaveButton::w() const { return f_W; }

u16 PageSaveButton::h() const { return f_H; }

#pragma endregion

#pragma region helper functions

void PageSaveButton::m_Highlight(bool touching)
{
    PageSaveWidget::m_Highlight(touching);
    u16 color = (touching ? 0x02 : 0x01) << 12;
    u16* row = p_Scene().textGFX().bg_Buffer() + f_X + f_Y * DS_SCREEN_COLS;
    for (u16 y = 0; y < f_H; ++y)
    {
        u16* optr = row;
        for (u16 x = 0; x < f_W; ++x) *(optr++) |= color;
        row += DS_SCREEN_COLS;
    }
}

void PageSaveButton::m_Action()
{
    PageSaveWidget::m_Action();
    f_Action(*this, p_Scene(), p_Page());
}

void PageSaveButton::m_Input_Left()
{
    PageSaveWidget::m_Input_Left();
    if (f_Widget_L) p_Page().focus(f_Widget_L);
}

void PageSaveButton::m_Input_Right()
{
    PageSaveWidget::m_Input_Right();
    if (f_Widget_R) p_Page().focus(f_Widget_R);
}

void PageSaveButton::m_Input_Up()
{
    PageSaveWidget::m_Input_Up();
    if (f_Widget_U) p_Page().focus(f_Widget_U);
}

void PageSaveButton::m_Input_Down()
{
    PageSaveWidget::m_Input_Down();
    if (f_Widget_D) p_Page().focus(f_Widget_D);
}

#pragma endregion