#include "game/FileUtil.h"

#include "engine/helper/StrUtil.h"
#include "engine/io/DirUtil.h"

using namespace game;

#pragma region const

const std::string FileUtil::extension = ".bin";

const std::string FileUtil::sample_Prefix = "SAMP:";

const std::string FileUtil::sample_Dir = "nitro:/samples";

const std::string FileUtil::user_prefix = "USER:";

const std::string FileUtil::user_Dir = "fat:/conwayds/patterns";

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

void FileUtil::getPatterns(engine::io::Path*& paths, u16& count)
{
    // Get samples
    auto samps = engine::io::DirUtil::getPaths(sample_Dir, true, false);
    m_FilterPaths(samps);
    // Create final array
    count = samps.size();
    if (count > 0)
    {
        // Create array
        paths = new engine::io::Path[count];
        engine::io::Path* optr = paths;
        // Add samples
        for (auto iptr = samps.begin(); iptr != samps.end(); ++iptr)
        {
            // Copy path
            *optr = std::move(*iptr);
            // Fix display name
            size_t ext = engine::helper::StrUtil::findChar(optr->displayName(), '.', 0, SIZE_MAX, true);
            optr->displayName() = sample_Prefix + optr->displayName().substr(0, ext);
            // Next
            ++optr;
        }
    }
    else paths = nullptr;
}

#pragma endregion