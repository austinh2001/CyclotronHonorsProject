import asyncio
from Physics.PhysicsEngine import PhysicsEngine
from UserInterface.GUIEngine import GUIEngine
async def setupTasks():
    physicsEngine = PhysicsEngine()
    guiEngine = GUIEngine(physicsEngine)
    await asyncio.wait([guiEngine.run(),physicsEngine.run()])

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setupTasks())
    loop.close()

asyncio.run(main())

