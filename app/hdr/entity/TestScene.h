#include "engine/scenes/Scene.h"

#ifndef ENTITY_TESTSCENE_H
#define ENTITY_TESTSCENE_H

namespace entity
{
    class TestScene : public engine::scenes::Scene
    {
        #pragma region init

        public: 

        /// @brief
        /// Constructor for TestScene
        TestScene();

        /// @brief
        /// Destructor for TestScene
        virtual ~TestScene() override;

        INIT_NOCOPYMOVE(TestScene)

        #pragma endregion

        #pragma region helper functions

        protected:

        void m_enter() override;

        void m_exit() override;

        void m_update() override;

        #pragma endregion
    };
}

#endif