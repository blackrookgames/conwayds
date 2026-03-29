#include "./PageSaveWidget.h"

#ifndef GAME_SCNS_MENU_PAGESAVEBUTTON_H
#define GAME_SCNS_MENU_PAGESAVEBUTTON_H

namespace game::scns::menu
{
    /// @brief Represents a button widget in a save page
    class PageSaveButton : public PageSaveWidget
    {
        #pragma region nested

        typedef void (*Action)(PageSaveButton&, Scene&, PageSave&);

        #pragma endregion

        #pragma region init

        public: 

        /// @brief Constructor for PageSaveButton
        /// @param scene Scene
        /// @param page Page
        /// @param action Action
        /// @param x X-coordinate of top-left tile
        /// @param y Y-coordinate of top-left tile
        /// @param w Width (in tiles)
        /// @param h Height (in tiles)
        /// @param action Action
        PageSaveButton(Scene& scene, PageSave& page, Action action, u16 x, u16 y, u16 w, u16 h);

        /// @brief Destructor for PageSaveButton
        virtual ~PageSaveButton() override;

        INIT_NODEFCOPYMOVE(PageSaveButton)

        #pragma endregion

        #pragma region fields

        private:

        Action f_Action;

        PageSaveWidget* f_Widget_L;
        PageSaveWidget* f_Widget_R;
        PageSaveWidget* f_Widget_U;
        PageSaveWidget* f_Widget_D;

        u16 f_X;
        u16 f_Y;
        u16 f_W;
        u16 f_H;
        
        u16 f_X0;
        u16 f_Y0;
        u16 f_X1;
        u16 f_Y1;

        #pragma endregion

        #pragma region helper properties

        protected:
        
        /// @brief Also accessed by PageSave
        virtual u16 p_x0() const override;
        
        /// @brief Also accessed by PageSave
        virtual u16 p_y0() const override;

        /// @brief Also accessed by PageSave
        virtual u16 p_x1() const override;

        /// @brief Also accessed by PageSave
        virtual u16 p_y1() const override;

        #pragma endregion

        #pragma region properties

        public:

        /// @brief Widget to give focus to when the left direction button is pressed
        const PageSaveWidget* widget_L() const;
        /// @brief Widget to give focus to when the left direction button is pressed
        PageSaveWidget* widget_L();
        /// @brief Widget to give focus to when the left direction button is pressed
        void widget_L(PageSaveWidget* value);

        /// @brief Widget to give focus to when the right direction button is pressed
        const PageSaveWidget* widget_R() const;
        /// @brief Widget to give focus to when the right direction button is pressed
        PageSaveWidget* widget_R();
        /// @brief Widget to give focus to when the right direction button is pressed
        void widget_R(PageSaveWidget* value);

        /// @brief Widget to give focus to when the up direction button is pressed
        const PageSaveWidget* widget_U() const;
        /// @brief Widget to give focus to when the up direction button is pressed
        PageSaveWidget* widget_U();
        /// @brief Widget to give focus to when the up direction button is pressed
        void widget_U(PageSaveWidget* value);

        /// @brief Widget to give focus to when the down direction button is pressed
        const PageSaveWidget* widget_D() const;
        /// @brief Widget to give focus to when the down direction button is pressed
        PageSaveWidget* widget_D();
        /// @brief Widget to give focus to when the down direction button is pressed
        void widget_D(PageSaveWidget* value);

        /// @brief X-coordinate of top-left tile
        virtual u16 x() const override;
        
        /// @brief Y-coordinate of top-left tile
        virtual u16 y() const override;

        /// @brief Width (in tiles)
        virtual u16 w() const override;

        /// @brief Height (in tiles)
        virtual u16 h() const override;

        #pragma endregion

        #pragma region helper functions

        protected:

        /// @brief Also accessed by PageSave
        virtual void m_Highlight(bool touching) override;

        /// @brief Also accessed by PageSave
        virtual void m_Action() override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_Left() override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_Right() override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_Up() override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_Down() override;

        #pragma endregion
    };
}

#endif
