#include "game/scns/menu/PageSaveWidget.h"

#include "game/scns/menu/PageSave.h"
#include "game/scns/menu/Scene.h"

using namespace game::scns::menu;

#pragma region init

PageSaveWidget::PageSaveWidget(Scene& scene, PageSave& page) : f_Scene(scene), f_Page(page) { }

PageSaveWidget::~PageSaveWidget() { }

#pragma endregion

#pragma region helper properties

const Scene& PageSaveWidget::p_Scene() const { return f_Scene; }
Scene& PageSaveWidget::p_Scene() { return f_Scene; }

const PageSave& PageSaveWidget::p_Page() const { return f_Page; }
PageSave& PageSaveWidget::p_Page() { return f_Page; }

u16 PageSaveWidget::p_x0() const { return 0; }

u16 PageSaveWidget::p_y0() const { return 0; }

u16 PageSaveWidget::p_x1() const { return 0; }

u16 PageSaveWidget::p_y1() const { return 0; }

#pragma endregion

#pragma region properties

u16 PageSaveWidget::x() const { return 0; }

u16 PageSaveWidget::y() const { return 0; }

u16 PageSaveWidget::w() const { return 0; }

u16 PageSaveWidget::h() const { return 0; }

#pragma endregion

#pragma region helper functions

void PageSaveWidget::m_Refresh() { }

void PageSaveWidget::m_Highlight(bool touching) { }

void PageSaveWidget::m_Enter(PageSaveWidget* prev) { }

void PageSaveWidget::m_Exit(PageSaveWidget* next) { }

void PageSaveWidget::m_Action() { }

void PageSaveWidget::m_Touch(u16 touch_X, u16 touch_Y) { }

void PageSaveWidget::m_Input_A() { }

void PageSaveWidget::m_Input_Left() { }

void PageSaveWidget::m_Input_Right() { }

void PageSaveWidget::m_Input_Up() { }

void PageSaveWidget::m_Input_Down() { }

#pragma endregion