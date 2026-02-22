#include <nds.h>
#include <stdio.h>

#include "engine/scenes/__.h"
#include "game/scns/sim/Scene.h"

int main(void)
{
    nocashMessage("Hello world!!!\n");

    engine::scenes::initialize();

    game::scns::sim::Scene* scene = new game::scns::sim::Scene();
    scene->deleteOnExit(true);
    engine::scenes::gotoScene(scene);

	while(pmMainLoop())
	{
		swiWaitForVBlank();
        
        engine::scenes::update();
    }

    engine::scenes::finalize();
}
