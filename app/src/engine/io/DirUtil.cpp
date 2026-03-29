#include "engine/io/DirUtil.h"

#include <dirent.h>
#include <errno.h>
#include <sstream>
#include <sys/stat.h>

using namespace engine::io;

#pragma region functions

bool DirUtil::m_MakeDir(const std::string& path)
{
    // Make directory
    if (mkdir(path.c_str(), 0777) == 0) return true;
    // Check if directory already existed
    if (EEXIST) return true;
    // Fail
    return false;
}

#pragma endregion

#pragma region functions

std::vector<Path> DirUtil::getPaths(const std::string& path, bool getFiles, bool getDirs)
{
    std::vector<Path> paths;
	DIR* pdir = opendir(path.c_str());
    if (pdir != nullptr)
    {
        while(true)
        {
            dirent* pent = readdir(pdir);
            if(pent == nullptr) break;
            if(strcmp(".", pent->d_name) != 0 && strcmp("..", pent->d_name) != 0)
            {
                // Should we add it?
                if (pent->d_type == DT_DIR) { if (!getDirs) continue; }
                else { if (!getFiles) continue; }
                // Add it
                paths.push_back(Path(path + "/" + pent->d_name, pent->d_name, pent->d_type == DT_DIR));
            }
        }
        closedir(pdir);
    }
    return paths;
}

bool DirUtil::create(const std::string& path)
{
    for (size_t i = 0; i < path.length(); ++i)
    {
        if (path[i] != '/') continue;
        if (!m_MakeDir(path.substr(0, i))) return false;
    }
    return m_MakeDir(path);
}

#pragma endregion