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

#pragma region MATH

#define MATH_MIN(v0, v1) \
    ((v0 < v1) ? (v0) : (v1))
#define MATH_MAX(v0, v1) \
    ((v0 > v1) ? (v0) : (v1))
#define MATH_CLAMP(min, max, value) \
    (MATH_MAX(min, MATH_MIN(max, value)))
#define MATH_SCALE(in_scale, out_scale, value) \
    (((value) * (out_scale)) / (in_scale))
#define MATH_SCALE2(in_min, in_max, out_min, out_max, value) \
    ((out_min) + MATH_SCALE((in_max) - (in_min), (out_max) - (out_min), (value) - (in_min)))

#pragma endregion

#pragma region STREAM

#define STREAM_STRING(variable, content) \
    std::ostringstream variable; variable << content;

#define STREAM_ALIGN_L(width) \
    std::left << std::setw(width)

#pragma endregion

#pragma region DELETE

#define DELETE_OBJECT(obj) \
    if (obj) delete obj; obj = nullptr;
    
#define DELETE_ARRAY(array) \
    if (array) delete[] array; array = nullptr;

#pragma endregion

#endif
