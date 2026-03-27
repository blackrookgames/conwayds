#include <string>

#include "./Page.h"

#ifndef GAME_SCNS_MENU_PAGERANDOM_H
#define GAME_SCNS_MENU_PAGERANDOM_H

namespace game::scns::menu
{
    /// @brief Represents a message that prompts the user to press Yes or No
    class PageRandom : public Page
    {
        #pragma region nested

        typedef void (*ButtonAction)(PageRandom&);

        #pragma endregion

        #pragma region init

        public: 

        /// @brief Constructor for PageRandom
        /// @param scene Scene
        /// @param seed Seed
        PageRandom(Scene& scene, u32 seed);

        /// @brief Destructor for PageRandom
        virtual ~PageRandom() override;

        INIT_NODEFCOPYMOVE(PageRandom)

        #pragma endregion

        #pragma region fields

        private:

        u32 f_Seed;
        u16 f_Digits;

        u16* f_Screen;
        size_t f_Screen_Len;

        u16 f_Sel_Index;
        u16 f_Sel_Touch;
        bool f_Sel_Touching;

        static ButtonAction f_ButtonActions[];

        static u32 f_RandSeed;

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

        void m_Button_Action();

        void m_Refresh();

        void m_InputDigit(u32 digit);

        static u16 m_Digits(u32 value);

        static void m_Msg_No(Scene& scene);

        static void m_Msg_Yes(Scene& scene);

        static void m_Action_0(PageRandom& page);

        static void m_Action_1(PageRandom& page);

        static void m_Action_2(PageRandom& page);

        static void m_Action_3(PageRandom& page);

        static void m_Action_4(PageRandom& page);

        static void m_Action_5(PageRandom& page);

        static void m_Action_6(PageRandom& page);

        static void m_Action_7(PageRandom& page);

        static void m_Action_8(PageRandom& page);

        static void m_Action_9(PageRandom& page);

        static void m_Action_A(PageRandom& page);

        static void m_Action_B(PageRandom& page);

        static void m_Action_C(PageRandom& page);

        static void m_Action_D(PageRandom& page);

        static void m_Action_E(PageRandom& page);

        static void m_Action_F(PageRandom& page);

        static void m_Action_Backspace(PageRandom& page);

        static void m_Action_OK(PageRandom& page);

        static void m_Action_Cancel(PageRandom& page);

        #pragma endregion
    };
}

#endif
