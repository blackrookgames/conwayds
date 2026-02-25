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

        s32 f_view_w;
        s32 f_view_h;
        s32 f_view_max_x;
        s32 f_view_max_y;
        s32 f_view_inc;

        s32 f_view_x;
        s32 f_view_y;

        bool f_paused;

        u32 f_cycle_length;
        u32 f_cycle_progress;

        #pragma endregion

        #pragma region helper functions

        protected:

        void m_enter() override;

        void m_exit() override;

        void m_update() override;

        private:

        void m_update_unpaused(u16 ticks);

        void m_update_paused();

        void m_update_view_size(s32 size);

        #pragma endregion
    };
}

#endif