#ifndef ENGINE_HELPER__MACROS_H
#define ENGINE_HELPER__MACROS_H

#pragma region INIT

#define INIT_NODEF(class) \
    class() = delete;

#define INIT_NOCOPY(class) \
    class(const class &src) = delete; \
    class& operator=(const class &src) = delete;
    
#define INIT_NOMOVE(class) \
    class(class &&src) = delete; \
    class& operator=(class &&src) = delete;

#define INIT_NOCOPYMOVE(class) \
    INIT_NOCOPY(class) \
    INIT_NOMOVE(class) \

#define INIT_NODEFCOPYMOVE(class) \
    INIT_NODEF(class) \
    INIT_NOCOPYMOVE(class)

#pragma endregion

#pragma region PATTERN

#define PATTERN_WIDTH 256
#define PATTERN_HEIGHT 256
#define PATTERN_AREA (PATTERN_WIDTH * PATTERN_HEIGHT)

#pragma endregion

#endif
