import asyncio
import math

import PySimpleGUI as sg

class Interface():
    window = None
    def __init__(self, physicsEngine):
        self.physicsEngine = physicsEngine
        print("User Interface: Loaded")

        sg.change_look_and_feel("DarkAmber")

        self.window = sg.Window("Particle Accelerator", self.createLayout())
        self.window.finalize()

    def createLayout(self):
        layout = [[sg.Graph((800, 600), (0, 0), (800, 600), background_color='lightblue', key='-GRAPH-')],
                  [sg.Text("Current Velocity: " + str(round(math.sqrt((self.physicsEngine.horizontalParticleVelocity**2)+(self.physicsEngine.verticalParticleVelocity**2)),2)) + " m/s", key="CurrentVelocityText")],
                  [sg.Button("Start"), sg.Button("Exit"), sg.Checkbox("Display Vectors", key="DisplayVectors", default=False),sg.Checkbox("Display Cyclotron Radius", key="DisplayCyclotronRadius", default=False),sg.Checkbox("Display Particle Path", key="DisplayParticlePath", default=True)],
                  [sg.Text("Initial Vertical Velocity (m/s)"),sg.Input(size=(10, 1),key="VerticalVelocity",default_text="10"),sg.Text("Magnetic Flux Density (T)"),sg.Input(size=(10, 1),key="MagneticFieldStrength",default_text="-1e-7"),sg.Text("Cyclotron Radius (m)"),sg.Input(size=(10, 1),key="CyclotronRadius",default_text="6")],
                  [sg.Text("Initial Horizontal Velocity (m/s)"),sg.Input(size=(10, 1),key="HorizontalVelocity",default_text="10"),sg.Text("Electric Field (N/C)"),sg.Input(size=(10, 1),key="ElectricFieldStrength",default_text="1e-5")],
                  [sg.Listbox(values=['Proton', 'Electron'], size=(10, 3),key="ParticleSelector",default_values="Proton",auto_size_text=True, enable_events=True)]]

        return layout

    def background_tasks(self):
        if(self.physicsEngine.runProgram):
            self.window["CurrentVelocityText"].update("Current Velocity: " + str(round(math.sqrt((self.physicsEngine.horizontalParticleVelocity**2)+(self.physicsEngine.verticalParticleVelocity**2)),2)) + " m/s")
        else:
            self.window["CurrentVelocityText"].update("Current Velocity: " + str(round(math.sqrt((self.physicsEngine.horizontalParticleVelocity**2)+(self.physicsEngine.verticalParticleVelocity**2)),2)) + " m/s")