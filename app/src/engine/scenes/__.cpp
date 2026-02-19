#include "engine/scenes/__.h"

#include "engine/scenes/Scene.h"

using namespace engine;
using namespace engine::scenes;

#pragma region macros

#define SCENE_ENTER \
    /* Enter scene */ \
    f_nextScene->m__enter(); \
    /* Set pointer for active scene */ \
    f_activeScene = f_nextScene; \
    /* Reset pointer for next scene */ \
    f_nextScene = nullptr;

#define SCENE_EXIT \
    /* Exit scene */ \
    f_activeScene->m__exit(); \
    /* Delete if requested*/ \
    if (f_activeScene->deleteOnExit()) delete f_activeScene; \
    /* Reset pointer for active scene */ \
    f_activeScene = nullptr;

#pragma endregion

#pragma region variables

helper::State f_state = helper::State::NOTRUN;
Scene* f_activeScene = nullptr;
Scene* f_nextScene = nullptr;

#pragma endregion

#pragma region init/final/update

void engine::scenes::initialize()
{
    if (f_state != helper::State::NOTRUN) return;
    f_state = helper::State::INIT;
    // Success!!!
    f_state = helper::State::RUN;
}

void engine::scenes::finalize()
{
    if (f_state != helper::State::RUN) return;
    f_state = helper::State::FINAL;
    // Exit active scene
    if (f_activeScene) { SCENE_EXIT }
    // Success!!!
    f_state = helper::State::NOTRUN;
}

void engine::scenes::update()
{
    if (f_state != helper::State::RUN) return;
    // Switch scenes (if requested)
    if (f_nextScene)
    {
        // Exit active scene
        if (f_activeScene) { SCENE_EXIT }
        // Enter next scene
        SCENE_ENTER
    }
    // Update scene
    if (f_activeScene) f_activeScene->m__update();
}

#pragma endregion

#pragma region properties

helper::State engine::scenes::state() { return f_state; }

Scene* engine::scenes::activeScene() { return f_activeScene; }

#pragma endregion

#pragma region methods

void engine::scenes::gotoScene(Scene* scene)
{
    f_nextScene = scene;
}

#pragma endregion