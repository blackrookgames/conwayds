#include <nds.h>
#include <stdio.h>

#include "DataChamp.h"

int main(void)
{
	consoleDebugInit(DebugDevice_NOCASH);
	
	fprintf(stderr, "Hello world!!!\n");

	videoSetMode(MODE_0_2D);
	vramSetBankA(VRAM_A_MAIN_BG);
	
	int bg = bgInit(0, BgType_Text8bpp, BgSize_T_256x256, 0, 1);
	u16* bgGfx = bgGetGfxPtr(bg);
	u16* bgMap = bgGetMapPtr(bg);

	DC_FlushRange(DataChamp::tileset_data, DataChamp::tileset_size);
	dmaCopy(DataChamp::tileset_data, bgGfx, DataChamp::tileset_size);

	DC_FlushRange(DataChamp::tilemap_data, DataChamp::tilemap_size);
	dmaCopy(DataChamp::tilemap_data, bgMap, DataChamp::tilemap_size);

	DC_FlushRange(DataChamp::palette_data, DataChamp::palette_size);
	dmaCopy(DataChamp::palette_data, BG_PALETTE, DataChamp::palette_size);

	while(pmMainLoop())
	{
		swiWaitForVBlank();
		scanKeys();
		if (keysDown() & KEY_START)
			break;
	}
	return 0;
}
