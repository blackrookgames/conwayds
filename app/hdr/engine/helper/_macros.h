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

#pragma region DS

#define DS_SCREEN_WIDTH 256
#define DS_SCREEN_HEIGHT 192

#define DS_SCREEN_OFF setBrightness(3, -16);
#define DS_SCREEN_ON setBrightness(3, 0);

#pragma endregion

#pragma region PATTERN

#define PATTERN_WIDTH 254
#define PATTERN_HEIGHT 254
#define PATTERN_AREA (PATTERN_WIDTH * PATTERN_HEIGHT)

#pragma endregion

#pragma region ENUMFLAGS

#define ENUMFLAGS_OP1(type, under, op) \
    inline type operator op(type v) \
    { return static_cast<type>(op static_cast<under>(v)); }

#define ENUMFLAGS_OP2(type, under, op) \
    inline type operator op(type v0, type v1) \
    { return static_cast<type>(static_cast<under>(v0) op static_cast<under>(v1)); }

#define ENUMFLAGS_OPS(type, under) \
    ENUMFLAGS_OP2(type, under, |) \
    ENUMFLAGS_OP2(type, under, &) \
    ENUMFLAGS_OP2(type, under, ^) \
    ENUMFLAGS_OP1(type, under, ~)

#pragma endregion

#endif
