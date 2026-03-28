#include "engine/io/Path.h"

using namespace engine::io;

#pragma region init

Path::Path() : Path("", "", false) { }

Path::Path(std::string fullPath, std::string displayName, bool isDir)
{
    f_FullPath = std::move(fullPath);
    f_DisplayName = std::move(displayName);
    f_IsDir = isDir;
}

Path::Path(const Path& src)
{
    f_FullPath = src.f_FullPath;
    f_DisplayName = src.f_DisplayName;
    f_IsDir = src.f_IsDir;
}

Path::Path(Path&& src)
{
    f_FullPath = std::move(src.f_FullPath);
    f_DisplayName = std::move(src.f_DisplayName);
    f_IsDir = std::move(src.f_IsDir);
}

Path::~Path() { }

#pragma endregion

#pragma region operators

Path& Path::operator=(const Path& src)
{
    if (&src != this)
    {
        f_FullPath = src.f_FullPath;
        f_DisplayName = src.f_DisplayName;
        f_IsDir = src.f_IsDir;
    }
    return *this;
}

Path& Path::operator=(Path&& src)
{
    if (&src != this)
    {
        f_FullPath = std::move(src.f_FullPath);
        f_DisplayName = std::move(src.f_DisplayName);
        f_IsDir = std::move(src.f_IsDir);
    }
    return *this;
}

#pragma endregion

#pragma region properties

const std::string& Path::fullPath() const { return f_FullPath; }
std::string& Path::fullPath() { return f_FullPath; }

const std::string& Path::displayName() const { return f_DisplayName; }
std::string& Path::displayName() { return f_DisplayName; }

bool Path::isDir() const { return f_IsDir; }
void Path::isDir(bool value) { f_IsDir = value; }

#pragma endregion