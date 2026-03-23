#include "engine/view/View.h"

using namespace engine::view;

#pragma region init

View::View(int bg, engine::helper::RRValue32 bg_X, engine::helper::RRValue32 bg_Y)
{
    f_IsDirty = false;
    f_BG = bg;
    f_BG_X = bg_X;
    f_BG_Y = bg_Y;
    f_Cam_X = 0;
    f_Cam_Y = 0;
    f_Cam_Zoom = 100 << 8;
}

View::~View()
{

}

#pragma endregion

#pragma region properties

engine::helper::RRValue32 View::cam_X() const { return f_Cam_X; }
void View::cam_X(engine::helper::RRValue32 value)
{
    if (f_Cam_X.equ(value)) return;
    // Set X-coordinate
    f_Cam_X = value;
    // Mark dirty
    f_IsDirty = true;
    // TODO: Notify
}

engine::helper::RRValue32 View::cam_Y() const { return f_Cam_Y; }
void View::cam_Y(engine::helper::RRValue32 value)
{
    if (f_Cam_Y.equ(value)) return;
    // Set Y-coordinate
    f_Cam_Y = value;
    // Mark dirty
    f_IsDirty = true;
    // TODO: Notify
}

engine::helper::RRValue32 View::cam_Zoom() const { return f_Cam_Zoom; }
void View::cam_Zoom(engine::helper::RRValue32 value)
{
    if (f_Cam_Zoom.equ(value)) return;
    // Set Zoom
    f_Cam_Zoom = value;
    m_Refresh_Size();
    // Mark dirty
    f_IsDirty = true;
    // TODO: Notify
}

#pragma endregion

#pragma region helper functions

void View::m_Refresh_Size()
{
    // f_Cam_Size = 
}

#pragma endregion

#pragma region functions

void View::vblank()
{
    if (!f_IsDirty) return;
    f_IsDirty = false;
    // Update background
    // bgScalef()
    // bgScrollf()
}

#pragma endregion