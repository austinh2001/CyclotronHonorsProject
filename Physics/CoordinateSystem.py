#Imports
import pygame
from Physics.Vector import Vector

class CoordinateSystem:
    def __init__(self,pixel_origin, conversionFactor, conversionType, pixel_screen_size = [800,600]):
        #Origin of the coordinate system (in pixels), in terms of the location on the window you are using.
        self.pixel_origin = pixel_origin
        
        #The type of conversion that your coordinate system is utilizing
        #By default, there exists two types of conversion types:
        #PPM (Pixels Per Meter)
        #MPP (Meters Per Pixel)
        self.conversionType = conversionType
        self.PPM = None
        self.MPP = None
        if(conversionType == "PPM"):
            self.PPM = conversionFactor
        elif(conversionType == "MPP"):
            self.MPP = conversionFactor
        else:
            raise Exception
        
        #The dimensions of the screen/window you are using (in pixels)
        self.pixel_screen_size = pixel_screen_size
        self.pixel_width = self.pixel_screen_size[0]
        self.pixel_height = self.pixel_screen_size[1]
        
        #The dimensions of the screen/window you are using (in meters)
        self.converted_screen_size = []
        if (self.conversionType == "PPM"):
            self.converted_screen_size.append(self.pixel_width / self.PPM)
            self.converted_screen_size.append(self.pixel_height / self.PPM)
        elif(self.conversionType == "MPP"):
            self.converted_screen_size.append(self.pixel_width * self.MPP)
            self.converted_screen_size.append(self.pixel_height * self.MPP)
    
    #Takes a vector object (which contains pixel information) and converts it accordingly to a meter-based position vector
    def convertFromPixelVector(self,pixel_vector):
        if (self.conversionType == "PPM"):
            vector = (pixel_vector * (1 / self.PPM))
        elif(self.conversionType == "MPP"):
            vector = pixel_vector * self.MPP
        vector = vector.rotateDegrees(90)
        return vector
    
    #Takes a vector object (which contains meter information) and converts it accordingly to a pixel-based position vector
    def convertToPixelPositionVector(self,vector):
        if (self.conversionType == "PPM"):
            pixel_vector = (vector * self.PPM)
            pixel_vector = pixel_vector.reflect(1)
            pixel_vector = pixel_vector + Vector(2,self.pixel_origin)
        elif(self.conversionType == "MPP"):
            pixel_vector = (vector * (1 / self.MPP))
            pixel_vector = pixel_vector.reflect(1)
            pixel_vector = pixel_vector + Vector(2, self.pixel_origin)
        return pixel_vector


