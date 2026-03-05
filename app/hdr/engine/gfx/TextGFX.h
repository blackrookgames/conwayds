#include <iostream>
#include <nds.h>
#include <string>
#include <streambuf>

#include "engine/helper/_macros.h"

#ifndef ENGINE_GFX_TEXTGFX_H
#define ENGINE_GFX_TEXTGFX_H

namespace engine::gfx
{
    /// @brief Represents text graphics
    class TextGFX : public std::streambuf
    {
        #pragma region init

        public:

        /// @brief Constructor for TextGFX
        /// @param sub Whether or not to utilize the sub-screen instead of the main-screen
        /// @param layer Background hardware layer to initialize and use
        /// @param mapBase 2K offset (within VRAM) for tile map
        /// @param tileBase 16K offset (within VRAM) of tile graphics data
        /// @param priority Priority of background layer
        TextGFX(bool sub, int layer, int mapBase, int tileBase, unsigned int priority);

        /// @brief Destructor for TextGFX
        virtual ~TextGFX() override;

        INIT_NODEFCOPYMOVE(TextGFX)

        #pragma endregion
        
        #pragma region fields

        private:

        bool f_IsDirty;
        
        int f_BG;
        u16* f_BG_GFX;
        u16* f_BG_Map;
        u8* f_BG_Buffer_Beg;
        u8* f_BG_Buffer_End;
        u8* f_BG_Buffer_Ptr;

        char* f_Stream_Base;

        #pragma endregion

        #pragma region properties

        public:
        
        /// @brief Background tile graphics
        const u16* bg_GFX() const;
        /// @brief Background tile graphics
        u16* bg_GFX();

        /// @brief Background tilemap
        const u16* bg_Map() const;
        /// @brief Background tilemap
        u16* bg_Map();

        /// @brief Background buffer
        u8* bg_Buffer() const;
        /// @brief Background buffer
        u8* bg_Buffer();

        #pragma endregion
        
        #pragma region helper functions

        private:

        void m_Write(char c);
        
        void m_Write(char* beg, char* end);

        #pragma endregion

        #pragma region streambuf

        virtual int_type overflow(int_type c) override;

        virtual int sync() override;

        #pragma endregion

        #pragma region functions

        public:

        /// @brief Call this during the vertical blanking
        void vblank();

        /// @brief Marks the visuals as "dirty", forcing an update during the next vertical blanking
        void markDirty();

        /// @brief Clears the screen
        void clear();

        /// @brief Retrieves the position of the cursor
        /// @param x X-coordinate
        /// @param y Y-coordinate
        void getCursor(u8& x, u8& y);

        /// @brief Sets the position of the cursor
        /// @param x X-coordinate
        /// @param y Y-coordinate
        void setCursor(u8 x, u8 y);

        #pragma endregion
    };
}

#endif