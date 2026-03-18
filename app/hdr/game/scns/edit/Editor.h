#include <nds.h>

#include "engine/data/Pattern.h"
#include "engine/helper/_macros.h"

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

        #pragma region fields

        private:

        bool f_IsDirty;
        
        int f_BG;
        u16* f_BG_GFX;
        u16* f_BG_Map;
        u8* f_BG_Buffer_A;
        u8* f_BG_Buffer_B;
        u8* f_BG_Buffer_Ptr;

        s32 f_View_Zoom;
        s32 f_View_X;
        s32 f_View_Y;
        s32 f_View_W;
        s32 f_View_H;
        s32 f_View_Min_X;
        s32 f_View_Min_Y;
        s32 f_View_Max_X;
        s32 f_View_Max_Y;

        engine::data::Pattern f_Pattern;

        bool f_Grid;

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

        /// @brief Whether or not the grid is enabled
        bool grid() const;
        /// @brief Whether or not the grid is enabled
        void grid(bool value);

        #pragma endregion

        #pragma region helper functions

        private:

        void m_Refresh_View();

        void m_Refresh_Buffer_Ptr();

        void m_Redraw_Buffer();

        #pragma endregion

        #pragma region functions

        public:

        /// @brief Marks the visuals as "dirty", forcing an update during the next vertical blanking
        void markDirty();

        /// @brief Call this during the vertical blanking
        void vblank();

        /// @brief Saves the current pattern
        void savePattern();

        #pragma endregion
    };
}

#endif