#include "./Page.h"

#ifndef GAME_SCNS_MENU_PAGEMAIN_H
#define GAME_SCNS_MENU_PAGEMAIN_H

namespace game::scns::menu
{
    /// @brief Represents a menu page
    class PageMain : public Page
    {
        #pragma region init

        public: 

        /// @brief Constructor for PageMain
        /// @param scene Scene
        PageMain(Scene& scene);

        /// @brief Destructor for PageMain
        virtual ~PageMain() override;

        INIT_NODEFCOPYMOVE(PageMain)

        #pragma endregion

        #pragma region fields

        private:

        u16* f_Screen;
        size_t f_Screen_Len;

        u16 f_Sel_Index;
        u16 f_Sel_Touch;
        bool f_Sel_Touching;

        #pragma endregion

        #pragma region helper functions

        protected:

        /// @brief Called when entering the page
        virtual void m_enter() override;

        /// @brief Called when exiting the page
        virtual void m_exit() override;

        /// @brief Called when updating the page
        virtual void m_update() override;

        /// @brief Called during vblank
        virtual void m_vblank() override;

        private:

        void m_Close();

        void m_Button_Action();

        void m_Refresh_Buttons();

        #pragma endregion
    };
}

#endif
