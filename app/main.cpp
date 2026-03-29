#include <fat.h>
#include <filesystem.h>
#include <nds.h>
#include <stdio.h>

#include "engine/io/DirUtil.h"
#include "engine/scenes/__.h"
#include "game/FileUtil.h"
#include "game/Global.h"
#include "game/scns/edit/Scene.h"

int main(void)
{
    if (nitroFSInit(NULL))
    {
        game::Global::saveEnabled(fatInitDefault() && engine::io::DirUtil::create(game::FileUtil::user_Dir));
        
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
