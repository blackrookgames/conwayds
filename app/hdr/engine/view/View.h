#include <nds.h>

#include "engine/helper/_macros.h"
#include "engine/helper/RRValue32.h"

#ifndef ENGINE_VIEW_VIEW_H
#define ENGINE_VIEW_VIEW_H

namespace engine::view
{
    /// @brief
    /// Represents a scene
    class View
    {
        #pragma region init

        public: 

        /// @brief Constructor for View
        /// @param bg Background
        /// @param bg_X X-coordinate of background offset (in world)
        /// @param bg_Y X-coordinate of background offset (in world)
        View(int bg, engine::helper::RRValue32 bg_X, engine::helper::RRValue32 bg_Y);

        /// @brief Destructor for View
        virtual ~View();

        INIT_NODEFCOPYMOVE(View)

        #pragma endregion

        #pragma region fields

        private:

        bool f_IsDirty;

        int f_BG;
        engine::helper::RRValue32 f_BG_X;
        engine::helper::RRValue32 f_BG_Y;
        
        engine::helper::RRValue32 f_Cam_X;
        engine::helper::RRValue32 f_Cam_Y;
        engine::helper::RRValue32 f_Cam_Zoom;

        engine::helper::RRValue32 f_Cam_Size;
        
        #pragma endregion

        #pragma region properties
        
        public:

        /// @brief Camera X-coordinate
        engine::helper::RRValue32 cam_X() const;
        /// @brief Camera X-coordinate
        void cam_X(engine::helper::RRValue32 value);
        
        /// @brief Camera Y-coordinate
        engine::helper::RRValue32 cam_Y() const;
        /// @brief Camera Y-coordinate
        void cam_Y(engine::helper::RRValue32 value);
        
        /// @brief Camera zoom percentage (x256)
        engine::helper::RRValue32 cam_Zoom() const;
        /// @brief Camera zoom percentage (x256)
        void cam_Zoom(engine::helper::RRValue32 value);
        
        #pragma endregion

        #pragma region helper functions

        private:

        void m_Refresh_Size();
        
        #pragma endregion

        #pragma region functions

        public:

        /// @brief Call this during the vertical blanking
        void vblank();

        #pragma endregion
    };
}

#endif
