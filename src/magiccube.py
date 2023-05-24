from cube import Cube
from constants import *

class MagicCube:

    def __init__(self) -> None:
        self.solution = []
        self.step = 0
        self.rotation_queue = []
        self.rotation_rate = 18  # Rotation rate  Default: 18 degrees/Hz (Angle system)

        # Cube Color Definition Rules：
        # F L U B R F——W G R Y B O
        self.cubes = []
        self.cubes.append(Cube("101010", (-12, 12, 12), colors=[SELECT_WHITE[1], SELECT_RED[1],
                                                                SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[1], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("101000", (0, 12, 12), colors=[SELECT_WHITE[1], SELECT_RED[1],
                                                              SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("111000", (12, 12, 12), colors=[SELECT_WHITE[1], SELECT_RED[1],
                                                               SELECT_GREEN[1], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("100010", (-12, 0, 12), colors=[SELECT_WHITE[1], SELECT_RED[0],
                                                               SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[1], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("100000", (0, 0, 12), colors=[SELECT_WHITE[1], SELECT_RED[0],
                                                             SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("110000", (12, 0, 12), colors=[SELECT_WHITE[1], SELECT_RED[0],
                                                              SELECT_GREEN[1], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("100011", (-12, -12, 12), colors=[SELECT_WHITE[1], SELECT_RED[0],
                                                                 SELECT_GREEN[0], SELECT_ORANGE[1], SELECT_BULE[1], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("100001", (0, -12, 12), colors=[SELECT_WHITE[1], SELECT_RED[0],
                                                               SELECT_GREEN[0], SELECT_ORANGE[1], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("110001", (12, -12, 12), colors=[SELECT_WHITE[1], SELECT_RED[0],
                                                                SELECT_GREEN[1], SELECT_ORANGE[1], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("001010", (-12, 12, 0), colors=[SELECT_WHITE[0], SELECT_RED[1],
                                                               SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[1], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("001000", (0, 12, 0), colors=[SELECT_WHITE[0], SELECT_RED[1],
                                                             SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("011000", (12, 12, 0), colors=[SELECT_WHITE[0], SELECT_RED[1],
                                                              SELECT_GREEN[1], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("000010", (-12, 0, 0), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                              SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[1], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("010000", (12, 0, 0), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                             SELECT_GREEN[1], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("000011", (-12, -12, 0), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                                SELECT_GREEN[0], SELECT_ORANGE[1], SELECT_BULE[1], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("000001", (0, -12, 0), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                              SELECT_GREEN[0], SELECT_ORANGE[1], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("010001", (12, -12, 0), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                               SELECT_GREEN[1], SELECT_ORANGE[1], SELECT_BULE[0], SELECT_YELLOW[0]]))
        self.cubes.append(Cube("001110", (-12, 12, -12), colors=[SELECT_WHITE[0], SELECT_RED[1],
                                                                 SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[1], SELECT_YELLOW[1]]))
        self.cubes.append(Cube("001100", (0, 12, -12), colors=[SELECT_WHITE[0], SELECT_RED[1],
                                                               SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[1]]))
        self.cubes.append(Cube("011100", (12, 12, -12), colors=[SELECT_WHITE[0], SELECT_RED[1],
                                                                SELECT_GREEN[1], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[1]]))
        self.cubes.append(Cube("000110", (-12, 0, -12), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                                SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[1], SELECT_YELLOW[1]]))
        self.cubes.append(Cube("000100", (0, 0, -12), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                              SELECT_GREEN[0], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[1]]))
        self.cubes.append(Cube("010100", (12, 0, -12), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                               SELECT_GREEN[1], SELECT_ORANGE[0], SELECT_BULE[0], SELECT_YELLOW[1]]))
        self.cubes.append(Cube("000111", (-12, -12, -12), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                                  SELECT_GREEN[0], SELECT_ORANGE[1], SELECT_BULE[1], SELECT_YELLOW[1]]))
        self.cubes.append(Cube("000101", (0, -12, -12), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                                SELECT_GREEN[0], SELECT_ORANGE[1], SELECT_BULE[0], SELECT_YELLOW[1]]))
        self.cubes.append(Cube("010101", (12, -12, -12), colors=[SELECT_WHITE[0], SELECT_RED[0],
                                                                 SELECT_GREEN[1], SELECT_ORANGE[1], SELECT_BULE[0], SELECT_YELLOW[1]]))

    def setRotationRate(self, rate: int):
        self.rotation_rate = rate

    def rotating(self):
        if len(self.rotation_queue) > 0:
            act = self.rotation_queue[0]
            self.rotation_queue.pop(0)
            if act[0] == "F":
                self.rotateWhite(act[1])
            if act[0] == "U":
                self.rotateRed(act[1])
            if act[0] == "R":
                self.rotateGreen(act[1])
            if act[0] == "D":
                self.rotateOrange(act[1])
            if act[0] == "L":
                self.rotateBlue(act[1])
            if act[0] == "B":
                self.rotateYellow(act[1])

    def processShape(self):
        if self.step < len(self.solution):
            self.rotation_queue = []

            if self.solution[self.step] == "F":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("F", -self.rotation_rate))
            if self.solution[self.step] == "F'":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("F", self.rotation_rate))
            if self.solution[self.step] == "F2":
                for i in range(180//self.rotation_rate):
                    self.rotation_queue.append(("F", -self.rotation_rate))

            if self.solution[self.step] == "U":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("U", -self.rotation_rate))
            if self.solution[self.step] == "U'":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("U", self.rotation_rate))
            if self.solution[self.step] == "U2":
                for i in range(180//self.rotation_rate):
                    self.rotation_queue.append(("U", -self.rotation_rate))

            if self.solution[self.step] == "R":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("R", -self.rotation_rate))
            if self.solution[self.step] == "R'":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("R", self.rotation_rate))
            if self.solution[self.step] == "R2":
                for i in range(180//self.rotation_rate):
                    self.rotation_queue.append(("R", -self.rotation_rate))

            if self.solution[self.step] == "D":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("D", -self.rotation_rate))
            if self.solution[self.step] == "D'":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("D", self.rotation_rate))
            if self.solution[self.step] == "D2":
                for i in range(180//self.rotation_rate):
                    self.rotation_queue.append(("D", -self.rotation_rate))

            if self.solution[self.step] == "L":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("L", -self.rotation_rate))
            if self.solution[self.step] == "L'":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("L", self.rotation_rate))
            if self.solution[self.step] == "L2":
                for i in range(180//self.rotation_rate):
                    self.rotation_queue.append(("L", -self.rotation_rate))

            if self.solution[self.step] == "B":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("B", -self.rotation_rate))
            if self.solution[self.step] == "B'":
                for i in range(90//self.rotation_rate):
                    self.rotation_queue.append(("B", self.rotation_rate))
            if self.solution[self.step] == "B2":
                for i in range(180//self.rotation_rate):
                    self.rotation_queue.append(("B", -self.rotation_rate))

            self.step += 1

    def setMagicCube(self, state):
        # Color Setting Order：U-R-F-D-L-B
        index = 0

        # Up
        self.cubes[17].setPaletteColor(1, state[index])
        index += 1
        self.cubes[18].setPaletteColor(1, state[index])
        index += 1
        self.cubes[19].setPaletteColor(1, state[index])
        index += 1
        self.cubes[9].setPaletteColor(1, state[index])
        index += 1
        self.cubes[10].setPaletteColor(1, state[index])
        index += 1
        self.cubes[11].setPaletteColor(1, state[index])
        index += 1
        self.cubes[0].setPaletteColor(1, state[index])
        index += 1
        self.cubes[1].setPaletteColor(1, state[index])
        index += 1
        self.cubes[2].setPaletteColor(1, state[index])
        index += 1

        # Right
        self.cubes[2].setPaletteColor(2, state[index])
        index += 1
        self.cubes[11].setPaletteColor(2, state[index])
        index += 1
        self.cubes[19].setPaletteColor(2, state[index])
        index += 1
        self.cubes[5].setPaletteColor(2, state[index])
        index += 1
        self.cubes[13].setPaletteColor(2, state[index])
        index += 1
        self.cubes[22].setPaletteColor(2, state[index])
        index += 1
        self.cubes[8].setPaletteColor(2, state[index])
        index += 1
        self.cubes[16].setPaletteColor(2, state[index])
        index += 1
        self.cubes[25].setPaletteColor(2, state[index])
        index += 1

        # Front
        self.cubes[0].setPaletteColor(0, state[index])
        index += 1
        self.cubes[1].setPaletteColor(0, state[index])
        index += 1
        self.cubes[2].setPaletteColor(0, state[index])
        index += 1
        self.cubes[3].setPaletteColor(0, state[index])
        index += 1
        self.cubes[4].setPaletteColor(0, state[index])
        index += 1
        self.cubes[5].setPaletteColor(0, state[index])
        index += 1
        self.cubes[6].setPaletteColor(0, state[index])
        index += 1
        self.cubes[7].setPaletteColor(0, state[index])
        index += 1
        self.cubes[8].setPaletteColor(0, state[index])
        index += 1

        # Down
        self.cubes[6].setPaletteColor(3, state[index])
        index += 1
        self.cubes[7].setPaletteColor(3, state[index])
        index += 1
        self.cubes[8].setPaletteColor(3, state[index])
        index += 1
        self.cubes[14].setPaletteColor(3, state[index])
        index += 1
        self.cubes[15].setPaletteColor(3, state[index])
        index += 1
        self.cubes[16].setPaletteColor(3, state[index])
        index += 1
        self.cubes[23].setPaletteColor(3, state[index])
        index += 1
        self.cubes[24].setPaletteColor(3, state[index])
        index += 1
        self.cubes[25].setPaletteColor(3, state[index])
        index += 1

        # Left
        self.cubes[17].setPaletteColor(4, state[index])
        index += 1
        self.cubes[9].setPaletteColor(4, state[index])
        index += 1
        self.cubes[0].setPaletteColor(4, state[index])
        index += 1
        self.cubes[20].setPaletteColor(4, state[index])
        index += 1
        self.cubes[12].setPaletteColor(4, state[index])
        index += 1
        self.cubes[3].setPaletteColor(4, state[index])
        index += 1
        self.cubes[23].setPaletteColor(4, state[index])
        index += 1
        self.cubes[14].setPaletteColor(4, state[index])
        index += 1
        self.cubes[6].setPaletteColor(4, state[index])
        index += 1

        # Back
        self.cubes[19].setPaletteColor(5, state[index])
        index += 1
        self.cubes[18].setPaletteColor(5, state[index])
        index += 1
        self.cubes[17].setPaletteColor(5, state[index])
        index += 1
        self.cubes[22].setPaletteColor(5, state[index])
        index += 1
        self.cubes[21].setPaletteColor(5, state[index])
        index += 1
        self.cubes[20].setPaletteColor(5, state[index])
        index += 1
        self.cubes[25].setPaletteColor(5, state[index])
        index += 1
        self.cubes[24].setPaletteColor(5, state[index])
        index += 1
        self.cubes[23].setPaletteColor(5, state[index])
        index += 1

    def setSolution(self, solution: str):
        self.solution = []
        self.step = 0
        for act in solution.split(" "):
            self.solution.append(act)

    def drawMagicCube(self):
        for i in range(26):
            self.cubes[i].drawCube()

    def rotateWhite(self, th=3):
        for i in range(26):
            if(self.cubes[i].center[2] > 10):
                self.cubes[i].rotateCubeZ(th)

    def rotateGreen(self, th=3):
        for i in range(26):
            if(self.cubes[i].center[0] > 10):
                self.cubes[i].rotateCubeX(th)

    def rotateRed(self, th=3):
        for i in range(26):
            if(self.cubes[i].center[1] > 10):
                self.cubes[i].rotateCubeY(th)

    def rotateYellow(self, th=3):
        for i in range(26):
            if(self.cubes[i].center[2] < -10):
                self.cubes[i].rotateCubeZ(-th)

    def rotateBlue(self, th=3):
        for i in range(26):
            if(self.cubes[i].center[0] < -10):
                self.cubes[i].rotateCubeX(-th)

    def rotateOrange(self, th=3):
        for i in range(26):
            if(self.cubes[i].center[1] < -10):
                self.cubes[i].rotateCubeY(-th)
