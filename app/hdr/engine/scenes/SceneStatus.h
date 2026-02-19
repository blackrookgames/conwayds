#ifndef ENGINE_SCENES_SCENESTATUS_H
#define ENGINE_SCENES_SCENESTATUS_H

namespace engine::scenes
{
    /// @brief
    /// Represents the status of a scene
    enum struct SceneStatus
    {
        /// @brief
        /// Scene has been initialized
        INIT,
        /// @brief
        /// Scene is being entered
        ENTERING,
        /// @brief 
        /// Scene is the active scene
        ACTIVE,
        /// @brief 
        /// Scene is being exited
        EXITING,
        /// @brief 
        /// Scene has been exited
        EXITED,
    };
}

#endif
