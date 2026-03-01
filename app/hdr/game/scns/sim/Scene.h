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

        u8* f_sim_empty;
        u8* f_sim_tiles_a;
        u8* f_sim_tiles_b;
        u8* f_sim_ptr;
        bool f_sim_dirty;
        
        int f_main_3;
        u16* f_main_3_gfx;
        u16* f_main_3_map;
        u8* f_main_3_buffer;

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

        #pragma region properties

        public:

        /// @brief Length of a single cycle
        u32 cycle_length() const;
        /// @brief Length of a single cycle
        void cycle_length(u32 value);

        #pragma endregion

        #pragma region helper functions

        protected:

        void m_enter() override;

        void m_exit() override;

        void m_update() override;

        private:

        void m_update_unpaused(u16 ticks);

        void m_update_paused();

        void m_update_sim();

        void m_update_simtiles();

        void m_update_view_size(s32 size);

        void m_update_scroll();

        #pragma endregion
    };
}

#endif