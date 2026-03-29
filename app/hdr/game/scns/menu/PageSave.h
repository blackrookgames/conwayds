#include <string>

#include "engine/io/Path.h"
#include "./Page.h"
#include "./PageSaveButton.h"
#include "./PageSaveKeyboard.h"
#include "./PageSaveWidget.h"

#ifndef GAME_SCNS_MENU_PAGESAVE_H
#define GAME_SCNS_MENU_PAGESAVE_H

namespace game::scns::menu
{
    /// @brief Represents a page for saving a pattern
    class PageSave : public Page
    {
        #pragma region init

        public: 

        /// @brief Constructor for PageSave
        /// @param scene Scene
        /// @param initialName Initial name
        PageSave(Scene& scene, const std::string* initialName = nullptr);

        /// @brief Destructor for PageSave
        virtual ~PageSave() override;

        INIT_NODEFCOPYMOVE(PageSave)

        #pragma endregion

        #pragma region fields

        private:

        const std::string* f_InitialName;

        u16* f_Screen;
        size_t f_Screen_Len;

        PageSaveWidget** f_Widgets;
        size_t f_Widgets_Count;

        PageSaveButton* f_Widget_OK;
        PageSaveButton* f_Widget_Cancel;
        PageSaveKeyboard* f_Widget_Keyboard;

        PageSaveWidget* f_Widget_Focus;
        PageSaveWidget* f_Widget_Touch;
        bool f_Touching;

        std::string f_Name;

        static std::string f_Chosen;
        static engine::io::Path f_Chosen_Path;

        static constexpr u8 f_BadNames_Count = 22;
        static const std::string f_BadNames[];

        #pragma endregion

        #pragma region properties

        public:

        /// @brief Whether or not the touch screen is being touched
        bool touching() const;

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

        void m_Refresh();

        static void m_OK(PageSaveButton& button, Scene& scene, PageSave& page);

        static void m_Cancel(PageSaveButton& button, Scene& scene, PageSave& page);

        static void m_Input(PageSaveKeyboard& keyboard, Scene& scene, PageSave& page, char chr);

        static void m_Msg_OK(Scene& scene);

        static void m_Msg_Save(Scene& scene);

        static void m_Msg_No(Scene& scene);

        #pragma endregion

        #pragma region functions

        public:

        /// @brief Focus on the specified widget
        /// @param widget Widget to focus on
        void focus(PageSaveWidget* widget);

        #pragma endregion
    };
}

#endif
