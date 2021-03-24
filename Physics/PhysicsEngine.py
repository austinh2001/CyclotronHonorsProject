import asyncio
import math

import pygame
from Engine import Engine
from Physics.CoordinateSystem import CoordinateSystem
from Physics.Electron import Electron
from Physics.Force import Force, CREATEFORCE, NONE, CONSTANTFORCE, EARTHGRAVITY, SQUARELAW, CUBELAW, GRAVITATIONALFORCE, ELECTRICFORCE, VECTORFIELD, MODIFIEDGRAVITATIONALFORCE, MAGNETICFORCE, ELECTRICFIELD
from Physics.Proton import Proton
from Physics.Particle import Particle
from Physics.Vector import Vector
import sympy as sp
from Physics.VectorField import VectorField
import random
class PhysicsEngine(Engine):
    def __init__(self):
        self.runProgram = False
        self.initialHorizontalParticleVelocity = 10
        self.horizontalParticleVelocity = 10
        self.initialVerticalParticleVelocity = 10
        self.verticalParticleVelocity = 10
        self.cyclotronRadius = 6
        self.particleType = "Proton"
        self.magneticFieldStrength = float(-1e-7)
        self.electricFieldStrength = float(1e-29)
        self.displayVectors = False
        self.displayCyclotronRadius = False
        self.displayParticlePath = True

    def initializeEngine(self):
        self.horizontalParticleVelocity = self.initialHorizontalParticleVelocity
        self.verticalParticleVelocity = self.initialVerticalParticleVelocity
        self.FPS = 120
        self.fpsClock = pygame.time.Clock()
        width = 800
        height = 600
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(pygame.Color(0, 0, 0))
        pygame.display.init()
        pygame.display.update()
        self.particles = pygame.sprite.Group()
        self.timer = 0
        self.toggleField = False
        # Scale Type: PPM
        scaleFactor = 10
        self.globalCoordinateSystem = CoordinateSystem([pygame.display.get_surface().get_size()[0] / 2, pygame.display.get_surface().get_size()[1] / 2],scaleFactor, "PPM", pygame.display.get_surface().get_size())

        if(self.particleType == "Proton"):
            particle = Proton(position_vector=Vector(2, [0, 0]),velocity=Vector(2, [self.horizontalParticleVelocity, self.verticalParticleVelocity]),coordinateSystem=self.globalCoordinateSystem)
            self.particles.add(particle)
        elif(self.particleType == "Electron"):
            particle = Electron(position_vector=Vector(2, [0, 0]),velocity=Vector(2, [self.horizontalParticleVelocity, self.verticalParticleVelocity]),coordinateSystem=self.globalCoordinateSystem)
            self.particles.add(particle)

        if (self.particleType == "Electron"):
            if(self.magneticFieldStrength != 0):
                r = (particle.mass * math.sqrt(
                    (self.initialHorizontalParticleVelocity ** 2) + (self.initialVerticalParticleVelocity ** 2))) / (
                            abs(particle.charge) * self.magneticFieldStrength)
            else:
                r = 0
            self.radial_direction_vector = particle.velocity.normalize().rotateDegrees(90) * r
        elif (self.particleType == "Proton"):
            if(self.magneticFieldStrength != 0):
                r = (particle.mass * math.sqrt(
                    (self.initialHorizontalParticleVelocity ** 2) + (self.initialVerticalParticleVelocity ** 2))) / (
                            abs(particle.charge) * self.magneticFieldStrength) * (-1)
            else:
                r = 0
            self.radial_direction_vector = particle.velocity.normalize().rotateDegrees(90) * r

        circle_center = self.globalCoordinateSystem.convertToPixelPositionVector(
            self.radial_direction_vector).components
        for i in range(len(circle_center)):
            circle_center[i] = int(circle_center[i])
        self.circle_center = circle_center
        print("Physics Engine: Initialized")

    async def run(self):
        while True:
            while self.runProgram:
                self.handleEvents()
                self.update(1 / self.FPS)
                self.render()
                await asyncio.sleep(0)
                self.fpsClock.tick(self.FPS)
            await asyncio.sleep(0)

    def handleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                break
        for particle in self.particles:
            onlyParticle = (len(self.particles) == 1)
            particle.handleEvents(events, onlyParticle)


    def update(self,delta_time):
        self.timer += delta_time
        for particle in self.particles:

            electricFieldLength = .2
            electricFieldDomainVector = Vector(2, [-electricFieldLength, electricFieldLength])
            electricFieldDomainVector = electricFieldDomainVector + Vector(2, [self.radial_direction_vector["x"],self.radial_direction_vector["x"]])

            if(self.magneticFieldStrength != 0):
                period = (math.pi * particle.mass) / (abs(particle.charge) * self.magneticFieldStrength)
                if (particle.position_vector["x"] > electricFieldDomainVector[2]):
                    self.toggleField = False
                elif(particle.position_vector["x"] < electricFieldDomainVector[1]):
                    self.toggleField = True

            if(self.toggleField):
                force_creation_event = pygame.event.Event(CREATEFORCE, creator=particle, forceType=ELECTRICFIELD,forceVectorField=VectorField("F(x,y)", [str(self.electricFieldStrength), "0"]),domain_x=electricFieldDomainVector.components)
                pygame.event.post(force_creation_event)
            else:
                force_creation_event = pygame.event.Event(CREATEFORCE, creator=particle, forceType=ELECTRICFIELD,forceVectorField=VectorField("F(x,y)", [str(-self.electricFieldStrength), "0"]),domain_x=electricFieldDomainVector.components)
                pygame.event.post(force_creation_event)

            force_creation_event = pygame.event.Event(CREATEFORCE, creator=particle, forceType=MAGNETICFORCE, domain_r=self.cyclotronRadius, magneticFieldStrength = self.magneticFieldStrength, centerVector= self.radial_direction_vector)
            pygame.event.post(force_creation_event)

            particle.update(delta_time)

            self.verticalParticleVelocity = particle.velocity["y"]
            self.horizontalParticleVelocity = particle.velocity["x"]

    def render(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        for particle in self.particles:
            particle.render(self.displayVectors,self.displayCyclotronRadius,self.circle_center,self.cyclotronRadius, self.displayParticlePath)
        pygame.draw.circle(pygame.display.get_surface(),pygame.Color(255,0,0),self.circle_center,5)
        pygame.display.update()