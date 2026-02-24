#include <nds.h>

#ifndef ENGINE_DATA_SERIAL_H
#define ENGINE_DATA_SERIAL_H

namespace engine::data
{
    /// @brief Represents serializable data
    class Serial
    {
        public:

        /// @brief Attempts to load from serialized data
        /// @param data Serialized data
        /// @param size Size of serialized data
        /// @return Whether or not successful
        virtual bool load(const char* data, size_t size) = 0;

        /// @brief Attempts to save to serialized data
        /// @param data Created serialized data (or nullptr if serialization fails); 
        /// safe to delete with delete[]
        /// @param size Size of serialized data
        /// @return Whether or not successful
        virtual bool save(char*& data, size_t& size) const = 0;

        /// @brief Attempts to load from a file
        /// @param path Path of file to load from
        /// @return Whether or not successful
        bool load_file(const char* path);
    };
}

#endif