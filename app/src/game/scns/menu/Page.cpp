#include "game/scns/menu/Page.h"

using namespace game::scns::menu;

#pragma region init

Page::Page(Scene& scene) : f_Scene(scene)
{
    f_status = PageStatus::INIT;
    f_deleteOnExit = false;
}

Page::~Page() { }

#pragma endregion

#pragma region properties

PageStatus Page::status() const { return f_status; }

bool Page::deleteOnExit() const { return f_deleteOnExit; }

void Page::deleteOnExit(bool value) { f_deleteOnExit = value; }

const Scene& Page::scene() const { return f_Scene; }
Scene& Page::scene() { return f_Scene; }

#pragma endregion

#pragma region helper functions

void Page::m_enter() { }

void Page::m_exit() { }

void Page::m_update() { }

void Page::m_vblank() { }

void Page::m__enter()
{
    f_status = PageStatus::ENTERING;
    m_enter();
    f_status = PageStatus::ACTIVE;
}

void Page::m__exit()
{
    f_status = PageStatus::EXITING;
    m_exit();
    f_status = PageStatus::EXITED;
}

void Page::m__update()
{
    m_update();
}

void Page::m__vblank()
{
    m_vblank();
}

#pragma endregion