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

        /// @brief Move constructor for RRValue32
        /// @param src Source
        RRValue32(RRValue32&& src);

        virtual ~RRValue32() override;

        #pragma endregion

        #pragma region operators

        public:

        /// @brief Copy assignment for RRValue32
        /// @param src Source
        RRValue32& operator=(const RRValue32 &src);

        /// @brief Move assignment for RRValue32
        /// @param src Source
        RRValue32& operator=(RRValue32 &&src);

        #pragma endregion
    };
}

#endif