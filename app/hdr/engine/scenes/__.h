#include "engine/helper/State.h"

#ifndef ENGINE_SCENES____H
#define ENGINE_SCENES____H

namespace engine::scenes
{
#ifndef ENGINE_SCENES_SCENE_H
    class Scene;
#endif

    #pragma region init/final/update

    /// @brief Initializes the scene handler
    void initialize();

    /// @brief Finalizes the scene handler, freeing data
    void finalize();

    /// @brief Updates the scene handler
    void update();

    #pragma endregion

    #pragma region properties

    /// @brief State of the scene handler
    engine::helper::State state();

    /// @brief Active scene
    Scene* activeScene();

    #pragma endregion

    #pragma region methods

    /// @brief Enters the specified scene on the next update
    /// @param scene Scene to enter
    void gotoScene(Scene* scene);

    #pragma endregion
}

#endif
