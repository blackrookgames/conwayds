#include <nds.h>
#include <stdio.h>

#include "DataBitmap.h"
// #include "DataChamp.h"

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

	int bg3 = bgInit(3, BgType_Bmp8, BgSize_B8_256x256, 0,0);

	DC_FlushRange(DataBitmap::bitmap_data, DataBitmap::bitmap_size);
	dmaCopy(DataBitmap::bitmap_data, bgGetGfxPtr(bg3), DataBitmap::bitmap_size);
	
	DC_FlushRange(DataBitmap::palette_data, DataBitmap::palette_size);
	dmaCopy(DataBitmap::palette_data, BG_PALETTE, DataBitmap::palette_size);

	while(pmMainLoop())
	{
		swiWaitForVBlank();
		scanKeys();
		if (keysDown() & KEY_START)
			break;
	}
	return 0;
}
