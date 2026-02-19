#include "engine/scenes/Scene.h"

using namespace engine::scenes;

#pragma region init

Scene::Scene()
{
    f_status = SceneStatus::INIT;
    f_deleteOnExit = false;
}

Scene::~Scene() { }

#pragma endregion

#pragma region properties

SceneStatus Scene::status() const { return f_status; }

bool Scene::deleteOnExit() const { return f_deleteOnExit; }

void Scene::deleteOnExit(bool value) { f_deleteOnExit = value; }

#pragma endregion

#pragma region helper functions

void Scene::m_enter() { }

void Scene::m_exit() { }

void Scene::m_update() { }

void Scene::m__enter()
{
    f_status = SceneStatus::ENTERING;
    m_enter();
    f_status = SceneStatus::ACTIVE;
}

void Scene::m__exit()
{
    f_status = SceneStatus::EXITING;
    m_exit();
    f_status = SceneStatus::EXITED;
}

void Scene::m__update()
{
    m_update();
}

#pragma endregion