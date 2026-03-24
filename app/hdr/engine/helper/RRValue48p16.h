#include <ostream>

#include "./_macros.h"
#include "./RRValue.h"

#ifndef ENGINE_HELPER_RRVALUE48P16_H
#define ENGINE_HELPER_RRVALUE48P16_H

namespace engine::helper
{
    /// @brief Represents a 48.16 fixed-point value
    class RRValue48p16 : public RRValue<s64, 16>
    {
        #pragma region init

        public:

        /// @brief Empty constructor for RRValue48p16
        RRValue48p16();

        /// @brief Constructor for RRValue48p16
        /// @param raw Raw value
        RRValue48p16(s64 raw);

        /// @brief CSonstructor for RRValue48p16
        /// @param whole Whole part
        /// @param fract Fractional part
        RRValue48p16(s64 whole, s64 fract);

        /// @brief Copy constructor for RRValue48p16
        /// @param src Source
        RRValue48p16(const RRValue48p16& src);

        /// @brief Copy constructor for RRValue48p16
        /// @param src Source
        RRValue48p16(const RRValue<s64, 16>& src);

        /// @brief Move constructor for RRValue48p16
        /// @param src Source
        RRValue48p16(RRValue48p16&& src);

        /// @brief Move constructor for RRValue48p16
        /// @param src Source
        RRValue48p16(RRValue<s64, 16>&& src);

        virtual ~RRValue48p16() override;

        #pragma endregion

        #pragma region operators

        public:

        /// @brief Copy assignment for RRValue48p16
        /// @param src Source
        RRValue48p16& operator=(const RRValue48p16 &src);

        /// @brief Copy assignment for RRValue48p16
        /// @param src Source
        RRValue48p16& operator=(const RRValue<s64, 16> &src);

        /// @brief Move assignment for RRValue48p16
        /// @param src Source
        RRValue48p16& operator=(RRValue48p16 &&src);

        /// @brief Move assignment for RRValue48p16
        /// @param src Source
        RRValue48p16& operator=(RRValue<s64, 16> &&src);

        #pragma endregion
    };

    #pragma region operators

    inline RRValue48p16 operator +(const RRValue48p16& v0, const RRValue48p16& v1) { return static_cast<RRValue48p16>(v0.add(v1)); }
    inline RRValue48p16 operator -(const RRValue48p16& v0, const RRValue48p16& v1) { return static_cast<RRValue48p16>(v0.sub(v1)); }
    inline RRValue48p16 operator *(const RRValue48p16& v0, const RRValue48p16& v1) { return static_cast<RRValue48p16>(v0.mul(v1)); }
    inline RRValue48p16 operator /(const RRValue48p16& v0, const RRValue48p16& v1) { return static_cast<RRValue48p16>(v0.div(v1)); }
    inline RRValue48p16 operator -(const RRValue48p16& v) { return static_cast<RRValue48p16>(v.neg()); }
    inline bool operator ==(const RRValue48p16& v0, const RRValue48p16& v1) { return v0.equ(v1); }
    inline bool operator !=(const RRValue48p16& v0, const RRValue48p16& v1) { return v0.neq(v1); }
    inline bool operator >(const RRValue48p16& v0, const RRValue48p16& v1) { return v0.gt(v1); }
    inline bool operator >=(const RRValue48p16& v0, const RRValue48p16& v1) { return v0.ge(v1); }
    inline bool operator <(const RRValue48p16& v0, const RRValue48p16& v1) { return v0.lt(v1); }
    inline bool operator <=(const RRValue48p16& v0, const RRValue48p16& v1) { return v0.le(v1); }

    inline std::ostream& operator <<(std::ostream& out, const RRValue48p16& v) { out << v.toStr(); return out; }

    #pragma endregion
}

#endif