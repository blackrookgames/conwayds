#include "engine/gfx/TextGFX.h"
#include "engine/scenes/Scene.h"

#ifndef GAME_SCNS_MENU_SCENE_H
#define GAME_SCNS_MENU_SCENE_H

namespace game::scns::menu
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

        u16* f_Screen_Main;
        size_t f_Screen_Main_Len;
        u16* f_Screen_Title;
        size_t f_Screen_Title_Len;

        int f_TScr;
        u16* f_TScr_Map;

        engine::gfx::TextGFX* f_BScr_TextGFX;
        std::ostream* f_BScr_TextStream;
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