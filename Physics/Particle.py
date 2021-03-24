import pygame
from Physics.Vector import Vector
from Physics.CoordinateSystem import CoordinateSystem
from Physics.Force import Force, CREATEFORCE, NONE, CONSTANTFORCE, EARTHGRAVITY, SQUARELAW, CUBELAW, GRAVITATIONALFORCE, ELECTRICFORCE, VECTORFIELD, MODIFIEDGRAVITATIONALFORCE
from Physics.VectorField import VectorField
class Particle(pygame.sprite.Sprite):

    def __init__(self, image_filename, coordinateSystem = None, position_vector = Vector(2,[0,0]), velocity = Vector(2,[0,0]), mass = 1, charge = 0):
        if(coordinateSystem is None):
            self.coordinateSystem = CoordinateSystem([pygame.display.get_surface().get_size()[0] / 2, pygame.display.get_surface().get_size()[1] / 2], 100,"PPM", pygame.display.get_surface().get_size())
        else:
            self.coordinateSystem = coordinateSystem
        self.pathPoints = []
        self.position_vector = position_vector
        self.velocity = velocity
        self.mass = mass
        self.charge = charge
        self.netForce = Vector(2, [0, 0])
        self.acceleration = self.netForce * (1/self.mass)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_filename)
        self.center_pixel_displacement_vector = Vector(2,self.image.get_rect().topleft)  -  Vector(2, self.image.get_rect().center)

    def handleEvents(self,events, onlyParticle = False):
        for event in events:
            if event.type == CREATEFORCE:
                creator = event.creator
                if(creator is not self or onlyParticle):
                    force_event_dict = event.__dict__
                    force_event_dict["reciever"] = self
                    force = Force(force_event_dict)
                    if(len(force) > 2):
                        new_force_components = force.components
                        new_force_components.pop()
                        force = Vector(2,new_force_components)
                    self.feelForce(force)

    def update(self, delta_time):
        self.pathPoints.append(self.coordinateSystem.convertToPixelPositionVector(self.position_vector).components)
        self.move(delta_time)

    def render(self, displayVectors,displayCyclotronRadius, circleCenter, cylcotronRadius, displayParticlePath):
        if (displayCyclotronRadius):
            pygame.draw.circle(pygame.display.get_surface(), pygame.Color(0, 255, 0), circleCenter,int(cylcotronRadius * self.coordinateSystem.PPM))

        if(displayParticlePath):
            if (len(self.pathPoints) >= 2):
                pygame.draw.lines(pygame.display.get_surface(), pygame.Color(255, 0, 0), False, self.pathPoints)
                if (len(self.pathPoints) >= 1000):
                    self.pathPoints.pop(0)

        if(displayVectors):
            if (self.netForce.mag() != 0):
                normalizedNetForce = self.netForce.normalize() * 5
                normalizedNetForce.draw(self.coordinateSystem, self.position_vector)
            self.velocity.draw(self.coordinateSystem, self.position_vector, pygame.Color(0, 0, 255))
        pygame.display.get_surface().blit(self.image, (self.coordinateSystem.convertToPixelPositionVector(self.position_vector) + self.center_pixel_displacement_vector).components)

        #Reset Net Force
        self.netForce = Vector(2, [0, 0])

    def move(self, delta_time):
        self.acceleration = self.netForce * (1/self.mass)
        self.velocity = self.velocity + (self.acceleration * delta_time)
        self.position_vector = self.position_vector + (self.velocity * delta_time)


    def feelForce(self, force):
        self.netForce = self.netForce + force


