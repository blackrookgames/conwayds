#include <nds.h>
#include <stdio.h>

#include "engine/scenes/__.h"
#include "entity/TestScene.h"

int main(void)
{
    consoleDebugInit(DebugDevice_NOCASH);

    fprintf(stderr, "Hello world!!!\n");

    engine::scenes::initialize();

    entity::TestScene* scene = new entity::TestScene();
    scene->deleteOnExit(true);
    engine::scenes::gotoScene(scene);

	while(pmMainLoop())
	{
		swiWaitForVBlank();
        
        engine::scenes::update();
    }

    engine::scenes::finalize();
}
