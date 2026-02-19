#include "./__.h"

#include "engine/helper/_macros.h"
#include "./SceneStatus.h"

#include <nds.h>

#ifndef ENGINE_SCENES_SCENE_H
#define ENGINE_SCENES_SCENE_H

namespace engine::scenes
{
    /// @brief
    /// Represents a scene
    class Scene
    {
        #pragma region init

        public: 

        /// @brief
        /// Constructor for Scene
        Scene();

        /// @brief
        /// Destructor for Scene
        virtual ~Scene();

        INIT_NOCOPYMOVE(Scene)

        #pragma endregion

        #pragma region friends

        friend void finalize();
        friend void update();

        #pragma endregion

        #pragma region fields

        private:

        SceneStatus f_status;
        bool f_deleteOnExit;
        
        #pragma endregion

        #pragma region properties

        public:

        /// @brief Status of the scene
        SceneStatus status() const;

        /// @brief Whether or not to delete the scene when exited 
        bool deleteOnExit() const;
        
        /// @brief Whether or not to delete the scene when exited 
        void deleteOnExit(bool value);
        
        #pragma endregion

        #pragma region helper functions

        protected:

        /// @brief
        /// Called when entering the scene
        virtual void m_enter();

        /// @brief
        /// Called when exiting the scene
        virtual void m_exit();

        /// @brief
        /// Called when updating the scene
        virtual void m_update();

        private:

        /// @brief
        /// Also accessed by ./__.h
        void m__enter();

        /// @brief
        /// Also accessed by ./__.h
        void m__exit();

        /// @brief
        /// Also accessed by ./__.h
        void m__update();

        #pragma endregion
    };
}

#endif
