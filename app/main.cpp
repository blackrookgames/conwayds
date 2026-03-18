#include <filesystem.h>
#include <nds.h>
#include <stdio.h>

#include "engine/scenes/__.h"
#include "game/Global.h"
#include "game/scns/edit/Scene.h"

int main(void)
{
    if (nitroFSInit(NULL))
    {
        engine::scenes::initialize();

        std::fill(game::Global::pattern()->cells(), game::Global::pattern()->cells() + PATTERN_AREA, 0);

        game::scns::edit::Scene* scene = new game::scns::edit::Scene();
        scene->deleteOnExit(true);
        engine::scenes::gotoScene(scene);

        while(pmMainLoop())
        {
            engine::scenes::update();
        }

        engine::scenes::finalize();
    }
    else
    {
        nocashMessage("Fail to initialize nitro\n");
    }
}
