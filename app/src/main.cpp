#include <nds.h>

#include <stdio.h>

static const u16 testSet[] = 
{
	0x0101, 0x0000, 0x0000, 0x0000, 
};
static const u16 testMap[] =
{
	0x0000, 0x0000, 0x0000, 0x0000, 
};
static const u16 testPal[] =
{
	0x0000, 0x7FFF, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,
	0x0000, 0x001F, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,
};

int main(void)
{
	consoleDebugInit(DebugDevice_NOCASH);
	
	fprintf(stderr, "Hello world!!!\n");

	videoSetMode(MODE_0_2D);
	vramSetBankA(VRAM_A_MAIN_BG);
	
	int bg = bgInit(0, BgType_Text4bpp, BgSize_T_256x256, 0, 1);
	u16* bgGfx = bgGetGfxPtr(bg);
	u16* bgMap = bgGetMapPtr(bg);
	
	DC_FlushRange(testSet, sizeof(testSet));
	dmaCopy(testSet, bgGfx, sizeof(testSet));

	DC_FlushRange(testMap, sizeof(testMap));
	dmaCopy(testMap, bgMap, sizeof(testMap));

	DC_FlushRange(testPal, sizeof(testPal));
	dmaCopy(testPal, BG_PALETTE, sizeof(testPal));

	while(pmMainLoop())
	{
		swiWaitForVBlank();
		scanKeys();
		if (keysDown() & KEY_START)
			break;
	}
	return 0;
}
