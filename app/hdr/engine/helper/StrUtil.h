#include <nds.h>
#include <string>

#include "./_macros.h"

#ifndef ENGINE_HELPER_STRUTIL_H
#define ENGINE_HELPER_STRUTIL_H

namespace engine::helper
{
    /// @brief Utility for string-related operations
    class StrUtil
    {
        public:

        /// @brief Searches the string for the specified character
        /// @param str String
        /// @param c Character to search for
        /// @param beg Index of the first character to search
        /// @param len Number of characters to search
        /// @param returnLast Whether or not to return the last occurance of the character instead of the first occurance
        /// @return First or last (see returnLast) occurance of the specified character (or SIZE_MAX if character could not be found)
        static size_t findChar(const std::string& str, char c, size_t beg = 0, size_t len = SIZE_MAX, bool returnLast = false);

        /// @brief Checks whether or not the string starts with the specified substring
        /// @param str String
        /// @param substr Substring
        /// @return Whether or not the string starts with the specified substring
        static bool startsWith(const std::string& str, const std::string& substr);

        /// @brief Checks whether or not the string ends with the specified substring
        /// @param str String
        /// @param substr Substring
        /// @return Whether or not the string ends with the specified substring
        static bool endsWith(const std::string& str, const std::string& substr);
    };
}

#endif