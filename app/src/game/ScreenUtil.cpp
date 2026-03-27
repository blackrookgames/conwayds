#include "game/ScreenUtil.h"

#include "engine/data/RLE.h"

using namespace game;

void ScreenUtil::load(const u16* in_data, size_t in_len, u16*& out_data, size_t& out_len)
{
    static constexpr size_t offset = 1;
    // Extract
    u16* temp_data;
    size_t temp_len;
    engine::data::RLE::extract(in_data, in_len, temp_data, temp_len);
    if (temp_len <= offset) { out_data = nullptr; out_len = 0; return; }
    // Create final array
    out_len = temp_len - offset;
    out_data = new u16[out_len];
    std::copy(temp_data + offset, temp_data + temp_len, out_data);
    delete[] temp_data;
}