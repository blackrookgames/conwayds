#include "engine/io/DirUtil.h"

#include <dirent.h>
#include <sstream>

using namespace engine::io;

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