#include <nds.h>
#include <string>
#include <vector>

#include "./Path.h"

#ifndef ENGINE_IO_DIRUTIL_H
#define ENGINE_IO_DIRUTIL_H

namespace engine::io
{
    /// @brief Utility for operations related to file directories
    class DirUtil
    {
        #pragma region helper functions

        private:

        static bool m_MakeDir(const std::string& path);
        
        #pragma endregion

        #pragma region functions

        public:

        /// @brief Retrieves the specified items within the directory at the specified path
        /// @param path Full path of directory
        /// @param getFiles Whether or not to retrieve files
        /// @param getDirs Whether or not to retrieve directories
        /// @return List of retrieved items
        /// @note The search is non-recursive
        static std::vector<Path> getPaths(const std::string& path, bool getFiles = true, bool getDirs = true);

        /// @brief Creates a directory (as well as any parent directories) at the specified path. 
        /// If the directory already exists, nothing happens.
        /// @param path Full path of directory
        /// @return Whether or not created successfully (or already exists)
        static bool create(const std::string& path);
        
        #pragma endregion
    };
}

#endif