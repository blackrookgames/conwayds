#include "engine/gfx/TextGFX.h"

#include "__.h"

using namespace engine::gfx;

#pragma region macros

#define BG_WIDTH 256
#define BG_HEIGHT 256
#define BG_TILEW (BG_WIDTH / 8)
#define BG_TILEH (BG_HEIGHT / 8)
#define BG_TILEAREA (BG_TILEW * BG_TILEH)
#define BG_BYTESPT 2                        // Bytes per tile
#define BG_BYTESPR (BG_TILEW * 2)           // Bytes per row
#define BG_SIZE (BG_BYTESPR * BG_TILEH)     // Size (in bytes)

#define STREAM_SIZE 256

#pragma endregion

#pragma region init

TextGFX::TextGFX(bool sub, int layer, int mapBase, int tileBase, unsigned int priority)
{
    // Mark as dirty
    f_IsDirty = true;
    // Initialize background
    if (sub) f_BG = bgInitSub(layer, BgType_Text4bpp, BgSize_T_256x256, mapBase, tileBase);
    else f_BG = bgInit(layer, BgType_Text4bpp, BgSize_T_256x256, mapBase, tileBase);
    f_BG_GFX = bgGetGfxPtr(f_BG);
    f_BG_Map = bgGetMapPtr(f_BG);
    f_BG_Buffer_Beg = new u8[BG_SIZE];
    f_BG_Buffer_End = f_BG_Buffer_Beg + BG_SIZE;
    f_BG_Buffer_Ptr = f_BG_Buffer_Beg;
    bgSetPriority(f_BG, priority);
    // Initialize buffer
    f_Stream_Base = new char[STREAM_SIZE];
    setp(f_Stream_Base, f_Stream_Base + STREAM_SIZE);
}

TextGFX::~TextGFX()
{
    // Finalize buffer
    delete[] f_Stream_Base;
    // Finalize background
    delete[] f_BG_Buffer_Beg;
}

#pragma endregion

#pragma region properties


const u16* TextGFX::bg_GFX() const { return f_BG_GFX; }
u16* TextGFX::bg_GFX() { return f_BG_GFX; }

const u16* TextGFX::bg_Map() const { return f_BG_Map; }
u16* TextGFX::bg_Map() { return f_BG_Map; }

u8* TextGFX::bg_Buffer() const { return f_BG_Buffer_Beg; }
u8* TextGFX::bg_Buffer() { return f_BG_Buffer_Beg; }

#pragma endregion

#pragma region helper functions

void TextGFX::m_Write(char c)
{
    *(f_BG_Buffer_Ptr++) = (u8)c;
    *(f_BG_Buffer_Ptr++) = 0x00;
    // Fix cursor
    if (f_BG_Buffer_Ptr >= f_BG_Buffer_End)
        f_BG_Buffer_Ptr = f_BG_Buffer_Beg;
}
        
void TextGFX::m_Write(char* beg, char* end)
{
    for (const char* ptr = beg; ptr < end; ++ptr)
        m_Write(*ptr);
}

#pragma endregion

#pragma region streambuf

std::streambuf::int_type TextGFX::overflow(int_type c)
{
    f_IsDirty = true;
    if (c != traits_type::eof())
    {
        // Write the current buffer content to the string
        m_Write(pbase(), pptr());
        // Reset the buffer put pointer to the beginning
        pbump(static_cast<int>(pbase() - pptr()));
        // Add the new character
        m_Write(static_cast<char>(c));
        // Return
        return traits_type::not_eof(c);
    }
    return traits_type::eof();
}

int TextGFX::sync()
{
    f_IsDirty = true;
    // Write the remaining buffer content
    m_Write(pbase(), pptr());
    // Reset the put pointer
    pbump(static_cast<int>(pbase() - pptr()));
    // Success!!!
    return 0;
}

#pragma endregion

#pragma region functions

void TextGFX::vblank()
{
    // Update dirty
    if (!f_IsDirty) return;
    f_IsDirty = false;
    // Update background
    DC_FlushRange(f_BG_Buffer_Beg, BG_SIZE);
    dmaCopy(f_BG_Buffer_Beg, f_BG_Map, BG_SIZE);
}

void TextGFX::markDirty()
{
    f_IsDirty = true;
}

void TextGFX::clear()
{
    // Clear contents
    std::fill(f_BG_Buffer_Beg, f_BG_Buffer_End, 0x20);
    // Reset cursor
    f_BG_Buffer_Ptr = f_BG_Buffer_Beg;
    // Mark as dirty
    f_IsDirty = true;
}

void TextGFX::getCursor(u8& x, u8& y)
{
    u32 index = (f_BG_Buffer_Ptr - f_BG_Buffer_Beg) / BG_BYTESPT;
    x = (u8)(index % BG_BYTESPR);
    y = (u8)(index / BG_BYTESPR);
}

void TextGFX::setCursor(u8 x, u8 y)
{
    if (x < 0 || x >= BG_TILEW) return;
    if (y < 0 || y >= BG_TILEH) return;
    f_BG_Buffer_Ptr = f_BG_Buffer_Beg + ((u32)x * BG_BYTESPT + (u32)y * BG_BYTESPR);
}

#pragma endregion