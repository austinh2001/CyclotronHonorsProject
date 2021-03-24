import math
import copy
import numpy as np
import pygame


class Vector:
    components = []
    def __init__(self, dimensions, element_list = None):
        if(element_list is tuple):
            element_list = list(element_list)
        try:
            if (len(element_list) == dimensions):
                valid_element_list = True
                for e in element_list:
                    if (type(e) != int and type(e) != float):
                        valid_element_list = False
                if (valid_element_list):
                    self.components = element_list
                else:
                    raise TypeError
            else:
                raise IndexError
        except:
            if (element_list == None):
                element_list = []
                for i in range(dimensions):
                    element_list.append(0)
                valid_element_list = True
                for e in element_list:
                    if (type(e) != int and type(e) != float):
                        valid_element_list = False
                if (valid_element_list):
                    self.components = element_list
                else:
                    raise TypeError
            elif(type(element_list) == list and dimensions > len(element_list)):
                for i in range(dimensions - len(element_list)):
                    element_list.append(0)
                valid_element_list = True
                for e in element_list:
                    if (type(e) != int and type(e) != float):
                        valid_element_list = False
                if (valid_element_list):
                    self.components = element_list
                else:
                    raise TypeError
            else:
                print("Error: More vector components than dimensions")
                raise TypeError

    def __getitem__(self, dimension):
        try:
            if (type(dimension) == int):
                if(dimension-1 < 0):
                    raise ValueError
                return self.components[dimension - 1]
            elif (dimension == "x"):
                return self.components[0]
            elif (dimension == "y"):
                return self.components[1]
            elif (dimension == "z"):
                return self.components[2]
            elif (dimension == "w"):
                return self.components[3]
            elif (dimension == "t"):
                return self.components[3]
            else:
                raise ValueError
        except:
            print("Error: Invalid Index")
            raise ValueError

    def __setitem__(self, dimension, value):
        try:
            if (type(dimension) == int):
                if (dimension - 1 < 0):
                    raise ValueError
                self.components[dimension-1] = value
            elif (dimension == "x"):
                self.components[0] = value
            elif (dimension == "y"):
                self.components[1] = value
            elif (dimension == "z"):
                self.components[2] = value
            elif (dimension == "w"):
                self.components[3] = value
            elif (dimension == "t"):
                self.components[3] = value
            else:
                raise ValueError
        except:
            print("Error: Invalid Index")
            raise ValueError

    def __add__(self, other):
        try:
            self_copy = copy.copy(self)
            if (isinstance(other,Vector) and isinstance(self,Vector)):
                for i in range(1,len(self.components)+1):
                    self_copy[i] += other[i]
                return self_copy
            else:
                raise TypeError
        except:
            print("Error: Invalid Type")

    def __radd__(self, other):
        try:
            self_copy = copy.copy(self)
            if (isinstance(other,Vector) and isinstance(self,Vector)):
                for i in range(1,len(self.components)+1):
                    self_copy[i] += other[i]
                return self_copy
            else:
                raise TypeError
        except:
            print("Error: Invalid Type")

    def __sub__(self, other):
        try:
            self_copy = copy.copy(self)
            if (isinstance(other, Vector) and isinstance(self, Vector)):
                for i in range(1,len(self.components)+1):
                    self_copy[i] -= other[i]
                return self_copy
            else:
                raise TypeError
        except TypeError:
            print("Error: Invalid Type")

    def __mul__(self, other):
        try:
            self_copy = copy.copy(self)
            if (type(other) is int or type(other) is float):
                for i in range(1,len(self.components)+1):
                    self_copy[i] *= other
                return self_copy
            else:
                raise TypeError
        except TypeError:
            print("Error: Invalid Type")

    def __truediv__(self, other):
        self_copy = copy.copy(self)
        self_copy * (1/other)
        return self_copy


    def __rmul__(self, other):
        try:
            self_copy = copy.copy(self)
            if (type(other) is int or type(other) is float or type(other)):
                for i in range(1,len(self.components)+1):
                    self_copy[i] *= other
                return self_copy
            else:
                raise TypeError
        except TypeError:
            print("INVALID?" + str(other))
            print("Error: Invalid Type")

    def dot(self, other):
        sum = 0
        if (type(other) is type(self)):
            if (len(other) == len(self)):
                for i in range(1,len(self)+1):
                    sum += self[i] * other[i]
                return sum
            else:
                raise IndexError
        else:
            raise TypeError

    def cross(self, other):
        if (type(other) is type(self)):
            if (len(self) == 3 and len(other) == 3):
                first_array = np.array(self.components)
                second_array = np.array(other.components)
                result = np.cross(first_array,second_array)
                new_results = []
                for i in range(len(result)):
                    r = str(result[i])
                    new_results.append(float(r))
                result_vector = Vector(len(self),new_results)
                return result_vector
            else:
                print("Error: Invalid Vector Size")
                raise IndexError
        else:
            raise TypeError

    def __len__(self):
        return len(self.components)

    def mag(self):
        radicand = 0
        for i in range(1, len(self) + 1):
            radicand += math.pow(self[i],2)
        magnitude = math.sqrt(radicand)
        return magnitude

    def magnitude(self):
        radicand = 0
        for i in range(1, len(self) + 1):
            radicand += math.pow(self[i],2)
        magnitude = math.sqrt(radicand)
        return magnitude

    def __copy__(self):
        return Vector(len(self.components), list(self.components).copy())

    def unit(self):
        if(self.mag() != 0):
            self_copy = copy.copy(self)
            return self_copy * (1 / self.mag())
        else:
            print("Cannot normalize, as magnitude is 0.")


    def normalize(self):
        if (self.mag() != 0):
            self_copy = copy.copy(self)
            return self_copy * (1 / self.mag())
        else:
            print("Cannot normalize, as magnitude is 0.")

    def rotateDegrees(self, angle_degrees):
        self_copy = copy.copy(self)
        if(len(self.components) == 2):
            angle_radians = angle_degrees * (math.pi / 180)
            new_components = [self.components[0] * math.cos(angle_radians) - self.components[1] * math.sin(angle_radians), self.components[0] * math.sin(angle_radians) +  self.components[1] * math.cos(angle_radians)]
            self_copy.components = new_components
            return self_copy
        else:
            raise ValueError

    def rotateRadians(self, angle_radians):
        self_copy = copy.copy(self)
        if(len(self.components) == 2):
            new_components = [self.components[0] * math.cos(angle_radians) - self.components[1] * math.sin(angle_radians), self.components[0] * math.sin(angle_radians) +  self.components[1] * math.cos(angle_radians)]
            self_copy.components = new_components
            return self_copy
        else:
            raise ValueError

    def reflect(self,dimension):
        self_copy = copy.copy(self)
        new_components = []
        count = 1
        for component in self.components:
            if(count == dimension):
                new_components.append(component)
            else:
                new_components.append(-1 * component)
            count += 1
        self_copy.components = new_components
        return self_copy

    def __abs__(self):
        self_copy = copy.copy(self)
        new_components = []
        for component in self.components:
            new_components.append(abs(component))
        self_copy.components = new_components
        return self_copy

    def __str__(self):
        return str(self.components)

    def __round__(self, n=None):
        for i in range(len(self.components)):
            self.components[i] = round(self.components[i], n)
        return self

    def print(self):
        print(self)

    def draw(self,coordinateSystem, initialPositionVector,color = pygame.Color(255,0,0)):
        pygame.draw.line(pygame.display.get_surface(),color,coordinateSystem.convertToPixelPositionVector(initialPositionVector).components, coordinateSystem.convertToPixelPositionVector((self + initialPositionVector)).components)