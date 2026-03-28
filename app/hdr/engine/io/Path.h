#include <string>

#ifndef ENGINE_IO_PATH_H
#define ENGINE_IO_PATH_H

namespace engine::io
{
    /// @brief Represents a filepath
    class Path
    {
        #pragma region init

        public:

        /// @brief Empty constructor for Path
        Path();

        /// @brief Constructor for Path
        /// @param fullPath Full path
        /// @param displayName Display name
        /// @param isDir Whether or not the path is a directory
        Path(std::string fullPath, std::string displayName, bool isDir);

        /// @brief Copy constructor for Path
        /// @param src Source
        Path(const Path& src);

        /// @brief Move constructor for Path
        /// @param src Source
        Path(Path&& src);

        /// @brief Destructor for Path
        ~Path();

        #pragma endregion
        
        #pragma region operators

        public:

        /// @brief Copy assignment for Path
        /// @param src Source
        Path& operator=(const Path& src);

        /// @brief Move assignment for Path
        /// @param src Source
        Path& operator=(Path&& src);

        #pragma endregion
        
        #pragma region fields

        private:

        std::string f_FullPath;
        std::string f_DisplayName;
        bool f_IsDir;

        #pragma endregion
        
        #pragma region properties

        public:

        /// @brief Full path
        const std::string& fullPath() const;
        /// @brief Full path
        std::string& fullPath();

        /// @brief Display name
        const std::string& displayName() const;
        /// @brief Display name
        std::string& displayName();

        /// @brief Whether or not the path is a directory
        bool isDir() const;
        /// @brief Whether or not the path is a directory
        void isDir(bool value);

        #pragma endregion
    };
}

#endif