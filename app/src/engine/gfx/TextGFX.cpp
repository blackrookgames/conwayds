#include "engine/gfx/TextGFX.h"

#include "__.h"

using namespace engine::gfx;

#pragma region macros

#define BG_WIDTH 256
#define BG_HEIGHT 256
#define BG_TILE_COLS (BG_WIDTH / 8)
#define BG_TILE_ROWS (BG_HEIGHT / 8)
#define BG_TILE_COUNT (BG_TILE_COLS * BG_TILE_ROWS)
#define BG_SIZE (BG_TILE_COUNT * 2) // Size (in bytes)

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
    f_BG_Buffer_Beg = new u16[BG_TILE_COUNT];
    f_BG_Buffer_End = f_BG_Buffer_Beg + BG_TILE_COUNT;
    f_BG_Buffer_Ptr = f_BG_Buffer_Beg;
    bgSetPriority(f_BG, priority);
    // Initialize buffer
    f_Stream_Base = new char[STREAM_SIZE];
    setp(f_Stream_Base, f_Stream_Base + STREAM_SIZE);
    // Initialize flags
    f_Flags = TextFlags::Default;
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

u16* TextGFX::bg_Buffer() const { return f_BG_Buffer_Beg; }
u16* TextGFX::bg_Buffer() { return f_BG_Buffer_Beg; }

TextFlags TextGFX::flags() const { return f_Flags; }
void TextGFX::flags(TextFlags value) { f_Flags = value; }

#pragma endregion

#pragma region helper functions

void TextGFX::m_Write(char c)
{
    *(f_BG_Buffer_Ptr++) = static_cast<u16>(f_Flags) | (u16)c;
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
    u32 index = f_BG_Buffer_Ptr - f_BG_Buffer_Beg;
    x = (u8)(index % BG_TILE_COLS);
    y = (u8)(index / BG_TILE_COLS);
}

void TextGFX::setCursor(u8 x, u8 y)
{
    if (x < 0 || x >= BG_TILE_COLS) return;
    if (y < 0 || y >= BG_TILE_ROWS) return;
    f_BG_Buffer_Ptr = f_BG_Buffer_Beg + ((u32)x + (u32)y * BG_TILE_COLS);
}

#pragma endregion