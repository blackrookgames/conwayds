#include "engine/data/Pattern.h"

#include <cstring>
#include <sstream>

#include "__.h"

using namespace engine::data;

#pragma region macros

#define INDEX(x, y) (x + y * PATTERN_WIDTH)
#define OUTOFRANGE(x, y) ((x >= PATTERN_WIDTH) || (y >= PATTERN_HEIGHT))

#pragma endregion

#pragma region init

Pattern::Pattern()
{
    f_cells = new bool[PATTERN_AREA];
}

Pattern::~Pattern()
{
    delete[] f_cells;
}

#pragma endregion

#pragma region load/save

bool Pattern::load(const char* data, size_t size)
{
    // Clear cells
    memset(f_cells, false, PATTERN_AREA); 
    // Get width and height
    if (size < 8) return false;
    u32 in_w = data[3];
    in_w <<= 8;
    in_w |= data[2];
    in_w <<= 8;
    in_w |= data[1];
    in_w <<= 8;
    in_w |= data[0];
    u32 in_h = data[7];
    in_h <<= 8;
    in_h |= data[6];
    in_h <<= 8;
    in_h |= data[5];
    in_h <<= 8;
    in_h |= data[4];
    u32 in_a = in_w * in_h;
    // Determine dimensions
    u32 in_x1, in_x2, out_x;
    if (in_w > PATTERN_WIDTH)
    {
        in_x1 = (in_w - PATTERN_WIDTH) / 2;
        in_x2 = in_x1 + PATTERN_WIDTH;
        out_x = 0;
    }
    else
    {
        in_x1 = 0;
        in_x2 = in_w;
        out_x = (PATTERN_WIDTH - in_w) / 2;
    }
    u32 in_y1, in_y2, out_y;
    if (in_h > PATTERN_HEIGHT)
    {
        in_y1 = (in_h - PATTERN_HEIGHT) / 2;
        in_y2 = in_y1 + PATTERN_HEIGHT;
        out_y = 0;
    }
    else
    {
        in_y1 = 0;
        in_y2 = in_h;
        out_y = (PATTERN_HEIGHT - in_h) / 2;
    }
    // Get cell data
    const char* iptr = data + 8;
    u32 ipos = 0;
    while (ipos < in_a)
    {
        // Compressed?
        if ((*iptr & 0b00000001) != 0)
        {
            bool live = (*iptr & 0b00000010) != 0;
            u8 count = *iptr >> 2;
            while (ipos < in_a && count > 0)
            {
                // Set cell
                u32 ix = ipos % in_w;
                u32 iy = ipos / in_w;
                if (ix >= in_x1 && ix < in_x2 && iy >= in_y1 && iy < in_y2)
                    f_cells[(out_x + ix - in_x1) + (out_y + iy - in_y1) * PATTERN_WIDTH] = live;
                // Next
                ++ipos;
                --count;
            }
        }
        // Uncompressed?
        else
        {
            u16 mask = 0b00000010;
            while (ipos < in_a && mask <= 0b10000000)
            {
                // Set cell
                u32 ix = ipos % in_w;
                u32 iy = ipos / in_w;
                if (ix >= in_x1 && ix < in_x2 && iy >= in_y1 && iy < in_y2)
                    f_cells[(out_x + ix - in_x1) + (out_y + iy - in_y1) * PATTERN_WIDTH] = (*iptr & mask) != 0;
                // Next
                ++ipos;
                mask <<= 1;
            }
        }
        // Next
        ++iptr;
    }
    // Success!!!
    return true;
}

bool Pattern::save(char*& data, size_t& size) const
{
    data = nullptr;
    size = 0;
    // Gather cell data
    u8 celldata[(PATTERN_AREA + 6) / 7];
    size_t cellsize;
    {
        bool* iptr = f_cells;
        u8* optr = celldata;
        bool* iend = iptr + PATTERN_AREA;
        while (iptr < iend)
        {
            // Get first cell in byte
            bool first = *(iptr++);
            // Get next 6 cells
            u8 byte = first ? 0b00000010 : 0b00000000;
            u16 mask = 0b00000100;
            bool compressable = true;
            while (iptr < iend && mask <= 0b10000000)
            {
                // Get cell
                bool cell = *(iptr++);
                // Compare with first
                if (cell != first) compressable = false;
                // Add to byte
                if (cell) byte |= mask;
                // Next
                mask <<= 1;
            }
            if (mask <= 0b10000000)
                compressable = false;
            // Compressable?
            if (compressable)
            {
                u8 count = 7;
                while (count < 63 && iptr < iend && *iptr == first)
                {
                    ++iptr;
                    ++count;
                }
                byte = ((byte & 0b00000010) | 0b00000001) | (count << 2);
            }
            // Add byte
            *(optr++) = byte;
        }
        cellsize = iptr - f_cells;
    }
    // Create data
    size = 8 + cellsize;
    data = new char[size];
    {
        char* optr = data;
        // Write width and height
        {
            u32 value = PATTERN_WIDTH;
            optr[0] = (u8)(value & 0xFF); value >>= 8;
            optr[1] = (u8)(value & 0xFF); value >>= 8;
            optr[2] = (u8)(value & 0xFF); value >>= 8;
            optr[3] = (u8)value;
            optr += 4;
            value = PATTERN_HEIGHT;
            optr[0] = (u8)(value & 0xFF); value >>= 8;
            optr[1] = (u8)(value & 0xFF); value >>= 8;
            optr[2] = (u8)(value & 0xFF); value >>= 8;
            optr[3] = (u8)value;
            optr += 4;
        }
        // Write cell data
        {
            u8* iptr = celldata;
            u8* iend = celldata + cellsize;
            while (iptr < iend) *(optr++) = *(iptr++);
        }
    }
    // Success!!!
    return true;
}

#pragma endregion

#pragma region properties

const bool* Pattern::cells() const { return f_cells; }

bool* Pattern::cells() { return f_cells; }

#pragma endregion

#pragma region functions

bool Pattern::getcell(u16 x, u16 y) const
{
    if OUTOFRANGE(x, y) return false;
    return f_cells[INDEX(x, y)];
}

void Pattern::setcell(u16 x, u16 y, bool live)
{
    if OUTOFRANGE(x, y) return;
    f_cells[INDEX(x, y)] = live;
}

#pragma endregion