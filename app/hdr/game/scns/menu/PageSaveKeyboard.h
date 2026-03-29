#include "./PageSaveWidget.h"

#ifndef GAME_SCNS_MENU_PAGESAVEKEYBOARD_H
#define GAME_SCNS_MENU_PAGESAVEKEYBOARD_H

namespace game::scns::menu
{
    /// @brief Represents a keyboard widget in a save page
    class PageSaveKeyboard : public PageSaveWidget
    {
        #pragma region nested

        typedef void (*Input)(PageSaveKeyboard&, Scene&, PageSave&, char);

        struct Key { bool cap; u8 lo; u8 up; u16 off; u16 len; };

        #pragma endregion

        #pragma region init

        public: 

        /// @brief Constructor for PageSaveKeyboard
        /// @param scene Scene
        /// @param page Page
        /// @param action Action
        /// @param input Input action
        PageSaveKeyboard(Scene& scene, PageSave& page, Input input);

        /// @brief Destructor for PageSaveKeyboard
        virtual ~PageSaveKeyboard() override;

        INIT_NODEFCOPYMOVE(PageSaveKeyboard)

        #pragma endregion

        #pragma region fields

        private:

        Input f_Input;

        PageSaveWidget* f_Widget_L;
        PageSaveWidget* f_Widget_R;

        bool f_CapsLock;
        bool f_Shift;

        u16 f_Sel_X;
        u16 f_Sel_Y;
        const Key* f_Sel_Key;

        static constexpr u16 f_Keys_Count = 0x61;
        static const Key f_Keys[];

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

        /// @brief Widget below the left half of the keyboard
        const PageSaveWidget* widget_L() const;
        /// @brief Widget below the left half of the keyboard
        PageSaveWidget* widget_L();
        /// @brief Widget below the left half of the keyboard
        void widget_L(PageSaveWidget* value);

        /// @brief Widget below the right half of the keyboard
        const PageSaveWidget* widget_R() const;
        /// @brief Widget below the right half of the keyboard
        PageSaveWidget* widget_R();
        /// @brief Widget below the right half of the keyboard
        void widget_R(PageSaveWidget* value);

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
        virtual void m_Refresh() override;

        /// @brief Also accessed by PageSave
        virtual void m_Highlight(bool touching) override;

        /// @brief Also accessed by PageSave
        virtual void m_Enter(PageSaveWidget* prev) override;

        /// @brief Also accessed by PageSave
        virtual void m_Exit(PageSaveWidget* next) override;

        /// @brief Also accessed by PageSave
        virtual void m_Touch(u16 touch_X, u16 touch_Y) override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_A() override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_Left() override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_Right() override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_Up() override;

        /// @brief Also accessed by PageSave
        virtual void m_Input_Down() override;

        private:

        u8 m_GetChar(const Key& key);

        void m_Set_Selection(u16 x, u16 y);

        void m_Inc_Selection(u16 x);

        void m_Input();

        #pragma endregion
    };
}

#endif
