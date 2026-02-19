#include "entity/TestScene.h"

#include <stdio.h>

#include "Assets.h"
#include "entity/StartPattern.h"

using namespace entity;

#pragma region init

TestScene::TestScene() { }

TestScene::~TestScene() { }

#pragma endregion

#pragma region helper functions

void TestScene::m_enter()
{
    Scene::m_enter();

	videoSetMode(MODE_5_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);
	
	videoSetModeSub(MODE_5_2D);
    vramSetBankC(VRAM_C_SUB_BG_0x06200000);

	int main_3 = bgInit(3, BgType_Bmp8, BgSize_B8_256x256, 0, 0);
	u16* main_3_ptr = bgGetGfxPtr(main_3);

	int sub_3 = bgInitSub(3, BgType_Bmp8, BgSize_B8_256x256, 0, 0);
	u16* sub_3_ptr = bgGetGfxPtr(sub_3);

	dmaFillWords(0, main_3_ptr, 256 * 256);
	
	DC_FlushRange(Assets::palette_data, Assets::palette_size);
	dmaCopy(Assets::palette_data, BG_PALETTE, Assets::palette_size);
	dmaCopy(Assets::palette_data, BG_PALETTE_SUB, Assets::palette_size);
	
	StartPattern startPattern;
	for (u16 i = 0; i < 128; ++i)
		startPattern.cell(i, i, true);
	
	const bool* iptr = startPattern.cells();
	u16* optrM = main_3_ptr;
	u16* optrS = sub_3_ptr;
	for (u32 i = 0; i < PATTERN_AREA; i += 2)
	{
		u16 value = 0;
		if (*(iptr++)) value |= 0x0007;
		if (*(iptr++)) value |= 0x0700;
		*(optrM++) = value;
		*(optrS++) = value;
	}
}

void TestScene::m_exit()
{
    Scene::m_exit();
}

void TestScene::m_update()
{
    Scene::m_update();
	scanKeys();
	if (keysDown() & KEY_START)
    	fprintf(stderr, "Start\n");
}

#pragma endregion