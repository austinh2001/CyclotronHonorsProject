import asyncio
import math
import os
import sys

import pygame

from Engine import Engine
from UserInterface import Interface

class GUIEngine(Engine):
    interface = None

    def __init__(self, physicsEngine):
        self.physicsEngine = physicsEngine
        print("GUIEngine: Initialized")
        self.interface = Interface.Interface(self.physicsEngine)
        graph = self.interface.window['-GRAPH-']
        embed = graph.TKCanvas
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

    async def run(self):
        while True:
            await self.handleEvents()
            self.update()
            self.render()
            await asyncio.sleep(0)

    async def handleEvents(self):
        event, values = self.interface.window.read(timeout=1)
        if event in (None, "Exit"):
            sys.exit()
        elif event in "Start":
            self.physicsEngine.initialVerticalParticleVelocity = float(values["VerticalVelocity"])
            self.physicsEngine.initialHorizontalParticleVelocity = float(values["HorizontalVelocity"])
            self.physicsEngine.particleType = values["ParticleSelector"][0]
            self.physicsEngine.magneticFieldStrength = float(values["MagneticFieldStrength"])
            self.physicsEngine.electricFieldStrength = float(values["ElectricFieldStrength"])
            self.physicsEngine.cyclotronRadius = float(values["CyclotronRadius"])
            self.physicsEngine.displayVectors = bool(values["DisplayVectors"])
            self.physicsEngine.displayCyclotronRadius = bool(values["DisplayCyclotronRadius"])
            self.physicsEngine.displayParticlePath = bool(values["DisplayParticlePath"])
            self.physicsEngine.initializeEngine()
            self.physicsEngine.runProgram = True
        elif event in "ParticleSelector":
            if (values["ParticleSelector"][0] == "Proton"):
                self.interface.window["MagneticFieldStrength"].update("-1e-7")
                self.interface.window["ElectricFieldStrength"].update("1e-5")
            elif (values["ParticleSelector"][0] == "Electron"):
                self.interface.window["MagneticFieldStrength"].update("1e-10")
                self.interface.window["ElectricFieldStrength"].update("-1e-8")



    def update(self):
        self.interface.background_tasks()

    def render(self):
        pass