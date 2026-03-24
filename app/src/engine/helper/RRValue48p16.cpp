#include "engine/helper/RRValue48p16.h"

#include <utility>

using namespace engine::helper;

#pragma region init

RRValue48p16::RRValue48p16() : RRValue() { }

RRValue48p16::RRValue48p16(s64 raw) : RRValue(raw) { }

RRValue48p16::RRValue48p16(s64 whole, s64 fract) : RRValue(whole, fract) { }

RRValue48p16::RRValue48p16(const RRValue48p16& src) : RRValue(src) { }

RRValue48p16::RRValue48p16(const RRValue<s64, 16>& src) : RRValue(src) { }

RRValue48p16::RRValue48p16(RRValue48p16&& src) : RRValue(std::move(src)) { }

RRValue48p16::RRValue48p16(RRValue<s64, 16>&& src) : RRValue(std::move(src)) { }

RRValue48p16::~RRValue48p16() { }

#pragma endregion

#pragma region operators

RRValue48p16& RRValue48p16::operator=(const RRValue48p16 &src) { copyass(src); return *this; }

RRValue48p16& RRValue48p16::operator=(const RRValue<s64, 16> &src) { copyass(src); return *this; }

RRValue48p16& RRValue48p16::operator=(RRValue48p16 &&src) { moveass(std::move(src)); return *this; }

RRValue48p16& RRValue48p16::operator=(RRValue<s64, 16> &&src) { moveass(std::move(src)); return *this; }

#pragma endregion