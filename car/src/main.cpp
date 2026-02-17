#include <nds.h>
#include <stdio.h>

#include "Palette.h"
#include "Car00.h"
#include "Car01.h"
#include "Car02.h"
#include "Car03.h"
#include "Car04.h"
#include "Car05.h"
#include "Car06.h"
#include "Car07.h"
#include "Car08.h"
#include "Car09.h"
#include "Car10.h"
#include "Car11.h"
#include "Car12.h"
#include "Car13.h"
#include "Car14.h"
#include "Car15.h"
#include "Car16.h"
#include "Car17.h"
#include "Car18.h"
#include "Car19.h"
#include "Car20.h"
#include "Car21.h"
#include "Car22.h"
#include "Car23.h"
#include "Car24.h"
#include "Car25.h"
#include "Car26.h"
#include "Car27.h"
#include "Car28.h"
#include "Car29.h"
#include "Car30.h"
#include "Car31.h"
#include "Car32.h"
#include "Car33.h"
#include "Car34.h"
#include "Car35.h"
#include "Car36.h"
#include "Car37.h"

static const u8* bitmaps[] = 
{
	Car00::img_data, Car01::img_data, Car02::img_data, Car03::img_data, Car04::img_data, Car05::img_data, Car06::img_data, Car07::img_data, Car08::img_data, Car09::img_data,
	Car10::img_data, Car11::img_data, Car12::img_data, Car13::img_data, Car14::img_data, Car15::img_data, Car16::img_data, Car17::img_data, Car18::img_data, Car19::img_data,
	Car20::img_data, Car21::img_data, Car22::img_data, Car23::img_data, Car24::img_data, Car25::img_data, Car26::img_data, Car27::img_data, Car28::img_data, Car29::img_data,
	Car30::img_data, Car31::img_data, Car32::img_data, Car33::img_data, Car34::img_data, Car35::img_data, Car36::img_data, Car37::img_data, 
};

int main(void)
{
	consoleDebugInit(DebugDevice_NOCASH);
	
	fprintf(stderr, "Hello world!!!\n");

	videoSetMode(MODE_5_2D);
    vramSetBankA(VRAM_A_MAIN_BG_0x06000000);

	int bg3 = bgInit(3, BgType_Bmp8, BgSize_B8_256x256, 0, 0);

	u16* outbmp = bgGetGfxPtr(bg3);

	dmaFillWords(0, outbmp, 256 * 256);
	
	DC_FlushRange(Palette::palette_data, Palette::palette_size);
	dmaCopy(Palette::palette_data, BG_PALETTE, Palette::palette_size);

	u8 index = 0;

	while(pmMainLoop())
	{
		swiWaitForVBlank();

		const u8* src = bitmaps[index];
		DC_FlushRange(src, 256 * 256);
		dmaCopy(src, outbmp, 256 * 256);

		index = (index + 1) % 38;

		scanKeys();
		if (keysDown() & KEY_START)
			break;
	}
	return 0;
}
