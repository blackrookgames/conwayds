#include "engine/data/Serial.h"

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