#include "engine/helper/RRValue24p8.h"

#include <utility>

using namespace engine::helper;

#pragma region init

RRValue24p8::RRValue24p8() : RRValue() { }

RRValue24p8::RRValue24p8(s32 raw) : RRValue(raw) { }

RRValue24p8::RRValue24p8(s32 whole, s32 fract) : RRValue(whole, fract) { }

RRValue24p8::RRValue24p8(const RRValue24p8& src) : RRValue(src) { }

RRValue24p8::RRValue24p8(const RRValue<s32, 8>& src) : RRValue(src) { }

RRValue24p8::RRValue24p8(RRValue24p8&& src) : RRValue(std::move(src)) { }

RRValue24p8::RRValue24p8(RRValue<s32, 8>&& src) : RRValue(std::move(src)) { }

RRValue24p8::~RRValue24p8() { }

#pragma endregion

#pragma region operators

RRValue24p8& RRValue24p8::operator=(const RRValue24p8 &src) { copyass(src); return *this; }

RRValue24p8& RRValue24p8::operator=(const RRValue<s32, 8> &src) { copyass(src); return *this; }

RRValue24p8& RRValue24p8::operator=(RRValue24p8 &&src) { moveass(std::move(src)); return *this; }

RRValue24p8& RRValue24p8::operator=(RRValue<s32, 8> &&src) { moveass(std::move(src)); return *this; }

#pragma endregion