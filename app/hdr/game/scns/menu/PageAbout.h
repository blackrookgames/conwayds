#include <sstream>
#include <vector>

#include "engine/io/Path.h"
#include "game/assets/MenuAboutT.h"
#include "game/assets/MenuAboutB.h"
#include "./Page.h"

#ifndef GAME_SCNS_MENU_PAGEABOUT_H
#define GAME_SCNS_MENU_PAGEABOUT_H

namespace game::scns::menu
{
    /// @brief Represents a page about the app
    class PageAbout : public Page
    {
        #pragma region init

        struct Character { char value; bool escape; };

        #pragma endregion
        
        #pragma region init

        public: 

        /// @brief Constructor for PageAbout
        /// @param scene Scene
        PageAbout(Scene& scene);

        /// @brief Destructor for PageAbout
        virtual ~PageAbout() override;

        INIT_NODEFCOPYMOVE(PageAbout)

        #pragma endregion

        #pragma region helper const

        private:
        
        static constexpr size_t f_Msg_Height = 
            (DS_SCREEN_ROWS - game::assets::MenuAboutT::msg_beg) +
            game::assets::MenuAboutB::msg_end;
        static constexpr u16 f_Msg_Beg = 
            game::assets::MenuAboutT::msg_beg * DS_SCREEN_COLS;
        static constexpr u16 f_Msg_End = 
            game::assets::MenuAboutB::msg_end * DS_SCREEN_COLS;

        #pragma endregion

        #pragma region fields

        private:

        u16* f_ScreenT;
        size_t f_ScreenT_Len;
        u16* f_ScreenB;
        size_t f_ScreenB_Len;

        size_t f_Texts_Count;
        std::string* f_Texts_Title;
        std::string* f_Texts_Content;

        u8 f_But_Index;
        u8 f_But_Touch;

        u8 f_Tch_Index;
        u8 f_Tch_Touch;

        bool f_Touching;

        size_t f_TextIndex;

        std::string f_Title;

        u16* f_Content;
        size_t f_Content_Height;
        size_t f_Content_Size;

        size_t f_View_Offset;

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

        static u8 m_GetTouched(u16 tile_X, u16 tile_Y, 
            const u16* btns_X, const u16* btns_Y, u16 btns_W, u16 btns_H, u8 btns_Count);

        private:
        
        static void m_Add_Word(
            std::vector<std::string>& lines, std::ostringstream& os, size_t& lineLen, 
            std::string::const_iterator beg, std::string::const_iterator end, char endChar);

        /// @brief Assume
        /// @brief - Each string has a length <= DS_SCREEN_COLS
        static std::vector<std::string> m_TextToLines(const std::string& text);

        static void m_GetTexts(size_t& texts_Count, std::string*& texts_Title, std::string*& texts_Content);

        static bool m_GetTexts_ParseLine(const char* beg, const char* end, std::string& title, std::string& content);
        
        static bool m_GetTexts_ReadSegment(const char*& ptr, const char* end, std::ostringstream& os);
        
        static Character m_GetTexts_ReadChar(const char*& ptr, const char* end);

        void m_Refresh();

        void m_Refresh_Buttons();

        void m_Close();

        void m_SetContent(const std::string& text);

        void m_ButtonAction();

        void m_Set_TextIndex(size_t value);

        void m_View_Inc(size_t amount);

        void m_View_Dec(size_t amount);

        void m_PageNav();

        #pragma endregion
    };
}

#endif
