#include <string>

#include "./Page.h"

#ifndef GAME_SCNS_MENU_PAGEMSGOK_H
#define GAME_SCNS_MENU_PAGEMSGOK_H

namespace game::scns::menu
{
    /// @brief Represents a message that prompts the user to press Yes or No
    class PageMsgOK : public Page
    {
        #pragma region nested

        typedef void (*ButtonAction)(Scene&);

        #pragma endregion

        #pragma region init

        public: 

        /// @brief Constructor for PageMsgOK
        /// @param scene Scene
        /// @param msg Message text
        /// @param action Action performed when user presses OK
        PageMsgOK(Scene& scene, std::string msg, ButtonAction action);

        /// @brief Destructor for PageMsgOK
        virtual ~PageMsgOK() override;

        INIT_NODEFCOPYMOVE(PageMsgOK)

        #pragma endregion

        #pragma region fields

        private:

        std::string f_Msg;
        ButtonAction f_Action;

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

        void m_Refresh_Msg();

        void m_Refresh_Buttons();

        #pragma endregion
    };
}

#endif
