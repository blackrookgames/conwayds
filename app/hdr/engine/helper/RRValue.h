#include <nds.h>
#include <string.h>

#include <__.h>

#ifndef ENGINE_HELPER_RRVALUE_H
#define ENGINE_HELPER_RRVALUE_H

namespace engine::helper
{
    /// @brief Represents a fixed-point value with crude operators
    /// @tparam TRaw Raw data type
    /// @tparam TFrac Number of bits to represent the fraction
    template<typename TRaw, int TFrac>
    class RRValue
    {
        #pragma region const

        private:

        static constexpr u8 f_TotalSize = sizeof(TRaw) * 8;
        static constexpr u8 f_WholeSize = f_TotalSize - TFrac;
        static constexpr TRaw f_FractVals = (TRaw)1 << TFrac;
        static constexpr TRaw f_FractMask = f_FractVals - 1;
        static constexpr TRaw f_FractMask_Inv = ~f_FractMask;
        static constexpr size_t f_WholeBufLen = (f_WholeSize < 1) ? 1 : f_WholeSize;
        static constexpr size_t f_FractBufLen = (TFrac < 1) ? 1 : TFrac;
        static constexpr TRaw f_FractHalf = f_FractVals / 2;

        #pragma endregion

        #pragma region init

        public:

        /// @brief Empty constructor for RRValue
        RRValue() : RRValue(0) { }

        /// @brief Constructor for RRValue
        /// @param raw Raw value
        RRValue(TRaw raw) { f_Raw = raw; }

        /// @brief Constructor for RRValue
        /// @param whole Whole part
        /// @param fract Fractional part
        RRValue(TRaw whole, TRaw fract) { f_Raw = (whole << TFrac) | fract; }

        /// @brief Copy constructor for RRValue
        /// @param src Source
        RRValue(const RRValue& src) { f_Raw = src.f_Raw; }

        /// @brief Move constructor for RRValue
        /// @param src Source
        RRValue(RRValue&& src) { f_Raw = src.f_Raw; }

        virtual ~RRValue() { }

        #pragma endregion

        #pragma region fields

        private:

        TRaw f_Raw;

        #pragma endregion

        #pragma region properties

        public:

        /// @brief Raw value
        TRaw raw() const { return f_Raw; }

        #pragma endregion

        #pragma region functions

        public:

        /// @brief Creates a string representation of the value
        /// @param ndecs Number of decimals places
        /// @return Created string
        std::string toStr(s8 ndecs = -1) const
        {
            char* iptr;
            char* optr;
            // Get absolute value
            bool isneg = f_Raw < 0;
            TRaw abs = isneg ? (-f_Raw) : f_Raw;
            // Whole number
            TRaw whole = abs >> TFrac;
            u8 whole_Len = 0;
            char whole_Chars[f_WholeBufLen];
            optr = whole_Chars + f_WholeBufLen;
            while (true)
            {
                *(--optr) = 0x30 + (char)(whole % 10);
                ++whole_Len;
                whole /= 10;
                if (whole == 0) break;
            }
            // Fractional number
            TRaw fract = abs & f_FractMask;
            u8 fract_Len = 0;
            size_t fractBufLen = (ndecs < 0) ? f_FractBufLen : ndecs;
            char fract_Chars[fractBufLen];
            optr = fract_Chars;
            while (fract_Len < fractBufLen)
            {
                fract *= 10;
                *(optr++) = 0x30 + (char)(fract >> TFrac);
                ++fract_Len;
                fract &= f_FractMask;
                if (ndecs < 0 && fract == 0) break;
            }
            // Create final string
            char cstr[(isneg ? 1 : 0) + whole_Len + 1 + fract_Len + 1];
            {
                optr = cstr;
                // Negative
                if (isneg) *(optr++) = '-';
                // Whole
                iptr = whole_Chars + f_WholeBufLen - whole_Len;
                for (u8 i = 0; i < whole_Len; ++i) *(optr++) = *(iptr++);
                // Period
                *(optr++) = '.';
                // Fraction
                iptr = fract_Chars;
                for (u8 i = 0; i < fract_Len; ++i) *(optr++) = *(iptr++);
                // Null
                *optr = 0;
            }
            // Success!!!
            return std::string(cstr);
        }

        /// @brief Addition
        /// @param other Value to add
        /// @return this + other
        RRValue add(const RRValue& other) const
        {
            return RRValue(f_Raw + other.f_Raw);
        }

        /// @brief Subtraction
        /// @param other Value to subtract
        /// @return this - other
        RRValue sub(const RRValue& other) const
        {
            return RRValue(f_Raw - other.f_Raw);
        }

        /// @brief Multiplication
        /// @param other Value to multiply by
        /// @return this * other
        RRValue mul(const RRValue& other) const
        {
            if (f_Raw == 0 || other.f_Raw == 0) return RRValue(0);
            TRaw v0 = MATH_ABS(f_Raw);
            TRaw v1 = MATH_ABS(other.f_Raw);
            TRaw sign = (f_Raw / v0) * (other.f_Raw / v1);
            // Calculate whole
            TRaw w = v0 * (v1 >> TFrac);
            // Calculate fraction
            TRaw f = (v0 * (v1 & f_FractMask)) >> TFrac;
            // Calculate final
            return RRValue(sign * (w + f));
        }

        /// @brief Division
        /// @param other Value to divide by
        /// @return this / other
        RRValue div(const RRValue& other) const
        {
            if (f_Raw == 0 || other.f_Raw == 0) return RRValue(0);
            TRaw v0 = MATH_ABS(f_Raw);
            TRaw v1 = MATH_ABS(other.f_Raw);
            TRaw sign = (f_Raw / v0) * (other.f_Raw / v1);
            // Calculate whole
            TRaw w = v0 / v1;
            v0 -= w * v1;
            // Calculate fraction
            TRaw f = (v0 << TFrac) / v1;
            // Calculate final
            return RRValue(sign * ((w << TFrac) + f));
        }

        /// @brief Negation
        /// @return -this
        RRValue neg() const
        {
            return RRValue(-f_Raw);
        }

        /// @brief Equality
        /// @param other Other value
        /// @return this == other
        bool equ(const RRValue& other) const
        {
            return f_Raw == other.f_Raw;
        }

        /// @brief Inequality
        /// @param other Other value
        /// @return this != other
        bool neq(const RRValue& other) const
        {
            return f_Raw != other.f_Raw;
        }

        /// @brief Greater than
        /// @param other Other value
        /// @return this > other
        bool gt(const RRValue& other) const
        {
            return f_Raw > other.f_Raw;
        }

        /// @brief Greater than or equal to
        /// @param other Other value
        /// @return this >= other
        bool ge(const RRValue& other) const
        {
            return f_Raw >= other.f_Raw;
        }

        /// @brief Less than
        /// @param other Other value
        /// @return this < other
        bool lt(const RRValue& other) const
        {
            return f_Raw < other.f_Raw;
        }

        /// @brief Less than or equal to
        /// @param other Other value
        /// @return this <= other
        bool le(const RRValue& other) const
        {
            return f_Raw <= other.f_Raw;
        }

        /// @brief Copy assignment for RRValue
        /// @param src Source
        RRValue& copyass(const RRValue &src)
        {
            if (&src != this) f_Raw = src.f_Raw;
            return *this;
        }

        /// @brief Move assignment for RRValue
        /// @param src Source
        RRValue& moveass(RRValue &&src)
        {
            if (&src != this) f_Raw = src.f_Raw;
            return *this;
        }

        /// @brief Returns the whole part of the value
        /// @return Whole part of the value
        TRaw get_Whole() const { return f_Raw >> TFrac; }
        
        /// @brief Returns the fractional part of the value
        /// @return Fractional part of the value
        TRaw get_Fract() const { return f_Raw & f_FractMask; }

        /// @brief Rounds down to the nearest whole number
        /// @return Nearest whole number that's <= this
        RRValue floorNearest() const { return RRValue(f_Raw & f_FractMask_Inv); }

        /// @brief Rounds up to the nearest whole number
        /// @return Nearest whole number that's >= this
        RRValue ceilNearest() const { return RRValue((f_Raw + f_FractMask) & f_FractMask_Inv); }

        /// @brief Rounds to the nearest whole number
        /// @return Nearest whole number
        RRValue roundNearest() const { return RRValue((f_Raw + f_FractHalf) & f_FractMask_Inv); }

        /// @brief Rounds down to the nearest whole number
        /// @return Nearest whole number that's <= this
        TRaw floorToWhole() const { return f_Raw >> TFrac; }

        /// @brief Rounds up to the nearest whole number
        /// @return Nearest whole number that's >= this
        TRaw ceilToWhole() const { return (f_Raw + f_FractMask) >> TFrac; }

        /// @brief Rounds to the nearest whole number
        /// @return Nearest whole number
        TRaw roundToWhole() const { return (f_Raw + f_FractHalf) >> TFrac; }

        #pragma endregion
    };
}

#endif