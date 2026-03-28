#include "engine/helper/DirUtil.h"

#include <dirent.h>
#include <sstream>
#include <vector>

using namespace engine::helper;

void DirUtil::getPaths(const std::string& path, std::string*& paths, u16& count, 
    bool full, bool getFiles, bool getDirs)
{
    paths = nullptr; count = 0;
    // Open directory
	DIR* pdir = opendir(path.c_str());
    if (pdir == nullptr) return;
    // Get paths
    std::vector<std::string> pathList;
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
            std::ostringstream os;
            if (full) os << path << '/';
            os << pent->d_name;
            pathList.push_back(os.str());
        }
    }
    closedir(pdir);
    // Create array
    if (pathList.size() > 0)
    {
        count = pathList.size();
        paths = new std::string[count];
        std::string* optr = paths;
        for (auto iptr = pathList.begin(); iptr != pathList.end(); ++iptr)
            *(optr++) = std::move(*iptr);
    }
}