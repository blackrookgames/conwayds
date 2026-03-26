#include <nds.h>

#include "./__.h"

#include "engine/helper/_macros.h"
#include "./PageStatus.h"

#ifndef GAME_SCNS_MENU_PAGE_H
#define GAME_SCNS_MENU_PAGE_H

namespace game::scns::menu
{
#ifndef GAME_SCNS_MENU_SCENE_H
    class Scene;
#endif

    /// @brief Represents a menu page
    class Page
    {
        #pragma region init

        public: 

        /// @brief Constructor for Page
        /// @param scene Scene
        Page(Scene& scene);

        /// @brief Destructor for Page
        virtual ~Page();

        INIT_NODEFCOPYMOVE(Page)

        #pragma endregion

        #pragma region friends

        friend Scene;

        #pragma endregion

        #pragma region fields

        private:

        PageStatus f_status;
        bool f_deleteOnExit;

        Scene& f_Scene;
        
        #pragma endregion

        #pragma region properties

        public:

        /// @brief Status of the page
        PageStatus status() const;

        /// @brief Whether or not to delete the page when exited 
        bool deleteOnExit() const;
        
        /// @brief Whether or not to delete the page when exited 
        void deleteOnExit(bool value);

        /// @brief Scene
        const Scene& scene() const;
        /// @brief Scene
        Scene& scene();
        
        #pragma endregion

        #pragma region helper functions

        protected:

        /// @brief Called when entering the page
        virtual void m_enter();

        /// @brief Called when exiting the page
        virtual void m_exit();

        /// @brief Called when updating the page
        virtual void m_update();

        /// @brief Called during vblank
        virtual void m_vblank();

        private:

        /// @brief Also accessed by Scene
        void m__enter();

        /// @brief Also accessed by Scene
        void m__exit();

        /// @brief Also accessed by Scene
        void m__update();

        /// @brief Also accessed by Scene
        void m__vblank();

        #pragma endregion
    };
}

#endif
