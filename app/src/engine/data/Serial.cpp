#include "engine/data/Serial.h"

#include <algorithm>
#include <cstdio>

#include "engine/helper/_macros.h"
#include "engine/io/IOUtil.h"

using namespace engine::data;

bool Serial::load_file(const char* path)
{
    char* data; size_t size;
    if (!engine::io::IOUtil::load(path, data, size)) return false;
    bool success = load(data, size);
    DELETE_ARRAY(data);
    return success;
}

bool Serial::save_file(const char* path)
{
    char* data; size_t size;
    if (!save(data, size)) return false;
    bool success = engine::io::IOUtil::save(path, data, size);
    DELETE_ARRAY(data);
    return success;
}