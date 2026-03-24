#include <ostream>

#include "./_macros.h"
#include "./RRValue.h"

#ifndef ENGINE_HELPER_RRVALUE24P8_H
#define ENGINE_HELPER_RRVALUE24P8_H

namespace engine::helper
{
    /// @brief Represents a 24.8 fixed-point value
    class RRValue24p8 : public RRValue<s32, 8>
    {
        #pragma region init

        public:

        /// @brief Empty constructor for RRValue24p8
        RRValue24p8();

        /// @brief Constructor for RRValue24p8
        /// @param raw Raw value
        RRValue24p8(s32 raw);

        /// @brief CSonstructor for RRValue24p8
        /// @param whole Whole part
        /// @param fract Fractional part
        RRValue24p8(s32 whole, s32 fract);

        /// @brief Copy constructor for RRValue24p8
        /// @param src Source
        RRValue24p8(const RRValue24p8& src);

        /// @brief Copy constructor for RRValue24p8
        /// @param src Source
        RRValue24p8(const RRValue<s32, 8>& src);

        /// @brief Move constructor for RRValue24p8
        /// @param src Source
        RRValue24p8(RRValue24p8&& src);

        /// @brief Move constructor for RRValue24p8
        /// @param src Source
        RRValue24p8(RRValue<s32, 8>&& src);

        virtual ~RRValue24p8() override;

        #pragma endregion

        #pragma region operators

        public:

        /// @brief Copy assignment for RRValue24p8
        /// @param src Source
        RRValue24p8& operator=(const RRValue24p8 &src);

        /// @brief Copy assignment for RRValue24p8
        /// @param src Source
        RRValue24p8& operator=(const RRValue<s32, 8> &src);

        /// @brief Move assignment for RRValue24p8
        /// @param src Source
        RRValue24p8& operator=(RRValue24p8 &&src);

        /// @brief Move assignment for RRValue24p8
        /// @param src Source
        RRValue24p8& operator=(RRValue<s32, 8> &&src);

        #pragma endregion
    };

    #pragma region operators

    inline RRValue24p8 operator +(const RRValue24p8& v0, const RRValue24p8& v1) { return static_cast<RRValue24p8>(v0.add(v1)); }
    inline RRValue24p8 operator -(const RRValue24p8& v0, const RRValue24p8& v1) { return static_cast<RRValue24p8>(v0.sub(v1)); }
    inline RRValue24p8 operator *(const RRValue24p8& v0, const RRValue24p8& v1) { return static_cast<RRValue24p8>(v0.mul(v1)); }
    inline RRValue24p8 operator /(const RRValue24p8& v0, const RRValue24p8& v1) { return static_cast<RRValue24p8>(v0.div(v1)); }
    inline RRValue24p8 operator -(const RRValue24p8& v) { return static_cast<RRValue24p8>(v.neg()); }
    inline bool operator ==(const RRValue24p8& v0, const RRValue24p8& v1) { return v0.equ(v1); }
    inline bool operator !=(const RRValue24p8& v0, const RRValue24p8& v1) { return v0.neq(v1); }
    inline bool operator >(const RRValue24p8& v0, const RRValue24p8& v1) { return v0.gt(v1); }
    inline bool operator >=(const RRValue24p8& v0, const RRValue24p8& v1) { return v0.ge(v1); }
    inline bool operator <(const RRValue24p8& v0, const RRValue24p8& v1) { return v0.lt(v1); }
    inline bool operator <=(const RRValue24p8& v0, const RRValue24p8& v1) { return v0.le(v1); }

    inline std::ostream& operator <<(std::ostream& out, const RRValue24p8& v) { out << v.toStr(); return out; }

    #pragma endregion
}

#endif