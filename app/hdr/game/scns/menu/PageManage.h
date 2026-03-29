#include "engine/io/Path.h"
#include "./Page.h"

#ifndef GAME_SCNS_MENU_PAGEMANAGE_H
#define GAME_SCNS_MENU_PAGEMANAGE_H

namespace game::scns::menu
{
    /// @brief Represents a page for managing patterns
    class PageManage : public Page
    {
        #pragma region nested

        typedef void (*ButtonAction)(Scene&);

        #pragma endregion

        #pragma region init

        public: 

        /// @brief Constructor for PageManage
        /// @param scene Scene
        /// @param initialIndex Initial index
        PageManage(Scene& scene, u16 initialIndex = 0);

        /// @brief Destructor for PageManage
        virtual ~PageManage() override;

        INIT_NODEFCOPYMOVE(PageManage)

        #pragma endregion

        #pragma region fields

        private:

        u16 f_InitialIndex;

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
        static u16 f_Chosen_Index;

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

        static void m_Msg_Delete(Scene& scene);

        static void m_Msg_Bk2Manage(Scene& scene);

        #pragma endregion
    };
}

#endif
