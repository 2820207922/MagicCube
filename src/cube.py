
import math
from constants import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Cube:

    def __init__(self, id: str, center=(0, 0, 0), r=1, h=10, colors=[BLEAK, BLEAK, BLEAK, BLEAK, BLEAK, BLEAK]):

        self.ID = int(id, 2)

        self.center = [center[0], center[1], center[2]]

        self.cube = self.buildCube(center, r, h)

        self.covers = self.buildSquare(center, r, h)

        self.colors = colors

        self.notation_to_color = {"F": WHITE, "U": RED,
                                  "R": GREEN, "D": ORANGE, "L": BLUE, "B": YELLOW}

    # Set palette color
    def setPaletteColor(self, side, color):
        self.colors[side] = self.notation_to_color[color]

    # Rotate around the x-axis

    def rotatePointX(self, point, th=3):

        th_origin = math.atan2(point[2], point[1])
        th_target = th_origin + th * PI/180
        r = math.sqrt(math.pow(point[1], 2) + math.pow(point[2], 2))
        output = [0, 0, 0]
        output[0] = point[0]
        output[1] = r * math.cos(th_target)
        output[2] = r * math.sin(th_target)

        return output

    # Rotate around the y-axis

    def rotatePointY(self, point, th=3):

        th_origin = math.atan2(point[0], point[2])
        th_target = th_origin + th * PI/180
        r = math.sqrt(math.pow(point[0], 2) + math.pow(point[2], 2))
        output = [0, 0, 0]
        output[0] = r * math.sin(th_target)
        output[1] = point[1]
        output[2] = r * math.cos(th_target)

        return output

    # Rotate around the z-axis

    def rotatePointZ(self, point, th=3):

        th_origin = math.atan2(point[1], point[0])
        th_target = th_origin + th * PI/180
        r = math.sqrt(math.pow(point[0], 2) + math.pow(point[1], 2))
        output = [0, 0, 0]
        output[0] = r * math.cos(th_target)
        output[1] = r * math.sin(th_target)
        output[2] = point[2]

        return output

    def drawSurface(self, points, color):
        # Set surface color
        glColor3fv(color)

        glBegin(GL_POLYGON)
        for point in points:
            glVertex3fv(point)
        glEnd()

    def rotateCubeX(self, th=3):
        self.center = self.rotatePointX(self.center, th)

        for i in range(16):
            for j in range(8):
                self.cube[i][j] = self.rotatePointX(self.cube[i][j], th)

        for i in range(12):
            for j in range(4):
                self.covers[i][j] = self.rotatePointX(self.covers[i][j], th)

    def rotateCubeY(self, th=3):
        self.center = self.rotatePointY(self.center, th)

        for i in range(16):
            for j in range(8):
                self.cube[i][j] = self.rotatePointY(self.cube[i][j], th)

        for i in range(12):
            for j in range(4):
                self.covers[i][j] = self.rotatePointY(self.covers[i][j], th)

    def rotateCubeZ(self, th=3):
        self.center = self.rotatePointZ(self.center, th)

        for i in range(16):
            for j in range(8):
                self.cube[i][j] = self.rotatePointZ(self.cube[i][j], th)

        for i in range(12):
            for j in range(4):
                self.covers[i][j] = self.rotatePointZ(self.covers[i][j], th)

    # Draw cube (Optimize)

    def drawCube(self):
        for i in range(16):
            for j in range(7):
                points_in = [self.cube[i][j], self.cube[i][j + 1],
                             self.cube[(i + 1) % 16][j + 1], self.cube[(i + 1) % 16][j]]
                self.drawSurface(points_in, BLEAK)

        for i in range(6):
            self.drawCover(self.covers[i * 2], BLEAK)
            self.drawCover(self.covers[i * 2 + 1], self.colors[i])

    # Draw surface

    def drawCover(self, points, color):
        self.drawSurface(points, color)

    # Draw points on surface

    def buildCube(self, center=(0, 0, 0), r=1, h=1) -> list:
        points = [[[0 for k in range(3)] for j in range(8)]
                  for i in range(16)]

        for i in range(16):
            for j in range(8):
                th1 = j * PI / 8
                th2 = i * PI / 8
                points[i][j][0] = center[0] + r * math.sin(th1) * math.sin(th2)
                if (points[i][j][0] >= center[0]):
                    points[i][j][0] += h/2
                else:
                    points[i][j][0] -= h/2

                points[i][j][1] = center[1] + r * math.cos(th1)
                if (points[i][j][1] >= center[1]):
                    points[i][j][1] += h/2
                else:
                    points[i][j][1] -= h/2

                points[i][j][2] = center[2] + r * math.sin(th1) * math.cos(th2)
                if (points[i][j][2] >= center[2]):
                    points[i][j][2] += h/2
                else:
                    points[i][j][2] -= h/2

        return points

    # Create points on surface

    def buildSquare(self, center=(0, 0, 0), r=1, h=1) -> list:
        points = [[[0 for k in range(3)] for j in range(4)] for i in range(12)]

        points[0][0] = [center[0] - h/2, center[1] + h/2, center[2] + h/2 + r]
        points[0][1] = [center[0] + h/2, center[1] + h/2, center[2] + h/2 + r]
        points[0][2] = [center[0] + h/2, center[1] - h/2, center[2] + h/2 + r]
        points[0][3] = [center[0] - h/2, center[1] - h/2, center[2] + h/2 + r]
        points[1][0] = [center[0] - h/2 + 0.1, center[1] +
                        h/2 - 0.1, center[2] + h/2 + r + 0.01]
        points[1][1] = [center[0] + h/2 - 0.1, center[1] +
                        h/2 - 0.1, center[2] + h/2 + r + 0.01]
        points[1][2] = [center[0] + h/2 - 0.1, center[1] -
                        h/2 + 0.1, center[2] + h/2 + r + 0.01]
        points[1][3] = [center[0] - h/2 + 0.1, center[1] -
                        h/2 + 0.1, center[2] + h/2 + r + 0.01]

        points[10][0] = [center[0] - h/2, center[1] + h/2, center[2] - h/2 - r]
        points[10][1] = [center[0] + h/2, center[1] + h/2, center[2] - h/2 - r]
        points[10][2] = [center[0] + h/2, center[1] - h/2, center[2] - h/2 - r]
        points[10][3] = [center[0] - h/2, center[1] - h/2, center[2] - h/2 - r]
        points[11][0] = [center[0] - h/2 + 0.1, center[1] +
                         h/2 - 0.1, center[2] - h/2 - r - 0.01]
        points[11][1] = [center[0] + h/2 - 0.1, center[1] +
                         h/2 - 0.1, center[2] - h/2 - r - 0.01]
        points[11][2] = [center[0] + h/2 - 0.1, center[1] -
                         h/2 + 0.1, center[2] - h/2 - r - 0.01]
        points[11][3] = [center[0] - h/2 + 0.1, center[1] -
                         h/2 + 0.1, center[2] - h/2 - r - 0.01]

        points[2][0] = [center[0] - h/2, center[1] + h/2 + r, center[2] + h/2]
        points[2][1] = [center[0] + h/2, center[1] + h/2 + r, center[2] + h/2]
        points[2][2] = [center[0] + h/2, center[1] + h/2 + r, center[2] - h/2]
        points[2][3] = [center[0] - h/2, center[1] + h/2 + r, center[2] - h/2]
        points[3][0] = [center[0] - h/2 + 0.1, center[1] +
                        h/2 + r + 0.01, center[2] + h/2 - 0.1]
        points[3][1] = [center[0] + h/2 - 0.1, center[1] +
                        h/2 + r + 0.01, center[2] + h/2 - 0.1]
        points[3][2] = [center[0] + h/2 - 0.1, center[1] +
                        h/2 + r + 0.01, center[2] - h/2 + 0.1]
        points[3][3] = [center[0] - h/2 + 0.1, center[1] +
                        h/2 + r + 0.01, center[2] - h/2 + 0.1]

        points[6][0] = [center[0] - h/2, center[1] - h/2 - r, center[2] + h/2]
        points[6][1] = [center[0] + h/2, center[1] - h/2 - r, center[2] + h/2]
        points[6][2] = [center[0] + h/2, center[1] - h/2 - r, center[2] - h/2]
        points[6][3] = [center[0] - h/2, center[1] - h/2 - r, center[2] - h/2]
        points[7][0] = [center[0] - h/2 + 0.1, center[1] -
                        h/2 - r - 0.01, center[2] + h/2 - 0.1]
        points[7][1] = [center[0] + h/2 - 0.1, center[1] -
                        h/2 - r - 0.01, center[2] + h/2 - 0.1]
        points[7][2] = [center[0] + h/2 - 0.1, center[1] -
                        h/2 - r - 0.01, center[2] - h/2 + 0.1]
        points[7][3] = [center[0] - h/2 + 0.1, center[1] -
                        h/2 - r - 0.01, center[2] - h/2 + 0.1]

        points[4][0] = [center[0] + h/2 + r, center[1] + h/2, center[2] + h/2]
        points[4][1] = [center[0] + h/2 + r, center[1] - h/2, center[2] + h/2]
        points[4][2] = [center[0] + h/2 + r, center[1] - h/2, center[2] - h/2]
        points[4][3] = [center[0] + h/2 + r, center[1] + h/2, center[2] - h/2]
        points[5][0] = [center[0] + h/2 + r + 0.01, center[1] +
                        h/2 - 0.1, center[2] + h/2 - 0.1]
        points[5][1] = [center[0] + h/2 + r + 0.01, center[1] -
                        h/2 + 0.1, center[2] + h/2 - 0.1]
        points[5][2] = [center[0] + h/2 + r + 0.01, center[1] -
                        h/2 + 0.1, center[2] - h/2 + 0.1]
        points[5][3] = [center[0] + h/2 + r + 0.01, center[1] +
                        h/2 - 0.1, center[2] - h/2 + 0.1]

        points[8][0] = [center[0] - h/2 - r, center[1] + h/2, center[2] + h/2]
        points[8][1] = [center[0] - h/2 - r, center[1] - h/2, center[2] + h/2]
        points[8][2] = [center[0] - h/2 - r, center[1] - h/2, center[2] - h/2]
        points[8][3] = [center[0] - h/2 - r, center[1] + h/2, center[2] - h/2]
        points[9][0] = [center[0] - h/2 - r - 0.01,
                        center[1] + h/2 - 0.1, center[2] + h/2 - 0.1]
        points[9][1] = [center[0] - h/2 - r - 0.01,
                        center[1] - h/2 + 0.1, center[2] + h/2 - 0.1]
        points[9][2] = [center[0] - h/2 - r - 0.01,
                        center[1] - h/2 + 0.1, center[2] - h/2 + 0.1]
        points[9][3] = [center[0] - h/2 - r - 0.01,
                        center[1] + h/2 - 0.1, center[2] - h/2 + 0.1]

        return points
