import pygame
from Physics.Particle import Particle
from Physics.Vector import Vector
from Physics.CoordinateSystem import CoordinateSystem
from Physics.Force import Force, CREATEFORCE, NONE, CONSTANTFORCE, EARTHGRAVITY, SQUARELAW, CUBELAW, GRAVITATIONALFORCE, ELECTRICFORCE

class Electron(Particle):
    def __init__(self, coordinateSystem = None, position_vector = Vector(2,[0,0]), velocity = Vector(2,[0,0])):
        if(coordinateSystem is None):
            self.coordinateSystem = CoordinateSystem([pygame.display.get_surface().get_size()[0] / 2, pygame.display.get_surface().get_size()[1] / 2], 100,"PPM", pygame.display.get_surface().get_size())
        else:
            self.coordinateSystem = coordinateSystem
        self.timer = 0
        self.pathPoints = []
        self.position_vector = position_vector
        self.velocity = velocity
        self.mass = float(9.1093837015e-31)
        self.charge = (-1) * float(1.60217662e-19)
        self.netForce = Vector(2, [0, 0])
        self.acceleration = self.netForce * (1/self.mass)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Electron.png")
        self.center_pixel_displacement_vector = Vector(2,self.image.get_rect().topleft)  -  Vector(2, self.image.get_rect().center)