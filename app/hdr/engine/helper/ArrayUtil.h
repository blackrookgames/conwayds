#include <nds.h>

#ifndef ENGINE_HELPER_ARRAYUTIL_H
#define ENGINE_HELPER_ARRAYUTIL_H

namespace engine::helper
{
    /// @brief Utility for array-related operations
    class ArrayUtil
    {
        public:

        /// @brief Performs a copy operation within a range
        /// @tparam T Data type
        /// @param input_Start Pointer to start of input data
        /// @param input_End Pointer to end of input data
        /// @param input_Inc Input increment; if input_Inc > 1, input_Inc - 1 input items are skipped
        /// @param output Pointer to start of output data
        /// @param output_Inc Output Increment; if output_Inc > 1, output_Inc - 1 output items are skipped
        template<typename T>
        static void copy(const T* input_Start, const T* input_End, u32 input_Inc, T* output, u32 output_Inc)
        {
            while (input_Start < input_End)
            {
                *output = *input_Start;
                input_Start += input_Inc;
                output += output_Inc;
            }
        }

        /// @brief Performs a copy operation within a range
        /// @tparam T Data type
        /// @param input_Start Pointer to start of input data
        /// @param input_End Pointer to end of input data
        /// @param output Pointer to start of output data
        /// @param inc Increment; if inc > 1, inc - 1 input items are skipped. This applies to both input and output
        template<typename T>
        static void copy(const T* input_Start, const T* input_End, T* output, u32 inc)
        {
            copy(input_Start, input_End, inc, output, inc);
        }
    };
}

#endif