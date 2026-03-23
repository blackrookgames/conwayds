#include <nds.h>

#include <__.h>

#ifndef ENGINE_HELPER_RRVALUE_H
#define ENGINE_HELPER_RRVALUE_H

namespace engine::helper
{
    /// @brief Represents a fixed-point value with crude operators
    /// @tparam TRaw Raw data type
    /// @tparam TBig Data type to use when multiplying and dividing
    template<typename TRaw, typename TBig>
    class RRValue
    {
        static constexpr u8 totalSize = sizeof(TRaw) * 8;
        static constexpr u8 fracSize = totalSize / 4;
        static constexpr u8 wholeSize = totalSize - fracSize;
        static constexpr TRaw fractMask = ((TRaw)1 << fracSize) - 1;
        static constexpr size_t wholeBufLen = (wholeSize < 1) ? 1 : wholeSize;
        static constexpr size_t fractBufLen = (fracSize < 1) ? 1 : fracSize;

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
        RRValue(TRaw whole, TRaw fract) { f_Raw = (whole << fracSize) | fract; }

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
        /// @return Null-terminated string (can be deleted with delete[])
        char* toStr() const
        {
            char* iptr;
            char* optr;
            // Get absolute value
            bool isneg = f_Raw < 0;
            TRaw abs = isneg ? (-f_Raw) : f_Raw;
            // Whole number
            TRaw whole = abs >> fracSize;
            u8 whole_Len = 0;
            char whole_Chars[wholeBufLen];
            optr = whole_Chars + wholeBufLen;
            while (true)
            {
                *(--optr) = 0x30 + (char)(whole % 10);
                ++whole_Len;
                whole /= 10;
                if (whole == 0) break;
            }
            // Fractional number
            TRaw fract = abs & fractMask;
            u8 fract_Len = 0;
            char fract_Chars[fractBufLen];
            optr = fract_Chars;
            while (fract_Len < fractBufLen)
            {
                fract *= 10;
                *(optr++) = 0x30 + (char)(fract >> fracSize);
                ++fract_Len;
                fract &= fractMask;
                if (fract == 0) break;
            }
            // Create final string
            char* str = new char[(isneg ? 1 : 0) + whole_Len + 1 + fract_Len + 1];
            {
                optr = str;
                // Negative
                if (isneg) *(optr++) = '-';
                // Whole
                iptr = whole_Chars + wholeBufLen - whole_Len;
                for (u8 i = 0; i < whole_Len; ++i) *(optr++) = *(iptr++);
                // Period
                *(optr++) = '.';
                // Fraction
                iptr = fract_Chars;
                for (u8 i = 0; i < fract_Len; ++i) *(optr++) = *(iptr++);
                // Null
                *optr = 0;
            }
            return str;
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
            // Cast
            TBig v0 = f_Raw; TBig v1 = other.f_Raw;
            // Operate
            TBig ans = (v0 * v1) >> fracSize;
            // Create final
            return RRValue((TRaw)ans);
        }

        /// @brief Division
        /// @param other Value to divide by
        /// @return this / other
        RRValue div(const RRValue& other) const
        {
            // Cast
            TBig v0 = f_Raw; TBig v1 = other.f_Raw;
            // Operate
            TBig ans = ((v0 << fracSize) / v1);
            // Create final
            return RRValue((TRaw)ans);
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
        bool equ(const RRValue32& other) const
        {
            return f_Raw == other.f_Raw;
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

        #pragma endregion
    };
}

#endif