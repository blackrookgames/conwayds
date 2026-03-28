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