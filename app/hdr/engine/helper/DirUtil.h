#include <nds.h>
#include <string>

#ifndef ENGINE_HELPER_DIRUTIL_H
#define ENGINE_HELPER_DIRUTIL_H

namespace engine::helper
{
    /// @brief Utility for operations related to file directories
    class DirUtil
    {
        public:

        /// @brief Retrieves the specified items within the directory at the specified path
        /// @param path Path of directory
        /// @param paths Paths of specified items within the directory
        /// @param count Number of specified items within the directory
        /// @param full Whether or not to return full paths
        /// @param getFiles Whether or not to retrieve files
        /// @param getDirs Whether or not to retrieve directories
        /// @note The search is non-recursive
        static void getPaths(const std::string& path, std::string*& paths, u16& count, 
            bool full = true, bool getFiles = true, bool getDirs = true);
    };
}

#endif