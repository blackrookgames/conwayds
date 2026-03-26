#ifndef GAME_SCNS_MENU_PAGESTATUS_H
#define GAME_SCNS_MENU_PAGESTATUS_H

namespace game::scns::menu
{
    /// @brief Represents the status of a page
    enum struct PageStatus
    {
        /// @brief Page has been initialized
        INIT,
        /// @brief Page is being entered
        ENTERING,
        /// @brief Page is the active scene
        ACTIVE,
        /// @brief Page is being exited
        EXITING,
        /// @brief Page has been exited
        EXITED,
    };
}

#endif
