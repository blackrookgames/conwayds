#include <nds.h>
#include <stdio.h>

#include "Assets.h"
#include "StartPattern.h"

int main(void)
{
	consoleDebugInit(DebugDevice_NOCASH);
	
	fprintf(stderr, "Hello world!!!\n");

	/*
	videoSetMode(MODE_0_2D);
	vramSetBankA(VRAM_A_MAIN_BG);
	
	int bg = bgInit(0, BgType_Text4bpp, BgSize_T_256x256, 0, 1);
	u16* bgGfx = bgGetGfxPtr(bg);
	u16* bgMap = bgGetMapPtr(bg);

	DC_FlushRange(DataChamp::tileset_data, DataChamp::tileset_size);
	dmaCopy(DataChamp::tileset_data, bgGfx, DataChamp::tileset_size);

	DC_FlushRange(DataChamp::tilemap_data, DataChamp::tilemap_size);
	dmaCopy(DataChamp::tilemap_data, bgMap, DataChamp::tilemap_size);

	DC_FlushRange(DataChamp::palette_data, DataChamp::palette_size);
	dmaCopy(DataChamp::palette_data, BG_PALETTE, DataChamp::palette_size);
	*/

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

	StartPattern startPattern(7, 0);
	for (u16 i = 0; i < 128; ++i)
		startPattern.cell(i, i, true);
	startPattern.draw(main_3_ptr);
	startPattern.draw(sub_3_ptr);

	while(pmMainLoop())
	{
		swiWaitForVBlank();

		scanKeys();
		if (keysDown() & KEY_START)
			break;
	}
	return 0;
}
