import math
import time
import sys
import os
import numpy as np



class Cube:
    def __init__(self):
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0

        self.cubeWidth = 20
        self.width = 80
        self.height = 44

        self.zBuffer = [0] * (self.width * self.height) # i.e depth map
        self.buffer = [' '] * (self.width * self.height) 

        self.backgroundChar = ' '
        self.distanceFromCam = 100
        self.K1 = 100.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.ooz = 0.0
        self.xp = 0
        self.yp = 0
        self.idx = 0
    
    # clear buffers at start of frame
    def clear_buffers(self, backgroundChar):
        self.buffer[:] = [backgroundChar] * (self.width * self.height)
        self.zBuffer[:] = [0] * (self.width * self.height)
        
    # rotation axis calcs
    def calcX(i, j, k, sinA, cosA, sinB, cosB, sinC, cosC):
        return j * sinA * sinB * cosC - k * cosA * sinB * cosC + j * cosA * sinC + k * sinA * sinC + i * cosB * cosC

    def calcY(i, j, k, sinA, cosA, sinB, cosB, sinC, cosC):
        return j * cosA * cosC + k * sinA * cosC - j * sinA * sinB * sinC + k * cosA * sinB * sinC - i * cosB * sinC
    
    def calcZ(i, j, k, sinA, cosA, sinB, cosB):
        return k * cosA * cosB - j * sinA * cosB + i * sinB
    

    def calculate_point(self, i, j, k, ch):

        sinA, cosA = math.sin(self.A), math.cos(self.A)
        sinB, cosB = math.sin(self.B), math.cos(self.B)
        sinC, cosC = math.sin(self.C), math.cos(self.C)

        # axis rotation
        self.x = Cube.calcX(i, j, k, sinA, cosA, sinB, cosB, sinC, cosC)
        self.y = Cube.calcY(i, j, k, sinA, cosA, sinB, cosB, sinC, cosC)
        self.z = Cube.calcZ(i, j, k, sinA, cosA, sinB, cosB) + self.distanceFromCam

        self.ooz = 1 / self.z

        self.xp = int(self.width / 2 + self.K1 * self.ooz * self.x * 2)
        self.yp = int(self.height / 2 - self.K1 * self.ooz * self.y)
        self.idx = self.xp + self.yp * self.width
        if 0 <= self.idx and self.idx < self.width * self.height:

            if self.ooz > self.zBuffer[self.idx]:
                self.zBuffer[self.idx] = self.ooz
                self.buffer[self.idx] = ch
        
    def render(self):

        Cube.clear_buffers(self, self.backgroundChar) # always at the start of the loop

        
        i = -self.cubeWidth / 2

        while i < self.cubeWidth / 2:
            j = -self.cubeWidth / 2
            while j < self.cubeWidth / 2:
                
                # sides
                Cube.calculate_point(self, i, j, -self.cubeWidth/2, '.')
                Cube.calculate_point(self, self.cubeWidth/2, j, i, ',')
                Cube.calculate_point(self, -self.cubeWidth/2, j, -i, '-')
                Cube.calculate_point(self, -i, j, self.cubeWidth/2, '~')
                Cube.calculate_point(self, i, -self.cubeWidth/2, -j, '^')
                Cube.calculate_point(self, i, self.cubeWidth/2, j, '™')


                j += 0.15
            i += 0.15

        # print the buffer
        sys.stdout.write("\x1b[H")
        for k in range(self.height):
            start = k * self.width
            end = start + self.width
            sys.stdout.write(''.join(self.buffer[start:end]) + '\n')

        sys.stdout.flush()

        self.A += 0.03
        self.B += 0.05
        self.C += 0.09
        time.sleep(0.001)

class Main:
    def __init__(self):
        self.cube = Cube()

    def run(self):
        sys.stdout.write('\x1b[2J')
        
        while True:
            self.cube.render()

if __name__ == "__main__":
    app = Main()
    app.run()




