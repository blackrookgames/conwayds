#ifndef STARTPATTERN_H
#define STARTPATTERN_H

#include "_macros.h"

#include <nds.h>

/// @brief
/// Represents a starting pattern for a life simulation
class StartPattern
{
    #pragma region init

    public:

    /// @brief 
    /// Constructor for StartPattern
    /// @param fgColor 
    /// Foreground color
    /// @param bgColor 
    /// Background color (must be different from foreground color)
    StartPattern(u8 fgColor, u8 bgColor);

    /// @brief 
    /// Destructor for StartPattern
    virtual ~StartPattern();

    INIT_NODEFCOPYMOVE(StartPattern)

    #pragma endregion

    #pragma region fields

    private:
    
    u8 f_fgColor;
    u8 f_bgColor;
    u8* f_cells;

    #pragma endregion

    #pragma region functions

    public:

    /// @brief Gets the state of the cell at the specified coordinates
    /// @param x X-coordinate
    /// @param y Y-coordinate
    /// @return Whether or not the cell is alive
    bool cell(u16 x, u16 y) const;

    /// @brief Sets the state of the cell at the specified coordinates
    /// @param x X-coordinate
    /// @param y Y-coordinate
    /// @param alive Whether or not the cell is alive
    void cell(u16 x, u16 y, bool alive);

    /// @brief
    /// Draws the pattern onto the DS screen
    /// @param gfxptr 
    /// Pointer to bitmap layer; assuming the layer is an 8-bit 256x256 bitmap
    void draw(void* gfxptr) const;

    #pragma endregion
};

#endif
