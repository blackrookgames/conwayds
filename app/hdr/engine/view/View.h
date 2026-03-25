#include <nds.h>

#include "engine/helper/_macros.h"
#include "engine/helper/RRValue48p16.h"

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
        /// @note Y-coordinates increase upward
        View(int bg, engine::helper::RRValue48p16 bg_X, engine::helper::RRValue48p16 bg_Y);

        /// @brief Destructor for View
        virtual ~View();

        INIT_NODEFCOPYMOVE(View)

        #pragma endregion

        #pragma region helper const

        private:

        static const engine::helper::RRValue48p16 f_2;

        static const engine::helper::RRValue48p16 f_Zoom_Min;
        static const engine::helper::RRValue48p16 f_Zoom_Max;
        static const engine::helper::RRValue48p16 f_DS_Width;
        static const engine::helper::RRValue48p16 f_DS_Height;

        #pragma endregion

        #pragma region const

        public:

        /// @brief Horizontal span at 100%
        static const engine::helper::RRValue48p16 hSpan_100;
        /// @brief Zoom value of 100%
        static const engine::helper::RRValue48p16 zoom_100;
        
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
        engine::helper::RRValue48p16 f_BG_X;
        engine::helper::RRValue48p16 f_BG_Y;
        
        engine::helper::RRValue48p16 f_Cam_X;
        engine::helper::RRValue48p16 f_Cam_Y;
        engine::helper::RRValue48p16 f_Cam_Zoom;

        engine::helper::RRValue48p16 f_Cam_HSpan;
        engine::helper::RRValue48p16 f_Cam_VSpan;
        engine::helper::RRValue48p16 f_Cam_Ortho_Width;
        engine::helper::RRValue48p16 f_Cam_Ortho_Height;

        engine::helper::RRValue48p16 f_Cam_X0;
        engine::helper::RRValue48p16 f_Cam_Y0;
        engine::helper::RRValue48p16 f_Cam_X1;
        engine::helper::RRValue48p16 f_Cam_Y1;
        
        #pragma endregion

        #pragma region properties
        
        public:

        /// @brief Camera X-coordinate
        engine::helper::RRValue48p16 cam_X() const;
        /// @brief Camera X-coordinate
        void cam_X(engine::helper::RRValue48p16 value);
        
        /// @brief Camera Y-coordinate
        engine::helper::RRValue48p16 cam_Y() const;
        /// @brief Camera Y-coordinate
        void cam_Y(engine::helper::RRValue48p16 value);
        
        /// @brief Camera zoom percentage
        engine::helper::RRValue48p16 cam_Zoom() const;
        /// @brief Camera zoom percentage
        void cam_Zoom(engine::helper::RRValue48p16 value);

        /// @brief Camera horizontal span
        engine::helper::RRValue48p16 cam_HSpan() const;

        /// @brief Camera vertical span
        engine::helper::RRValue48p16 cam_VSpan() const;

        /// @brief Camera orthographic width
        engine::helper::RRValue48p16 cam_Ortho_Width() const;

        /// @brief Camera orthographic height
        engine::helper::RRValue48p16 cam_Ortho_Height() const;

        /// @brief X-coordinate of top-left edge of a camera
        engine::helper::RRValue48p16 cam_X0() const;

        /// @brief Y-coordinate of top-left edge of a camera
        engine::helper::RRValue48p16 cam_Y0() const;

        /// @brief X-coordinate of bottom-right edge of a camera
        engine::helper::RRValue48p16 cam_X1() const;

        /// @brief Y-coordinate of bottom-right edge of a camera
        engine::helper::RRValue48p16 cam_Y1() const;

        #pragma endregion

        #pragma region helper functions

        private:

        void m_Refresh();

        void m_Refresh_Size();

        void m_Refresh_Position();
        
        #pragma endregion

        #pragma region functions

        public:

        /// @brief Call this during the vertical blanking
        void vblank();

        #pragma endregion
    };
}

#endif
