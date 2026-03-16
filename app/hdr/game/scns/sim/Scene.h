#include "engine/gfx/TextGFX.h"
#include "engine/scenes/Scene.h"

#include "./Simulation.h"

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

        bool f_Paused;

        u16* f_Screen_Main;
        size_t f_Screen_Main_Len;
        u16* f_Screen_Pause;
        size_t f_Screen_Pause_Len;

        engine::gfx::TextGFX* f_TextGFX;
        std::ostream* f_TextStream;
        Simulation* f_Simulation;
        touchPosition f_TouchPos;

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