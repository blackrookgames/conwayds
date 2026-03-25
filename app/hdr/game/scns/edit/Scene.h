#include "engine/gfx/TextGFX.h"
#include "engine/scenes/Scene.h"

#include "./Editor.h"
#include "./Tool.h"

#ifndef GAME_SCNS_EDIT_SCENE_H
#define GAME_SCNS_EDIT_SCENE_H

namespace game::scns::edit
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

        #pragma region helper const

        static const engine::helper::RRValue48p16 f_0;
        static const engine::helper::RRValue48p16 f_1;

        static const engine::helper::RRValue48p16 f_Inc_Pos;
        static const engine::helper::RRValue48p16 f_Inc_Zoom;
        
        static const engine::helper::RRValue48p16 f_DS_Width;
        static const engine::helper::RRValue48p16 f_DS_Height;
        
        static const engine::helper::RRValue48p16 f_Pattern_Cols;
        static const engine::helper::RRValue48p16 f_Pattern_Rows;
        static const engine::helper::RRValue48p16 f_Pattern_Last_Col;
        static const engine::helper::RRValue48p16 f_Pattern_Last_Row;

        #pragma endregion

        #pragma region fields

        private:

        u16* f_Screen_Main;
        size_t f_Screen_Main_Len;

        engine::gfx::TextGFX* f_TextGFX;
        std::ostream* f_TextStream;
        Editor* f_Editor;
        touchPosition f_TouchPos;

        Tool f_Tool;

        #pragma endregion

        #pragma region helper functions

        protected:

        void m_enter() override;

        void m_exit() override;

        void m_update() override;

        private:

        void m_Refresh_ToolDisplay();

        #pragma endregion
    };
}

#endif