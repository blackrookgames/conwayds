#include "engine/gfx/TextGFX.h"
#include "engine/scenes/Scene.h"
#include "./Page.h"

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

        u16* f_Screen_Title;
        size_t f_Screen_Title_Len;

        int f_TScr;
        u16* f_TScr_Map;

        engine::gfx::TextGFX* f_TextGFX;
        std::ostream* f_TextStream;

        Page* f_ActivePage;
        Page* f_NextPage;

        u16 f_Input_Down;
        u16 f_Input_Up;
        u16 f_Input_Held;
        bool f_Input_Touch;
        touchPosition f_Input_Touch_Pos;

        #pragma endregion

        #pragma region properties

        public:

        /// @brief Current keypad pressed state
        u16 input_Down() const;

        /// @brief Current keypad released state 
        u16 input_Up() const;

        /// @brief Current keypad held state
        u16 input_Held() const;

        /// @brief Whether or not the touch screen is currently being touched
        bool input_Touch() const;

        /// @brief Current touch position
        touchPosition input_Touch_Pos() const;

        /// @brief Text graphics handler
        const engine::gfx::TextGFX& textGFX() const;
        /// @brief Text graphics handler
        engine::gfx::TextGFX& textGFX();

        /// @brief Output text stream
        const std::ostream& textStream() const;
        /// @brief Output text stream
        std::ostream& textStream();

        #pragma endregion

        #pragma region helper functions

        protected:

        void m_enter() override;

        void m_exit() override;

        void m_update() override;

        #pragma endregion

        #pragma region functions

        /// @brief Enters the specified page on the next update
        /// @param page Page to enter
        void gotoPage(Page* page);

        #pragma endregion
    };
}

#endif