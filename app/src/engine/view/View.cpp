#include "engine/view/View.h"

#include <__.h>

using namespace engine::view;

#pragma region init

View::View(int bg, engine::helper::RRValue48p16 bg_X, engine::helper::RRValue48p16 bg_Y)
{
    f_IsDirty = true;
    // Background
    f_BG = bg;
    f_BG_X = bg_X;
    f_BG_Y = bg_Y;
    // Camera
    f_Cam_X = engine::helper::RRValue48p16(0);
    f_Cam_Y = engine::helper::RRValue48p16(0);
    f_Cam_Zoom = zoom_100;
    // Post-init
    m_Refresh();
}

View::~View()
{

}

#pragma endregion

#pragma region const

const engine::helper::RRValue48p16 View::f_2 = engine::helper::RRValue48p16(2, 0);

const engine::helper::RRValue48p16 View::f_Zoom_Min = engine::helper::RRValue48p16(25, 0);
const engine::helper::RRValue48p16 View::f_Zoom_Max = engine::helper::RRValue48p16(400, 0);
const engine::helper::RRValue48p16 View::f_Bound_X0 = engine::helper::RRValue48p16(-512, 0);
const engine::helper::RRValue48p16 View::f_Bound_Y0 = engine::helper::RRValue48p16(-512, 0);
const engine::helper::RRValue48p16 View::f_Bound_X1 = engine::helper::RRValue48p16(512, 0);
const engine::helper::RRValue48p16 View::f_Bound_Y1 = engine::helper::RRValue48p16(512, 0);
const engine::helper::RRValue48p16 View::f_DS_Width = engine::helper::RRValue48p16(256, 0);
const engine::helper::RRValue48p16 View::f_DS_Height = engine::helper::RRValue48p16(192, 0);

#pragma endregion

#pragma region const

const engine::helper::RRValue48p16 View::hSpan_100 = engine::helper::RRValue48p16(256, 0);
const engine::helper::RRValue48p16 View::zoom_100 = engine::helper::RRValue48p16(100, 0);

#pragma endregion

#pragma region properties

engine::helper::RRValue48p16 View::cam_X() const { return f_Cam_X; }
void View::cam_X(engine::helper::RRValue48p16 value)
{
    if (f_Cam_X == value) return;
    // Set X-coordinate
    f_Cam_X = value;
    m_Refresh_Position();
    // Mark dirty
    f_IsDirty = true;
}

engine::helper::RRValue48p16 View::cam_Y() const { return f_Cam_Y; }
void View::cam_Y(engine::helper::RRValue48p16 value)
{
    if (f_Cam_Y == value) return;
    // Set Y-coordinate
    f_Cam_Y = value;
    m_Refresh_Position();
    // Mark dirty
    f_IsDirty = true;
}

engine::helper::RRValue48p16 View::cam_Zoom() const { return f_Cam_Zoom; }
void View::cam_Zoom(engine::helper::RRValue48p16 value)
{
    if (f_Cam_Zoom == value) return;
    // Set Zoom
    f_Cam_Zoom = value;
    m_Refresh_Size();
    // Mark dirty
    f_IsDirty = true;
}

engine::helper::RRValue48p16 View::cam_HSpan() const { return f_Cam_HSpan; }

engine::helper::RRValue48p16 View::cam_VSpan() const { return f_Cam_VSpan; }

engine::helper::RRValue48p16 View::cam_Ortho_Width() const { return f_Cam_Ortho_Width; }

engine::helper::RRValue48p16 View::cam_Ortho_Height() const { return f_Cam_Ortho_Height; }

engine::helper::RRValue48p16 View::cam_X0() const { return f_Cam_X0; }

engine::helper::RRValue48p16 View::cam_Y0() const { return f_Cam_Y0; }

engine::helper::RRValue48p16 View::cam_X1() const { return f_Cam_X1; }

engine::helper::RRValue48p16 View::cam_Y1() const { return f_Cam_Y1; }

#pragma endregion

#pragma region helper functions

void View::m_Refresh()
{
    m_Refresh_Size();
}

void View::m_Refresh_Size()
{
    // Fix zoom
    if (f_Cam_Zoom < f_Zoom_Min) f_Cam_Zoom = f_Zoom_Min;
    if (f_Cam_Zoom > f_Zoom_Max) f_Cam_Zoom = f_Zoom_Max;
    // Compute span
    f_Cam_HSpan = (hSpan_100 * zoom_100) / f_Cam_Zoom;
    f_Cam_VSpan = MATH_SCALE(f_DS_Width, f_DS_Height, f_Cam_HSpan);
    // Compute ortho
    f_Cam_Ortho_Width = f_Cam_HSpan / f_2;
    f_Cam_Ortho_Height = f_Cam_VSpan / f_2;
    // Refresh position
    m_Refresh_Position();
}

void View::m_Refresh_Position()
{
    // Fix position
    if ((f_Cam_X - f_Cam_Ortho_Width) < f_Bound_X0) f_Cam_X = f_Bound_X0 + f_Cam_Ortho_Width;
    if ((f_Cam_Y - f_Cam_Ortho_Height) < f_Bound_Y0) f_Cam_Y = f_Bound_Y0 + f_Cam_Ortho_Height;
    if ((f_Cam_X + f_Cam_Ortho_Width) > f_Bound_X1) f_Cam_X = f_Bound_X1 - f_Cam_Ortho_Width;
    if ((f_Cam_Y + f_Cam_Ortho_Height) > f_Bound_Y1) f_Cam_Y = f_Bound_Y1 - f_Cam_Ortho_Height;
    // Compute edges
    f_Cam_X0 = f_Cam_X - f_Cam_Ortho_Width;
    f_Cam_Y0 = f_Cam_Y - f_Cam_Ortho_Height;
    f_Cam_X1 = f_Cam_X0 + f_Cam_HSpan;
    f_Cam_Y1 = f_Cam_Y0 + f_Cam_VSpan;
}

#pragma endregion

#pragma region functions

void View::vblank()
{
    if (!f_IsDirty) return;
    f_IsDirty = false;
    // Update background
    s32 rawScroll_X = (f_Cam_X0 - f_BG_X).raw();
    s32 rawScroll_Y = (f_BG_Y - f_Cam_Y1).raw();
    s32 bg_Scroll_X = rawScroll_X >> 8; if ((rawScroll_X & 0x80) != 0) ++bg_Scroll_X;
    s32 bg_Scroll_Y = rawScroll_Y >> 8; if ((rawScroll_Y & 0x80) != 0) ++bg_Scroll_Y;
    s32 bg_Scale = f_Cam_HSpan.roundToWhole();
    bgSetScrollf(f_BG, bg_Scroll_X, bg_Scroll_Y);
    bgSetScale(f_BG, bg_Scale, bg_Scale);
}

#pragma endregion