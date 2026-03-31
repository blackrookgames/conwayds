#include <nds.h>
#include <string>
#include <vector>

#include "./Path.h"

#ifndef ENGINE_IO_IOUTIL_H
#define ENGINE_IO_IOUTIL_H

namespace engine::io
{
    /// @brief Utility for IO-related operations
    class IOUtil
    {
        #pragma region functions

        public:

        /// @brief Attempts to load binary data from a file
        /// @param path Path of input file
        /// @param data Loaded data (or nullptr if load fails); safe to delete with delete[]
        /// @param size Size of loaded data
        /// @return Whether or not successful
        static bool load(const char* path, char*& data, size_t& size);

        /// @brief Attempts to load binary data from a file
        /// @param path Path of input file
        /// @param data Loaded data (or nullptr if load fails); safe to delete with delete[]
        /// @param size Size of loaded data
        /// @return Whether or not successful
        static bool load(const std::string& path, char*& data, size_t& size);

        /// @brief Attempts to save binary data to a file
        /// @param path Path of output file
        /// @param data Data to save
        /// @param size Size of save data
        /// @return Whether or not successful
        static bool save(const char* path, const char* data, size_t size);

        /// @brief Attempts to save binary data to a file
        /// @param path Path of output file
        /// @param data Data to save
        /// @param size Size of save data
        /// @return Whether or not successful
        static bool save(const std::string& path, const char* data, size_t size);
        
        #pragma endregion
    };
}

#endif