#include "game/FileUtil.h"

#include "engine/helper/StrUtil.h"
#include "engine/io/DirUtil.h"

using namespace game;

#pragma region const

const std::string FileUtil::extension = ".bin";

const std::string FileUtil::sample_Prefix = "SAMP:";

const std::string FileUtil::sample_Dir = "nitro:/samples";

const std::string FileUtil::user_Prefix = "USER:";

const std::string FileUtil::user_Dir = "fat:/conwayds/patterns";

const std::string FileUtil::about_Dir = "nitro:/about";

const std::string FileUtil::about_Path = "nitro:/about/__.txt";

#pragma endregion

#pragma region helper functions

void FileUtil::m_FilterPaths(std::vector<engine::io::Path>& paths)
{
    auto iptr = paths.begin();
    while (iptr != paths.end())
    {
        if (engine::helper::StrUtil::endsWith(iptr->displayName(), extension)) ++iptr;
        else paths.erase(iptr);
    }
}

#pragma endregion

#pragma region functions

void FileUtil::getPatterns(engine::io::Path*& paths, u16& count, bool sample)
{
    // Get samples
    std::vector<engine::io::Path> samps;
    if (sample) samps = engine::io::DirUtil::getPaths(sample_Dir, true, false);
    m_FilterPaths(samps);
    // Get user
    auto users = engine::io::DirUtil::getPaths(user_Dir, true, false);
    m_FilterPaths(users);
    // Create final array
    size_t rawCount = samps.size() + users.size();
    count = MATH_MIN(rawCount, capacity);
    if (count > 0)
    {
        // Create array
        paths = new engine::io::Path[count];
        engine::io::Path* optr = paths;
        size_t currentCount = 0;
        // Add samples
        for (auto iptr = samps.begin(); iptr != samps.end(); ++iptr)
        {
            if (currentCount == count) break;
            // Copy path
            *optr = std::move(*iptr);
            // Fix display name
            size_t ext = engine::helper::StrUtil::findChar(optr->displayName(), '.', 0, SIZE_MAX, true);
            optr->displayName() = sample_Prefix + optr->displayName().substr(0, ext);
            // Next
            ++optr; ++currentCount;
        }
        // Add user
        for (auto iptr = users.begin(); iptr != users.end(); ++iptr)
        {
            if (currentCount == count) break;
            // Copy path
            *optr = std::move(*iptr);
            // Fix display name
            size_t ext = engine::helper::StrUtil::findChar(optr->displayName(), '.', 0, SIZE_MAX, true);
            optr->displayName() = user_Prefix + optr->displayName().substr(0, ext);
            // Next
            ++optr; ++currentCount;
        }
    }
    else paths = nullptr;
}

#pragma endregion