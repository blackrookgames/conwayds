#include "engine/io/Path.h"
#include "./Page.h"

#ifndef GAME_SCNS_MENU_PAGELOAD_H
#define GAME_SCNS_MENU_PAGELOAD_H

namespace game::scns::menu
{
    /// @brief Represents a page for loading a pattern
    class PageLoad : public Page
    {
        #pragma region nested

        typedef void (*ButtonAction)(Scene&);

        #pragma endregion

        #pragma region init

        public: 

        /// @brief Constructor for PageLoad
        /// @param scene Scene
        /// @param initialPath Initial path
        PageLoad(Scene& scene, engine::io::Path* initialPath = nullptr);

        /// @brief Destructor for PageLoad
        virtual ~PageLoad() override;

        INIT_NODEFCOPYMOVE(PageLoad)

        #pragma endregion

        #pragma region fields

        private:

        engine::io::Path* f_InitialPath;

        u16* f_Screen;
        size_t f_Screen_Len;

        u16 f_But_Index;
        u16 f_But_Touch;
        u16 f_But_Touch_Down;
        bool f_But_Touching;
        
        engine::io::Path* f_List;
        u16 f_List_Count;
        u16 f_List_Index;
        u16 f_List_Offset;

        static engine::io::Path f_Chosen;

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

        void m_Button_Action(u16 index);

        void m_Refresh_List();

        void m_Refresh_Buttons();

        void m_OK();

        void m_Cancel();

        void m_Nav_Up();

        void m_Nav_Down();

        static void m_Msg_No(Scene& scene);

        static void m_Msg_Yes(Scene& scene);

        static void m_Msg_OK(Scene& scene);

        #pragma endregion
    };
}

#endif
