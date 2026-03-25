#include <nds.h>

#include "engine/helper/_macros.h"
#include "engine/view/View.h"

#ifndef GAME_SCNS_SIM_SIMULATION_H
#define GAME_SCNS_SIM_SIMULATION_H

namespace game::scns::sim
{
    /// @brief Represents a simulation
    class Simulation
    {
        #pragma region init

        public: 

        /// @brief Constructor for Simulation
        /// @param layer Background hardware layer to initialize and use
        /// @param mapBase 2K offset (within VRAM) for tile map
        /// @param tileBase 16K offset (within VRAM) of tile graphics data
        /// @param priority Priority of background layer
        Simulation(int layer, int mapBase, int tileBase, unsigned int priority);

        /// @brief Destructor for Simulation
        virtual ~Simulation();

        INIT_NODEFCOPYMOVE(Simulation)

        #pragma endregion

        #pragma region helper const

        static const engine::helper::RRValue48p16 f_BG_X;
        static const engine::helper::RRValue48p16 f_BG_Y;

        #pragma endregion

        #pragma region const

        public:

        /// @brief Minimum simulation speed (in generations per 4 seconds (roughly))
        static constexpr u32 speed_Min = 1;

        /// @brief Maximum simulation speed (in generations per 4 seconds (roughly))
        static constexpr u32 speed_Max = 128;

        #pragma endregion

        #pragma region fields

        private:

        bool f_IsDirty;
        
        int f_BG;
        u16* f_BG_GFX;
        u16* f_BG_Map;

        engine::view::View* f_View;

        u8* f_Map_Empty;
        u8* f_Map_A;
        u8* f_Map_B;
        u8* f_Map_Ptr;

        u32 f_Speed;
        u32 f_Gen_Length;
        u32 f_Gen_Progress;

        u32 f_Sim_Live;
        u32 f_Sim_Gen;

        #pragma endregion

        #pragma region properties

        public:
        
        /// @brief Background tile graphics
        const u16* bg_GFX() const;
        /// @brief Background tile graphics
        u16* bg_GFX();

        /// @brief Background tilemap
        const u16* bg_Map() const;
        /// @brief Background tilemap
        u16* bg_Map();

        /// @brief View
        const engine::view::View& view() const;
        /// @brief View
        engine::view::View& view();

        /// @brief Simulation speed (in generations per 4 seconds (roughly))
        u32 speed() const;
        /// @brief Simulation speed (in generations per 4 seconds (roughly))
        void speed(u32 value);

        /// @brief Number of live cells
        u32 sim_Live() const;

        /// @brief Current generation
        u32 sim_Gen() const;

        #pragma endregion

        #pragma region helper functions

        private:

        void m_View_FixSize();
        
        void m_View_FixPosition();

        #pragma endregion

        #pragma region functions

        public:

        /// @brief Marks the visuals as "dirty", forcing an update during the next vertical blanking
        void markDirty();

        /// @brief Updates the simulation
        /// @param delta Delta time (in ticks)
        void update(u16 delta);

        /// @brief Call this during the vertical blanking
        void vblank();

        #pragma endregion
    };
}

#endif