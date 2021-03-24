import math

import numpy
import pygame
from Physics.Vector import Vector
import sympy as sp

#Force Event
from Physics.VectorField import VectorField

CREATEFORCE = pygame.USEREVENT + 1

#Force Types
NONE = 0
CONSTANTFORCE = 1
SQUARELAW = 2
CUBELAW = 3
GRAVITATIONALFORCE = 4
ELECTRICFORCE = 5
VECTORFIELD = 6
MODIFIEDGRAVITATIONALFORCE = 7
MAGNETICFORCE = 8
EARTHGRAVITY = 9
ELECTRICFIELD = 10

class Force(Vector):
    def __init__(self, force_dict):
        creator = force_dict.get("creator",None)
        reciever = force_dict.get("reciever",None)
        forceType = force_dict.get("forceType",None)
        forceVectorField = force_dict.get("forceVectorField",None)
        domain_x = force_dict.get("domain_x",None)
        domain_y = force_dict.get("domain_y",None)
        domain_r = force_dict.get("domain_r", None)
        constantForceVector = force_dict.get("constantForceVector", None)
        magneticFieldStrength = force_dict.get("magneticFieldStrength", None)
        centerVector = force_dict.get("centerVector", None)
        if(creator is not None and reciever is not None):
            self.creator = creator
            self.reciever = reciever
            try:
                temp1 = reciever.position_vector
                temp2 = creator.position_vector
                direction_vector = temp1 - temp2
                distance = direction_vector.magnitude()
                if(distance != 0):
                    direction_vector = direction_vector.normalize()
            except:
                pass
            if(forceType == None):
                force_mag  = 0
                vector = (force_mag * direction_vector)
                self.components = vector.components
            elif(forceType == CONSTANTFORCE):
                vector = constantForceVector
                self.components = vector.components
            elif(forceType == EARTHGRAVITY):
                self.components = Vector(2,[0,-9.8]).components
            elif(forceType == SQUARELAW):
                force_mag = -1000 / (math.pow(distance,2))
                vector = (force_mag * direction_vector)
                self.components = vector.components
            elif(forceType == CUBELAW):
                force_mag = 100000 / (math.pow(distance, 3))
                vector = (force_mag * direction_vector)
                self.components = vector.components
            elif (forceType == GRAVITATIONALFORCE):
                if (distance != 0):
                    m1, m2, r, G = sp.symbols('m1 m2 r G')
                    Grav_Force_Expression = G * ((m1 * m2) / (r ** 2))
                    Grav_Force = (-1) * Grav_Force_Expression.subs(m1, creator.mass).subs(m2, reciever.mass).subs(r,distance).subs(G, float(6.67408e-11)).evalf()
                    vector = (float(Grav_Force) * direction_vector)
                    self.components = vector.components
                else:
                    self.components = [0, 0]
                    print("Caution: You are applying the Electric Force with only 1 particle")
            elif(forceType == ELECTRICFORCE):
                if(distance != 0):
                    q1, q2, r, k = sp.symbols('q1 q2 r k')
                    Electric_Force_Expression = k * ((q1 * q2) / (r ** 2))
                    Electric_Force = Electric_Force_Expression.subs(q1, creator.charge).subs(q2,reciever.charge).subs(r, distance).subs(k, float(8.9875517923e9)).evalf()
                    vector = (float(Electric_Force) * direction_vector)
                    self.components = vector.components
                else:
                    self.components = [0, 0]
                    print("Caution: You are applying the Electric Force with only 1 particle")
            elif(forceType == VECTORFIELD):
                x = reciever.position_vector["x"]
                y = reciever.position_vector["y"]
                if(domain_x is not None and domain_y is not None):
                    if ((x >= domain_x[0] and x <= domain_x[1]) and (y >= domain_y[0] and y <= domain_y[1])):
                        vector = forceVectorField.solve("x=" + str(x), "y=" + str(y))
                    else:
                        vector = Vector(2,[0,0])
                elif(domain_x is not None):
                    if (x >= domain_x[0] and x <= domain_x[1]):
                        vector = forceVectorField.solve("x=" + str(x), "y=" + str(y))
                    else:
                        vector = Vector(2,[0,0])
                elif(domain_y is not None):
                    if (y >= domain_y[0] and y <= domain_y[1]):
                        vector = forceVectorField.solve("x=" + str(x), "y=" + str(y))
                    else:
                        vector = Vector(2,[0,0])
                else:
                    vector = forceVectorField.solve("x=" + str(x), "y=" + str(y))
                self.components = vector.components
            elif(forceType == MAGNETICFORCE):
                # Electron 1e-11
                # Proton -1e-7
                if(magneticFieldStrength != 0):
                    B = Vector(3, [0, 0, magneticFieldStrength])
                    new_components = reciever.velocity.components.copy()
                    new_components.append(0)
                    v = Vector(3, new_components)
                    radial_displacement_vector = centerVector - reciever.position_vector
                    d = radial_displacement_vector.mag()
                    force_direction_vector = float(numpy.sign(reciever.charge)) * radial_displacement_vector.normalize()
                    if (domain_r is not None):
                        if (d <= domain_r):
                            F = (reciever.charge * reciever.velocity.mag() * B.mag()) * force_direction_vector
                            # F = (reciever.charge * reciever.velocity.mag() * B.mag()) * v.cross(B).normalize()
                        else:
                            F = Vector(2, [0, 0])
                    else:
                        F = (reciever.charge * reciever.velocity.mag() * B.mag()) * force_direction_vector
                else:
                    F = Vector(2,[0,0])
                self.components = F.components
            elif(forceType == MODIFIEDGRAVITATIONALFORCE):
                if (distance != 0):
                    m1, m2, r, G = sp.symbols('m1 m2 r G')
                    Grav_Force_Expression = G * ((m1 * m2) / (r ** 2))
                    Grav_Force = (-1) * Grav_Force_Expression.subs(m1, creator.mass).subs(m2, reciever.mass).subs(r,distance).subs(G, float(6.67408e32)).evalf()
                    vector = (float(Grav_Force) * direction_vector)
                    self.components = vector.components
                else:
                    self.components = [0, 0]
                    print("Caution: You are applying the Gravitational Force with only 1 particle")
            elif (forceType == ELECTRICFIELD):
                x = reciever.position_vector["x"]
                y = reciever.position_vector["y"]
                if (domain_x is not None and domain_y is not None):
                    if ((x >= domain_x[0] and x <= domain_x[1]) and (y >= domain_y[0] and y <= domain_y[1])):
                        vector = forceVectorField.solve("x=" + str(x), "y=" + str(y))
                    else:
                        vector = Vector(2, [0, 0])
                elif (domain_x is not None):
                    if (x >= domain_x[0] and x <= domain_x[1]):
                        vector = forceVectorField.solve("x=" + str(x), "y=" + str(y))
                    else:
                        vector = Vector(2, [0, 0])
                elif (domain_y is not None):
                    if (y >= domain_y[0] and y <= domain_y[1]):
                        vector = forceVectorField.solve("x=" + str(x), "y=" + str(y))
                    else:
                        vector = Vector(2, [0, 0])
                else:
                    vector = forceVectorField.solve("x=" + str(x), "y=" + str(y))
                vector = reciever.charge * vector
                self.components = vector.components

        else:
            print("Error: No creator and or reciever")
            raise TypeError


