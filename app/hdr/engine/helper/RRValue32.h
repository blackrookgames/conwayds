#include <ostream>

#include "./_macros.h"
#include "./RRValue.h"

#ifndef ENGINE_HELPER_RRVALUE32_H
#define ENGINE_HELPER_RRVALUE32_H

namespace engine::helper
{
    /// @brief Represents a 32-bit fixed value
    class RRValue32 : public RRValue<s32, s64>
    {
        #pragma region init

        public:

        /// @brief Empty constructor for RRValue32
        RRValue32();

        /// @brief Constructor for RRValue32
        /// @param raw Raw value
        RRValue32(s32 raw);

        /// @brief CSonstructor for RRValue32
        /// @param whole Whole part
        /// @param fract Fractional part
        RRValue32(s32 whole, s32 fract);

        /// @brief Copy constructor for RRValue32
        /// @param src Source
        RRValue32(const RRValue32& src);

        /// @brief Copy constructor for RRValue32
        /// @param src Source
        RRValue32(const RRValue<s32, s64>& src);

        /// @brief Move constructor for RRValue32
        /// @param src Source
        RRValue32(RRValue32&& src);

        /// @brief Move constructor for RRValue32
        /// @param src Source
        RRValue32(RRValue<s32, s64>&& src);

        virtual ~RRValue32() override;

        #pragma endregion

        #pragma region operators

        public:

        /// @brief Copy assignment for RRValue32
        /// @param src Source
        RRValue32& operator=(const RRValue32 &src);

        /// @brief Copy assignment for RRValue32
        /// @param src Source
        RRValue32& operator=(const RRValue<s32, s64> &src);

        /// @brief Move assignment for RRValue32
        /// @param src Source
        RRValue32& operator=(RRValue32 &&src);

        /// @brief Move assignment for RRValue32
        /// @param src Source
        RRValue32& operator=(RRValue<s32, s64> &&src);

        #pragma endregion
    };

    #pragma region operators

    inline RRValue32 operator +(const RRValue32& v0, const RRValue32& v1) { return static_cast<RRValue32>(v0.add(v1)); }
    inline RRValue32 operator -(const RRValue32& v0, const RRValue32& v1) { return static_cast<RRValue32>(v0.sub(v1)); }
    inline RRValue32 operator *(const RRValue32& v0, const RRValue32& v1) { return static_cast<RRValue32>(v0.mul(v1)); }
    inline RRValue32 operator /(const RRValue32& v0, const RRValue32& v1) { return static_cast<RRValue32>(v0.div(v1)); }
    inline RRValue32 operator -(const RRValue32& v) { return static_cast<RRValue32>(v.neg()); }
    inline bool operator ==(const RRValue32& v0, const RRValue32& v1) { return v0.equ(v1); }
    inline bool operator !=(const RRValue32& v0, const RRValue32& v1) { return v0.neq(v1); }
    inline bool operator >(const RRValue32& v0, const RRValue32& v1) { return v0.gt(v1); }
    inline bool operator >=(const RRValue32& v0, const RRValue32& v1) { return v0.ge(v1); }
    inline bool operator <(const RRValue32& v0, const RRValue32& v1) { return v0.lt(v1); }
    inline bool operator <=(const RRValue32& v0, const RRValue32& v1) { return v0.le(v1); }

    inline std::ostream& operator <<(std::ostream& out, const RRValue32& v) { out << v.toStr(); return out; }

    #pragma endregion
}

#endif