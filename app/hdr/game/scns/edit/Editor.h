#include <nds.h>

#include "engine/data/Pattern.h"
#include "engine/helper/_macros.h"
#include "engine/view/View.h"

#ifndef GAME_SCNS_EDIT_EDITOR_H
#define GAME_SCNS_EDIT_EDITOR_H

namespace game::scns::edit
{
    /// @brief Represents an editor
    class Editor
    {
        #pragma region init

        public: 

        /// @brief Constructor for Editor
        /// @param layer Background hardware layer to initialize and use
        /// @param mapBase 2K offset (within VRAM) for tile map
        /// @param tileBase 16K offset (within VRAM) of tile graphics data
        /// @param priority Priority of background layer
        Editor(int layer, int mapBase, int tileBase, unsigned int priority);

        /// @brief Destructor for Editor
        virtual ~Editor();

        INIT_NODEFCOPYMOVE(Editor)

        #pragma endregion

        #pragma region helper const

        static const engine::helper::RRValue48p16 f_Zoom_Grid;

        #pragma endregion

        #pragma region const
        
        /// @brief X-coordinate of bottom-left corner
        static const engine::helper::RRValue48p16 bound_X0;
        /// @brief Y-coordinate of bottom-left corner
        static const engine::helper::RRValue48p16 bound_Y0;
        /// @brief X-coordinate of top-right corner
        static const engine::helper::RRValue48p16 bound_X1;
        /// @brief Y-coordinate of top-right corner
        static const engine::helper::RRValue48p16 bound_Y1;

        #pragma endregion

        #pragma region fields

        private:

        bool f_IsDirty;
        
        int f_BG;
        u16* f_BG_GFX;
        u16* f_BG_Map;
        u8* f_BG_Buffer_A;
        u8* f_BG_Buffer_B;
        u8* f_BG_Buffer_Ptr;

        engine::view::View* f_View;

        engine::data::Pattern f_Pattern;

        bool f_Grid;

        u32 f_NumLive;

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

        /// @brief Zoom value of view
        engine::helper::RRValue48p16 view_Zoom() const;
        /// @brief Zoom value of view
        void view_Zoom(engine::helper::RRValue48p16 value);

        /// @brief X-coordinate of view
        engine::helper::RRValue48p16 view_X() const;
        /// @brief X-coordinate of view
        void view_X(engine::helper::RRValue48p16 value);

        /// @brief Y-coordinate of view
        /// @note Y-coordinate increases upward
        engine::helper::RRValue48p16 view_Y() const;
        /// @brief Y-coordinate of view
        /// @note Y-coordinate increases upward
        void view_Y(engine::helper::RRValue48p16 value);

        /// @brief Whether or not the grid is enabled
        bool grid() const;
        /// @brief Whether or not the grid is enabled
        void grid(bool value);

        /// @brief Number of live cells
        u32 numLive() const;

        #pragma endregion

        #pragma region helper functions

        private:

        void m_Refresh_Buffer_Ptr();

        void m_Force_NumLive();

        void m_Force_Buffer();

        #pragma endregion

        #pragma region functions

        public:

        /// @brief Marks the visuals as "dirty", forcing an update during the next vertical blanking
        void markDirty();

        /// @brief Call this during the vertical blanking
        void vblank();

        /// @brief Saves the current pattern
        void savePattern();

        /// @brief Gets the cell at the specified coordinates
        /// @param x X-coordinate
        /// @param y Y-coordinate
        /// @return Cell at the specified coordinates
        bool getcell(u16 x, u16 y) const;

        /// @brief Sets the cell at the specified coordinates
        /// @param x X-coordinate
        /// @param y Y-coordinate
        /// @param live Whether or not the cell is alive
        void setcell(u16 x, u16 y, bool live);

        #pragma endregion
    };
}

#endif