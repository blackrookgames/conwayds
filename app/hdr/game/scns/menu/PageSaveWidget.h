#include <nds.h>

#include "engine/helper/_macros.h"

#ifndef GAME_SCNS_MENU_PAGESAVEWIDGET_H
#define GAME_SCNS_MENU_PAGESAVEWIDGET_H

namespace game::scns::menu
{
#ifndef GAME_SCNS_MENU_PAGESAVE_H
    class PageSave;
#endif

#ifndef GAME_SCNS_MENU_SCENE_H
    class Scene;
#endif

    /// @brief Represents a widget in a save page
    class PageSaveWidget 
    {
        #pragma region init

        public: 

        /// @brief Constructor for PageSaveWidget
        /// @param scene Scene
        /// @param page Page
        PageSaveWidget(Scene& scene, PageSave& page);

        /// @brief Destructor for PageSaveWidget
        virtual ~PageSaveWidget();

        INIT_NODEFCOPYMOVE(PageSaveWidget)

        #pragma endregion

        #pragma region friends

        friend PageSave;

        #pragma endregion

        #pragma region fields

        private:
        
        Scene& f_Scene;
        PageSave& f_Page;

        #pragma endregion

        #pragma region helper properties

        protected:
        
        const Scene& p_Scene() const;
        Scene& p_Scene();
        
        const PageSave& p_Page() const;
        PageSave& p_Page();
        
        /// @brief Also accessed by PageSave
        virtual u16 p_x0() const;
        
        /// @brief Also accessed by PageSave
        virtual u16 p_y0() const;

        /// @brief Also accessed by PageSave
        virtual u16 p_x1() const;

        /// @brief Also accessed by PageSave
        virtual u16 p_y1() const;

        #pragma endregion

        #pragma region properties

        public:

        /// @brief X-coordinate of top-left tile
        virtual u16 x() const;
        
        /// @brief Y-coordinate of top-left tile
        virtual u16 y() const;

        /// @brief Width (in tiles)
        virtual u16 w() const;

        /// @brief Height (in tiles)
        virtual u16 h() const;

        #pragma endregion

        #pragma region helper functions

        protected:

        /// @brief Also accessed by PageSave
        virtual void m_Refresh();

        /// @brief Also accessed by PageSave
        virtual void m_Highlight(bool touching);

        /// @brief Also accessed by PageSave
        virtual void m_Enter(PageSaveWidget* prev);

        /// @brief Also accessed by PageSave
        virtual void m_Exit(PageSaveWidget* next);

        /// @brief Also accessed by PageSave
        virtual void m_Action();

        /// @brief Also accessed by PageSave
        virtual void m_Touch(u16 touch_X, u16 touch_Y);

        /// @brief Also accessed by PageSave
        virtual void m_Input_A();

        /// @brief Also accessed by PageSave
        virtual void m_Input_Left();

        /// @brief Also accessed by PageSave
        virtual void m_Input_Right();

        /// @brief Also accessed by PageSave
        virtual void m_Input_Up();

        /// @brief Also accessed by PageSave
        virtual void m_Input_Down();

        #pragma endregion
    };
}

#endif
