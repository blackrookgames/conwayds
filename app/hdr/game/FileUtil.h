#include <nds.h>
#include <vector>

#include "engine/io/Path.h"

#ifndef GAME_FILEUTIL_H
#define GAME_FILEUTIL_H

namespace game
{
    /// @brief Utility for file-related operations
    class FileUtil
    {
        #pragma region const
        
        public:

        /// @brief Maximum capacity
        static constexpr u16 capacity = 0xFFFF;

        /// @brief File extension for patterns
        static const std::string extension;

        /// @brief Display prefix for sample patterns
        static const std::string sample_Prefix;

        /// @brief Directory for sample patterns
        static const std::string sample_Dir;
        
        /// @brief Display prefix for user patterns
        static const std::string user_Prefix;

        /// @brief Directory for user patterns
        static const std::string user_Dir;

        /// @brief Directory of about files
        static const std::string about_Dir;

        /// @brief Path of file containing about info
        static const std::string about_Path;

        #pragma endregion

        #pragma region helper functions

        private:

        static void m_FilterPaths(std::vector<engine::io::Path>& paths);

        #pragma endregion

        #pragma region functions
        
        public:

        /// @brief Retrieves the paths of all pattern files
        /// @param paths Retrieved paths
        /// @param count Number of retrieved paths
        /// @param samples Whether or not to retrieve sample files as well
        static void getPatterns(engine::io::Path*& paths, u16& count, bool sample = true);

        #pragma endregion
    };
}

#endif
