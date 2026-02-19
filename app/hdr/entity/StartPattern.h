#include "engine/helper/_macros.h"

#include <nds.h>

#ifndef ENTITY_STARTPATTERN_H
#define ENTITY_STARTPATTERN_H

namespace entity
{
    /// @brief
    /// Represents a starting pattern for a life simulation
    class StartPattern
    {
        #pragma region init

        public:

        /// @brief 
        /// Constructor for StartPattern
        StartPattern();

        /// @brief 
        /// Destructor for StartPattern
        virtual ~StartPattern();

        INIT_NOCOPYMOVE(StartPattern)

        #pragma endregion

        #pragma region fields

        private:
        
        bool* f_cells;

        #pragma endregion

        #pragma region properties

        public:

        /// @brief
        /// Cell data
        /// @note
        /// It is recommended to use cell(u16, u16) and cell(u16, u16, bool) for most operations
        const bool* cells() const;

        /// @brief
        /// Cell data
        /// @note
        /// It is recommended to use cell(u16, u16) and cell(u16, u16, bool) for most operations
        bool* cells();

        #pragma endregion

        #pragma region functions

        public:

        /// @brief
        /// Gets the state of the cell at the specified coordinates
        /// @param x
        /// X-coordinate
        /// @param y
        /// Y-coordinate
        /// @return
        /// Whether or not the cell is alive
        bool cell(u16 x, u16 y) const;

        /// @brief
        /// Sets the state of the cell at the specified coordinates
        /// @param x
        /// X-coordinate
        /// @param y
        /// Y-coordinate
        /// @param alive
        /// Whether or not the cell is alive
        void cell(u16 x, u16 y, bool alive);

        #pragma endregion
    };
}

#endif
