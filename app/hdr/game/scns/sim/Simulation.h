#include <nds.h>

#include "engine/helper/_macros.h"

#ifndef GAME_SCNS_SIM_SIM_H
#define GAME_SCNS_SIM_SIM_H

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

        #pragma region fields

        private:

        bool f_IsDirty;
        
        int f_BG;
        u16* f_BG_GFX;
        u16* f_BG_Map;

        s32 f_View_Zoom;
        s32 f_View_X;
        s32 f_View_Y;
        s32 f_View_W;
        s32 f_View_H;
        s32 f_View_Min_X;
        s32 f_View_Min_Y;
        s32 f_View_Max_X;
        s32 f_View_Max_Y;

        u8* f_Map_Empty;
        u8* f_Map_A;
        u8* f_Map_B;
        u8* f_Map_Ptr;

        u32 f_Cycle_Length;
        u32 f_Cycle_Progress;

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

        /// @brief Zoom value of view
        s32 view_Zoom() const;
        /// @brief Zoom value of view
        void view_Zoom(s32 value);

        /// @brief X-coordinate of view
        s32 view_X() const;
        /// @brief X-coordinate of view
        void view_X(s32 value);

        /// @brief Y-coordinate of view
        s32 view_Y() const;
        /// @brief Y-coordinate of view
        void view_Y(s32 value);

        /// @brief View width
        s32 view_W() const;

        /// @brief View height
        s32 view_H() const;

        /// @brief Maximum X-coordinate of view
        s32 view_Max_X() const;

        /// @brief Maximum Y-coordinate of view
        s32 view_Max_Y() const;

        /// @brief Length of a single cycle
        u32 cycle_Length() const;
        /// @brief Length of a single cycle
        void cycle_Length(u32 value);

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