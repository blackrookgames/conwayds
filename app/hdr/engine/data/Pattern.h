#include "engine/helper/_macros.h"
#include "./Serial.h"

#ifndef ENGINE_DATA_PATTERN_H
#define ENGINE_DATA_PATTERN_H

namespace engine::data
{
    /// @brief Represents a life pattern
    class Pattern : public Serial
    {
        #pragma region init

        public:
        
        /// @brief Constructor for Pattern
        Pattern();

        /// @brief Destructor for Pattern
        virtual ~Pattern();

        INIT_NOCOPYMOVE(Pattern)

        #pragma endregion

        #pragma region load/save
        
        public:

        /// @brief See Serial::load(const char*, size_t)
        virtual bool load(const char* data, size_t size) override;

        /// @brief See Serial::save(char*&, size_t&)
        virtual bool save(char*& data, size_t& size) const override;

        #pragma endregion

        #pragma region fields

        private:

        bool* f_cells;

        #pragma endregion

        #pragma region properties
        
        public:

        /// @brief Pattern cells
        /// @note It is recommended to use getcell(u16,u16) for most operations
        const bool* cells() const;

        /// @brief Pattern cells
        /// @note It is recommended to use getcell(u16,u16) and setcell(u16,u16,bool) for most operations
        bool* cells();

        #pragma endregion

        #pragma region functions
        
        public:

        /// @brief Gets the cell at the specified coordinates
        /// @param x X-coordinate
        /// @param y Y-coordinate
        /// @return Cell at the specified coordinates
        bool getcell(u16 x, u16 y) const;

        /// @brief Sets the cell at the specified coordinates
        /// @param x X-coordinate
        /// @param y Y-coordinate
        /// @param live Whether or not the cell is alive
        void setcell(u16 x, u16 y, bool live);

        #pragma endregion
    };
}

#endif