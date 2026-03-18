#include <nds.h>

#include "engine/data/Pattern.h"

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

        #pragma endregion
        
        #pragma region properties

        public:

        /// @brief Pattern
        static engine::data::Pattern* pattern();

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
