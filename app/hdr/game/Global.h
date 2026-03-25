#include <nds.h>

#include "engine/data/Pattern.h"
#include "engine/helper/RRValue48p16.h"
#include "game/scns/edit/Tool.h"

#ifndef GAME_GLOBAL_H
#define GAME_GLOBAL_H

namespace game
{
    /// @brief Represents information that is globally available
    class Global
    {
        #pragma region fields

        private:

        static engine::data::Pattern f_Pattern;

        static engine::helper::RRValue48p16 f_View_X;
        static engine::helper::RRValue48p16 f_View_Y;
        static engine::helper::RRValue48p16 f_View_Zoom;

        static game::scns::edit::Tool f_Edit_Tool;
        static bool f_Edit_Grid;

        #pragma endregion
        
        #pragma region properties

        public:

        /// @brief Pattern
        static engine::data::Pattern* pattern();

        /// @brief X-coordinate of view
        static engine::helper::RRValue48p16 view_X();
        /// @brief X-coordinate of view
        static void view_X(engine::helper::RRValue48p16 value);

        /// @brief Y-coordinate of view
        static engine::helper::RRValue48p16 view_Y();
        /// @brief Y-coordinate of view
        static void view_Y(engine::helper::RRValue48p16 value);

        /// @brief Zoom percentage of view
        static engine::helper::RRValue48p16 view_Zoom();
        /// @brief Zoom percentage of view
        static void view_Zoom(engine::helper::RRValue48p16 value);
        
        /// @brief Tool being used in editor
        static game::scns::edit::Tool edit_Tool();
        /// @brief Tool being used in editor
        static void edit_Tool(game::scns::edit::Tool value);

        /// @brief Whether or not grid is toggled in editor
        static bool edit_Grid();
        /// @brief Whether or not grid is toggled in editor
        static void edit_Grid(bool value);

        #pragma endregion
        
        #pragma region functions

        public:

        /// @brief Inputs from another pattern
        /// @param input Input pattern
        static void pattern_From(const engine::data::Pattern& input);

        /// @brief Outputs to another pattern
        /// @param output Output pattern
        static void pattern_To(engine::data::Pattern& output);

        #pragma endregion
    };
}

#endif
