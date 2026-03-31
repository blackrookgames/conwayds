#ifndef ENGINE_HELPER__MACROS_H
#define ENGINE_HELPER__MACROS_H

#pragma region data types

#define U8_MIN 0
#define U8_MAX 255
#define I8_MIN (-128)
#define I8_MAX 127
#define U16_MIN 0
#define U16_MAX 65535
#define I16_MIN (-32768)
#define I16_MAX 32767
#define U32_MIN 0
#define U32_MAX 4294967295
#define I32_MIN (-2147483648)
#define I32_MAX 2147483647
#define U64_MIN 0
#define U64_MAX 18446744073709551615
#define I64_MIN (-9223372036854775808)
#define I64_MAX 9223372036854775807

#define SIZE_MIN (U32_MIN)
#define SIZE_MAX (U32_MAX)

#pragma endregion

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

#define DS_SCREEN_COLS (DS_SCREEN_WIDTH / 8)
#define DS_SCREEN_ROWS (DS_SCREEN_HEIGHT / 8)
#define DS_SCREEN_TOTAL (DS_SCREEN_COLS * DS_SCREEN_ROWS)

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

#define MATH_ABS(v) \
    (((v) < 0) ? (-(v)) : (v))

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
