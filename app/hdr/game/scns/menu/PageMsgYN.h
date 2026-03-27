#include <string>

#include "./Page.h"

#ifndef GAME_SCNS_MENU_PAGEMSGYN_H
#define GAME_SCNS_MENU_PAGEMSGYN_H

namespace game::scns::menu
{
    /// @brief Represents a message that prompts the user to press Yes or No
    class PageMsgYN : public Page
    {
        #pragma region nested

        typedef void (*ButtonAction)(Scene&);

        #pragma endregion

        #pragma region init

        public: 

        /// @brief Constructor for PageMsgYN
        /// @param scene Scene
        /// @param msg Message text
        /// @param yes Action performed when user presses the Yes button
        /// @param no Action performed when user presses the No button
        PageMsgYN(Scene& scene, std::string msg, ButtonAction yes, ButtonAction no);

        /// @brief Destructor for PageMsgYN
        virtual ~PageMsgYN() override;

        INIT_NODEFCOPYMOVE(PageMsgYN)

        #pragma endregion

        #pragma region fields

        private:

        std::string f_Msg;
        ButtonAction f_Yes;
        ButtonAction f_No;

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
        
        void m_Print_Text(u16& x, u16& y, const char* beg, const char* end, char endChar);

        void m_Button_Action();

        void m_Refresh_Msg();

        void m_Refresh_Buttons();

        #pragma endregion
    };
}

#endif
