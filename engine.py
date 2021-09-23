import math
from kandinsky import * 
from time import *


width,height = 320,240
aspectRatio = height/width
fov = 90
fovRad = 1 / math.tanh(fov * 0.5 / 180 * math.pi);
near = 0.1
far = 1000
f = 1/math.tan(fov/2)
q = far/(far-near)

points = []


black = color(0,0,0)
white = color(255,255,255)


def drawLine(x1,y1,x2,y2):
    x,y,xe,ye = 0,0,0,0

    dx = x2-x1
    dy = y2-y1
    dx2 = abs(dx)
    dy2 = abs(dy)

    px = 2 * dy2 - dx2
    py = 2 * dx2 - dy2

    if dy2 <= dx2:
        if dx >= 0:
            x = x1;y = y1;xe = x2
        else:
            x = x2;y = y2;xe = x1
        point(x,y)

        while x<xe:
            x = x + 1
            if(px < 0):
                px = px + 2 * dy2
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    y = y + 1
                else:
                    y = y - 1
                px = px + 2 * (dy2 - dx2) 
            point(x,y)
    else:
        if dy >= 0:
            x=x1;y=y1;ye=y2
        else:
            x=x2;y=y2;ye=y1
        point(x,y)

        while y<ye:
            y = y + 1
            if(py <= 0):
                py = py + 2 * dx2
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    x = x + 1
                else:
                    x = x - 1
                py = py + 2 * (dx2 - dy2)
            point(x,y)

def drawTriangle(x1,y1,x2,y2,x3,y3):
    drawLine(x1,y1,x2,y2)
    drawLine(x2,y2,x3,y3)
    drawLine(x1,y1,x3,y3)

def point(x,y):
    set_pixel(x,y,black)
    #if not x in points:
    #    points.append(x)
    
    #points.append([x,y])

def fill(color):
    for x in range(width):
        for y in range(height):
            set_pixel(x,y,color)

#def clear():
#    points.sort()
#    for x in points:
#        for y in range(height):
#            set_pixel(x,y,white)
def clear():
  fill_rect(0,0, width,height,white)

class Vec3D:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class Triangle:
    def __init__(self):
        self.p = []

class Mesh:
    def __init__(self):
        self.tris = []
    def setTris(self,arr):
        for tri in arr:
            otri = Triangle()
            for p in tri:
                vec = Vec3D()
                vec.x = p[0]
                vec.y = p[1]
                vec.z = p[2]
                otri.p.append(vec)
            self.tris.append(otri)

class Mat4x4:
    def __init__(self):
        self.m = [[0 for _ in range(4)] for _ in range(4)]

    def multiplyMatrixVector(self,i):
        o = Vec3D()
        m = self
        o.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + m.m[3][0]
        o.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + m.m[3][1]
        o.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + m.m[3][2]

        w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + m.m[3][3]
        if (w != 0):
            o.x /= w
            o.y /= w
            o.z /= w
        return o

meshCube = Mesh()
meshCube.setTris([
    #SOUTH
    [[0,0,0],  [0,1,0],  [1,0,0]],
    [[0,1,0],  [1,1,0],  [1,0,0]],
    
    #EAST
    [[1,0,0],  [1,1,0],  [1,0,1]],
    [[1,1,0],  [1,1,1],  [1,0,1]],
    
    #NORTH
    [[1,0,1],  [1,1,1],  [0,0,1]],
    [[1,1,1],  [0,1,1],  [0,0,1]],
    
    #WEST
    [[0,0,1],  [0,1,1],  [0,0,0]],
    [[0,1,1],  [0,1,0],  [0,0,0]],
    
    #TOP
    [[0,1,0],  [0,1,1],  [1,1,0]],
    [[0,1,1],  [1,1,1],  [1,1,0]],

    #BOTTOM
    [[0,0,0],  [0,0,1],  [1,0,0]],
    [[0,0,1],  [1,0,1],  [1,0,0]],
])



matProj = Mat4x4()
matProj.m[0][0] = aspectRatio * fovRad
matProj.m[1][1] = fovRad
matProj.m[2][2] = far / (far-near)
matProj.m[3][2] = (-far * near) / (far-near)
matProj.m[2][3] = 1
matProj.m[3][3] = 0

theta =0
fill(white)
while True:
    clear()
    theta += 0.4
    matRotX = Mat4x4()
    matRotZ = Mat4x4()

    matRotX.m[0][0] = 1;
    matRotX.m[1][1] = math.cos(theta * 0.5);
    matRotX.m[1][2] = math.sin(theta * 0.5);
    matRotX.m[2][1] = -math.sin(theta * 0.5);
    matRotX.m[2][2] = math.cos(theta * 0.5);
    matRotX.m[3][3] = 1;

    matRotZ.m[0][0] = math.cos(theta);
    matRotZ.m[0][1] = math.sin(theta);
    matRotZ.m[1][0] = -math.sin(theta);
    matRotZ.m[1][1] = math.cos(theta);
    matRotZ.m[2][2] = 1;
    matRotZ.m[3][3] = 1;

    for tri in meshCube.tris:
        triRotated = Triangle()
        triPojected = Triangle()

        triRotated.p.append(matRotX.multiplyMatrixVector(matRotZ.multiplyMatrixVector(tri.p[0])))
        triRotated.p.append(matRotX.multiplyMatrixVector(matRotZ.multiplyMatrixVector(tri.p[1])))
        triRotated.p.append(matRotX.multiplyMatrixVector(matRotZ.multiplyMatrixVector(tri.p[2])))

        triRotated.p[0].z += 3
        triRotated.p[1].z += 3
        triRotated.p[2].z += 3

        triPojected.p.append(matProj.multiplyMatrixVector(triRotated.p[0]))
        triPojected.p.append(matProj.multiplyMatrixVector(triRotated.p[1]))
        triPojected.p.append(matProj.multiplyMatrixVector(triRotated.p[2]))

        triRotated = None

        triPojected.p[0].x += 1; triPojected.p[0].y += 1
        triPojected.p[1].x += 1; triPojected.p[1].y += 1
        triPojected.p[2].x += 1; triPojected.p[2].y += 1

        triPojected.p[0].x *= 0.5 * width; triPojected.p[0].y *= 0.5 * height
        triPojected.p[1].x *= 0.5 * width; triPojected.p[1].y *= 0.5 * height
        triPojected.p[2].x *= 0.5 * width; triPojected.p[2].y *= 0.5 * height

        drawTriangle(int(triPojected.p[0].x),int(triPojected.p[0].y),int(triPojected.p[1].x),int(triPojected.p[1].y),int(triPojected.p[2].x),int(triPojected.p[2].y))
    #sleep(0.2)
