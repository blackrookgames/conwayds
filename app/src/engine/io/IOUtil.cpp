#include "engine/io/IOUtil.h"

#include <__.h>

#include "engine/helper/_macros.h"

using namespace engine::io;

bool IOUtil::load(const char* path, char*& data, size_t& size)
{
    data = nullptr; size = 0;
    FILE* f = fopen(path, "rb");
    if (f)
    {
        bool success = false;
        long rawsize;
    getSize:
        fseek(f, 0, SEEK_END);
        rawsize = ftell(f);
        if (rawsize < 0) goto close;
        size = rawsize;
        fseek(f, 0, SEEK_SET);
    readData:
        if (size > 0)
        {
            data = new char[size];
            success = (fread(data, 1, size, f) == size);
            if (!success) delete[] data;
        }
        else success = true;
    close:
        fclose(f);
        return success;
    }
    else return false;
}

bool IOUtil::load(const std::string& path, char*& data, size_t& size)
{
    return load(path.c_str(), data, size);
}

bool IOUtil::save(const char* path, const char* data, size_t size)
{
    FILE* f = fopen(path, "wb");
    if (f)
    {
        bool success = false;
        char* tempData = nullptr; size_t tempSize = 0; 
        if (size > 0)
        {
            // Create padded copy
            tempSize = ((size + 3) / 4) * 4;
            tempData = new char[tempSize];
            std::copy(data, data + size, tempData);
            std::fill(tempData + size, tempData + tempSize, 0);
            // Save
            success = (fwrite(tempData, sizeof(char), tempSize, f) == tempSize);
        }
        else success = true;
    close:
        DELETE_ARRAY(tempData)
        fclose(f);
        return success;
    }
    return false;
}

bool IOUtil::save(const std::string& path, const char* data, size_t size)
{
    return save(path.c_str(), data, size);
}