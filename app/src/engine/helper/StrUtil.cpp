#include "engine/helper/StrUtil.h"

using namespace engine::helper;

size_t StrUtil::findChar(const std::string& str, char c, size_t beg, size_t len, bool returnLast)
{
    size_t found = SIZE_MAX;
    if (beg < str.length())
    {
        // Determine end
        size_t end = str.length() - beg;
        if (end > len) end = len;
        end += beg;
        // Search for character
        while (beg < end)
        {
            if (str[beg] == c)
            {
                found = beg;
                if (!returnLast) break;
            }
            ++beg;
        }
    }
    return found;
}

bool StrUtil::startsWith(const std::string& str, const std::string& substr)
{
    // Make sure substring can fit within string
    if (str.length() < substr.length()) return false;
    // Check characters
    for (size_t i = 0; i < substr.length(); ++i)
    {
        if (str[i] != substr[i]) return false;
    }
    // Success!!!
    return true;
}

bool StrUtil::endsWith(const std::string& str, const std::string& substr)
{
    // Make sure substring can fit within string
    if (str.length() < substr.length()) return false;
    // Check characters
    size_t beg = str.length() - substr.length();
    for (size_t i = 0; i < substr.length(); ++i)
    {
        if (str[beg + i] != substr[i]) return false;
    }
    // Success!!!
    return true;
}

bool StrUtil::noCaseEqu(const std::string& s0, const std::string& s1)
{
    // Check lengths
    if (s0.length() != s1.length()) return false;
    // Check characters
    for (size_t i = 0; i < s0.length(); ++i)
    {
        char c0 = s0[i]; if (c0 >= 'a' && c0 <= 'z') c0 -= 'a' - 'A';
        char c1 = s1[i]; if (c1 >= 'a' && c1 <= 'z') c1 -= 'a' - 'A';
        if (c0 != c1) return false;
    }
    // Equal!!!
    return true;
}