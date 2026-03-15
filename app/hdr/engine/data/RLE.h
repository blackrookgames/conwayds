#include <nds.h>
#include <vector>

#ifndef ENGINE_DATA_RLE_H
#define ENGINE_DATA_RLE_H

namespace engine::data
{
    /// @brief Utility for RLE-compressed data
    class RLE
    {
        #pragma region helper functions 

        private: 

        template<typename T>
        static void m_Extract(const T* in_data, size_t in_len, T*& out_data, size_t& out_len)
        {
            // Extract data
            std::vector<T> temp;
            if (in_len > 0)
            {
                const T* iptr = in_data;
                const T* iend = in_data + in_len;
                // Get RLE prefix
                T prefix = *(iptr++);
                // Extract data
                while (iptr < iend)
                {
                    // Is the start of RLE compressed data?
                    if (*iptr == prefix)
                    {
                        // Make sure there's no premature end
                        if ((iptr + 3) > iend) break;
                        // Get value and occurrances
                        T value = *(++iptr);
                        T occurances = *(++iptr);
                        // Copy
                        while (occurances > 0) { temp.push_back(value); --occurances; }
                        // Next
                        ++iptr;
                    }
                    // No! Just copy the value
                    else temp.push_back(*(iptr++));
                }
            }
            // Output data
            if (temp.size() > 0)
            {
                out_data = new T[temp.size()];
                out_len = temp.size();
                {
                    T* optr = out_data;
                    for (auto iptr = temp.begin(); iptr != temp.end(); ++iptr)
                        *(optr++) = *iptr;
                }
            }
            else
            {
                out_data = nullptr;
                out_len = 0;
            }
        }

        #pragma endregion

        #pragma region functions

        public:

        /// @brief Extracts RLE compressed data contained within an array
        /// @param in_data Input array
        /// @param in_len Number of items in input array 
        /// @param out_data Output array; safe to delete with delete[]
        /// @param out_len Number of items in output array
        static void extract(const u8* in_data, size_t in_len, u8*& out_data, size_t& out_len)
        { RLE::m_Extract(in_data, in_len, out_data, out_len); }

        /// @brief Extracts RLE compressed data contained within an array
        /// @param in_data Input array
        /// @param in_len Number of items in input array 
        /// @param out_data Output array; safe to delete with delete[]
        /// @param out_len Number of items in output array
        static void extract(const s8* in_data, size_t in_len, s8*& out_data, size_t& out_len)
        { RLE::m_Extract(in_data, in_len, out_data, out_len); }

        /// @brief Extracts RLE compressed data contained within an array
        /// @param in_data Input array
        /// @param in_len Number of items in input array 
        /// @param out_data Output array; safe to delete with delete[]
        /// @param out_len Number of items in output array
        static void extract(const u16* in_data, size_t in_len, u16*& out_data, size_t& out_len)
        { RLE::m_Extract(in_data, in_len, out_data, out_len); }

        /// @brief Extracts RLE compressed data contained within an array
        /// @param in_data Input array
        /// @param in_len Number of items in input array 
        /// @param out_data Output array; safe to delete with delete[]
        /// @param out_len Number of items in output array
        static void extract(const s16* in_data, size_t in_len, s16*& out_data, size_t& out_len)
        { RLE::m_Extract(in_data, in_len, out_data, out_len); }

        /// @brief Extracts RLE compressed data contained within an array
        /// @param in_data Input array
        /// @param in_len Number of items in input array 
        /// @param out_data Output array; safe to delete with delete[]
        /// @param out_len Number of items in output array
        static void extract(const u32* in_data, size_t in_len, u32*& out_data, size_t& out_len)
        { RLE::m_Extract(in_data, in_len, out_data, out_len); }

        /// @brief Extracts RLE compressed data contained within an array
        /// @param in_data Input array
        /// @param in_len Number of items in input array 
        /// @param out_data Output array; safe to delete with delete[]
        /// @param out_len Number of items in output array
        static void extract(const s32* in_data, size_t in_len, s32*& out_data, size_t& out_len)
        { RLE::m_Extract(in_data, in_len, out_data, out_len); }

        /// @brief Extracts RLE compressed data contained within an array
        /// @param in_data Input array
        /// @param in_len Number of items in input array 
        /// @param out_data Output array; safe to delete with delete[]
        /// @param out_len Number of items in output array
        static void extract(const u64* in_data, size_t in_len, u64*& out_data, size_t& out_len)
        { RLE::m_Extract(in_data, in_len, out_data, out_len); }

        /// @brief Extracts RLE compressed data contained within an array
        /// @param in_data Input array
        /// @param in_len Number of items in input array 
        /// @param out_data Output array; safe to delete with delete[]
        /// @param out_len Number of items in output array
        static void extract(const s64* in_data, size_t in_len, s64*& out_data, size_t& out_len)
        { RLE::m_Extract(in_data, in_len, out_data, out_len); }

        #pragma endregion
    };
}

#endif