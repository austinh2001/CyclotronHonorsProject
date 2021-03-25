#Imports
import asyncio
from Physics.PhysicsEngine import PhysicsEngine
from UserInterface.GUIEngine import GUIEngine

#Asynchronously puts the run functions of each engine into the main event loop
async def setupTasks():
    physicsEngine = PhysicsEngine()
    guiEngine = GUIEngine(physicsEngine)
    await asyncio.wait([guiEngine.run(),physicsEngine.run()])

#Main Function
#Gets the main event loop, asks for it to run until complete (which is forever), and to close the event loop if it were to complete
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setupTasks())
    loop.close()
    
#Asynchronously runs the Main Function
asyncio.run(main())

