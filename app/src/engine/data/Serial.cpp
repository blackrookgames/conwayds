#include "engine/data/Serial.h"

#include <algorithm>
#include <cstdio>

using namespace engine::data;

bool Serial::load_file(const char* path)
{
    bool success = false;
    FILE* f = fopen(path, "rb");
    if (!f) return false;
    {
        // Get size of data
        fseek(f, 0, SEEK_END);
        long rawsize = ftell(f);
        if (rawsize < 0) goto close;
        size_t size = rawsize;
        fseek(f, 0, SEEK_SET);
        // Read data from file
        char* data = (char*)malloc(size);
        size_t read = fread(data, 1, size, f);
        if (read == size)
            success = load(data, size);
        free(data);
    }
close:
    fclose(f);
    // Return
    return success;
}

bool Serial::save_file(const char* path)
{
    // Create save data
    char* data; size_t size;
    if (!save(data, size)) return false;
    // Pad save data
    bool success = false;
    if ((size % 4) != 0)
    {
        char* prev_data = data;
        size_t prev_size = size;
        // Create padded array
        size = ((size + 3) / 4) * 4; data = new char[size];
        std::copy(prev_data, prev_data + prev_size, data);
        // Delete old
        delete[] prev_data;
    }
    // Save to file
    FILE* f = fopen(path, "wb");
    if (f)
    {
        success = (fwrite(data, sizeof(char), size, f) == size);
        fclose(f);
    }
    // Finish
    delete[] data;
    return success;
}