#include "engine/helper/RRValue32.h"

#include <utility>

using namespace engine::helper;

#pragma region init

RRValue32::RRValue32() : RRValue() { }

RRValue32::RRValue32(s32 raw) : RRValue(raw) { }

RRValue32::RRValue32(s32 whole, s32 fract) : RRValue(whole, fract) { }

RRValue32::RRValue32(const RRValue32& src) : RRValue(src) { }

RRValue32::RRValue32(const RRValue<s32, s64>& src) : RRValue(src) { }

RRValue32::RRValue32(RRValue32&& src) : RRValue(std::move(src)) { }

RRValue32::RRValue32(RRValue<s32, s64>&& src) : RRValue(std::move(src)) { }

RRValue32::~RRValue32() { }

#pragma endregion

#pragma region operators

RRValue32& RRValue32::operator=(const RRValue32 &src) { copyass(src); return *this; }

RRValue32& RRValue32::operator=(const RRValue<s32, s64> &src) { copyass(src); return *this; }

RRValue32& RRValue32::operator=(RRValue32 &&src) { moveass(std::move(src)); return *this; }

RRValue32& RRValue32::operator=(RRValue<s32, s64> &&src) { moveass(std::move(src)); return *this; }

#pragma endregion