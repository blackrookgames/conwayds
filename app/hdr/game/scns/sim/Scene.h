#include "engine/scenes/Scene.h"

#ifndef GAME_SCNS_SIM_SCENE_H
#define GAME_SCNS_SIM_SCENE_H

namespace game::scns::sim
{
    /// @brief Represents a simulation scene
    class Scene : public engine::scenes::Scene
    {
        #pragma region init

        public: 

        /// @brief Constructor for Scene
        Scene();

        /// @brief Destructor for Scene
        virtual ~Scene() override;

        INIT_NOCOPYMOVE(Scene)

        #pragma endregion

        #pragma region fields

        private:

        int f_main_3;
        u16* f_main_3_gfx;
        u16* f_main_3_map;

        s32 f_scale;

        #pragma endregion

        #pragma region helper functions

        protected:

        void m_enter() override;

        void m_exit() override;

        void m_update() override;

        #pragma endregion
    };
}

#endif