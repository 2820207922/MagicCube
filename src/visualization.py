# -*- coding:utf8 -*-

import os
import qbr
import math
import pyglet
from magiccube import MagicCube
from OpenGL.GL import *
from OpenGL.GLU import *

IMAGE_DIR = os.path.join('D:\Project\Python\MagicCube\images')

class Border():

    def __init__(self, x, y, width, height, bold=1, color=(255, 255, 255, 255), batch=None) -> None:
        self.x, self.y, self.width, self.height = x, y, width, height
        self.line_down = pyglet.shapes.Line(
            x-1, y, x+width+1, y, bold, color, batch)
        self.line_right = pyglet.shapes.Line(
            x+width, y-1, x+width, y+height+1, bold, color, batch)
        self.line_top = pyglet.shapes.Line(
            x+width+1, y+height, x-1, y+height, bold, color, batch)
        self.line_left = pyglet.shapes.Line(
            x, y+height+1, x, y-1, bold, color, batch)


class Button():

    def __init__(self, x, y, pressed: str, depressed: str) -> None:
        super().__init__()
        self.is_pressed = 0
        self.position_x, self.position_y = x, y
        self.pressed = pyglet.sprite.Sprite(pyglet.image.load(
            pressed), self.position_x, self.position_y)
        self.depressed = pyglet.sprite.Sprite(pyglet.image.load(
            depressed), self.position_x, self.position_y)
        self.width, self.height = self.pressed.width, self.pressed.height

    def draw(self):
        if(self.is_pressed > 0):
            self.is_pressed -= 1
            self.pressed.draw()
        else:
            self.depressed.draw()

    def IsPressed(self, x, y) -> bool:
        if(x >= self.position_x and x <= self.position_x+self.width and y >= self.position_y and y <= self.position_y+self.height):
            self.is_pressed = 2
            return True


class MainWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.qbr = qbr.Qbr(qbr.args.normalize)

        # print("window's width = %d, window's height = %d" %
        #       (self.width, self.height))

        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)

        self.batch = pyglet.graphics.Batch()

        self.main_border = Border(
            240, 120, 480, 300, 4, (100, 100, 100, 255), self.batch)

        self.button_scan = Button(820, 300, IMAGE_DIR +
                                  "\\scan_pressed.png", IMAGE_DIR + "\\scan_depressed.png")
        self.button_play = Button(464, 70, IMAGE_DIR +
                                  "\\play_pressed.png", IMAGE_DIR + "\\play_depressed.png")
        self.button_pause = Button(464, 70, IMAGE_DIR +
                                   "\\pause_pressed.png", IMAGE_DIR + "\\pause_depressed.png")
        self.button_last = Button(416, 70, IMAGE_DIR +
                                   "\\last_step_pressed.png", IMAGE_DIR + "\\last_step_depressed.png")
        self.button_next = Button(512, 70, IMAGE_DIR +
                                   "\\next_step_pressed.png", IMAGE_DIR + "\\next_step_depressed.png")
        self.button_first = Button(368, 70, IMAGE_DIR +
                                   "\\first_step_pressed.png", IMAGE_DIR + "\\first_step_depressed.png")
        self.button_final = Button(560, 70, IMAGE_DIR +
                                   "\\final_step_pressed.png", IMAGE_DIR + "\\final_step_depressed.png")
        self.button_rate = Button(250, 380, IMAGE_DIR +
                                  "\\rate_pressed.png", IMAGE_DIR + "\\rate_depressed.png")

        self.magic_cube = MagicCube()
        self.magic_cube.setRotationRate(18)

        self.cam_x, self.cam_y, self.cam_z, self.cam_r = 0, 0, 80, 80   # Camera initial position and distance
        self.cube_vel = 0.5     # Magic Cube Control Sensitivity
        self.is_playing: bool = 0

        self.rotating_rate = (3,9,18,30,45)
        self.rate_index = 2
        self.rate_image_path = (IMAGE_DIR+"\\num1.png",IMAGE_DIR+"\\num2.png",IMAGE_DIR+"\\num3.png",IMAGE_DIR+"\\num4.png",IMAGE_DIR+"\\num5.png")
        self.rate_image = pyglet.sprite.Sprite(pyglet.image.load(self.rate_image_path[self.rate_index]), 290, 380)

    def drawButton(self):
        self.button_scan.draw()
        self.button_last.draw()
        self.button_next.draw()
        self.button_first.draw()
        self.button_final.draw()
        self.button_rate.draw()
        self.rate_image.draw()
        if self.is_playing :
            self.button_pause.draw()
        else:
            self.button_play.draw()

    def setViewport(self):

        self.clear()  # 或 glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)  # 清除深度(z排序)缓冲区

        # 光滑渲染
        glEnable(GL_BLEND)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 反走样，也称抗锯齿
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_FASTEST)

        glMatrixMode(GL_PROJECTION)  # 设置当前矩阵为投影矩阵
        glLoadIdentity()

        # 透视投影, 类似游戏中的FOV(视角大小)
        glFrustum(-16*self.cam_r/80, 16*self.cam_r/80, -9*self.cam_r/80,
                  9*self.cam_r/80, 10*self.cam_r/80, 100*self.cam_r/80)

        glMatrixMode(GL_MODELVIEW)  # 模型视图矩阵
        glLoadIdentity()

        glViewport(0, 0, self.width, self.height)

        glClearColor(0.7, 0.7, 0.7, 1)  # 设置背景为灰白色
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)     # 开启深度测试

        gluLookAt(self.cam_x, self.cam_y, self.cam_z, 0, 0, 0, 0, 1, 0)

        # 将绘制的图形显示在屏幕上
        glFlush()

    def on_draw(self):
        if(self.visible):
            self.setViewport()
            self.drawButton()
            self.batch.draw()
            self.magic_cube.drawMagicCube()

            if self.is_playing:
                self.magic_cube.rotating()

            if self.button_rate.is_pressed:
                self.button_rate.is_pressed = 0
                self.rate_index = (self.rate_index + 1) % 5
                self.magic_cube.setRotationRate(self.rotating_rate[self.rate_index])
                self.rate_image = pyglet.sprite.Sprite(pyglet.image.load(self.rate_image_path[self.rate_index]), 290, 380)

            if self.button_play.is_pressed:
                self.is_playing = 1
                self.button_play.is_pressed = 0
            if self.button_pause.is_pressed or (self.magic_cube.step == len(self.magic_cube.solution) and len(self.magic_cube.rotation_queue) == 0):
                self.is_playing = 0
                self.button_pause.is_pressed = 0

            if self.button_first.is_pressed:
                self.is_playing = 0
                self.button_first.is_pressed = 0
                self.magic_cube.__init__()
                if not self.qbr.state is None:
                    self.magic_cube.setMagicCube(self.qbr.state)
                if not self.qbr.solution is None:
                    self.magic_cube.setSolution(self.qbr.solution)
                    self.magic_cube.step = 0
            
            if self.button_final.is_pressed:
                self.is_playing = 0
                self.button_final.is_pressed = 0
                self.magic_cube.__init__()
                if not self.qbr.solution is None:
                    self.magic_cube.setSolution(self.qbr.solution)
                    self.magic_cube.step = len(self.magic_cube.solution)

            if self.button_last.is_pressed:
                self.is_playing = 0
                self.button_last.is_pressed = 0
                if len(self.magic_cube.rotation_queue) > 0:
                    while len(self.magic_cube.rotation_queue) > 0:
                        self.magic_cube.rotating()
                    if self.magic_cube.step > 0:
                        self.magic_cube.step -= 1
                        if self.magic_cube.solution[self.magic_cube.step] == "F":
                            self.magic_cube.rotateWhite(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "F'":
                            self.magic_cube.rotateWhite(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "F2":
                            self.magic_cube.rotateWhite(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "U":
                            self.magic_cube.rotateRed(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "U'":
                            self.magic_cube.rotateRed(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "U2":
                            self.magic_cube.rotateRed(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "R":
                            self.magic_cube.rotateGreen(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "R'":
                            self.magic_cube.rotateGreen(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "R2":
                            self.magic_cube.rotateGreen(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "D":
                            self.magic_cube.rotateOrange(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "D'":
                            self.magic_cube.rotateOrange(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "D2":
                            self.magic_cube.rotateOrange(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "L":
                            self.magic_cube.rotateBlue(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "L'":
                            self.magic_cube.rotateBlue(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "L2":
                            self.magic_cube.rotateBlue(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "B":
                            self.magic_cube.rotateYellow(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "B'":
                            self.magic_cube.rotateYellow(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "B2":
                            self.magic_cube.rotateYellow(180)
                else:
                    if self.magic_cube.step > 0:
                        self.magic_cube.step -= 1
                        if self.magic_cube.solution[self.magic_cube.step] == "F":
                            self.magic_cube.rotateWhite(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "F'":
                            self.magic_cube.rotateWhite(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "F2":
                            self.magic_cube.rotateWhite(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "U":
                            self.magic_cube.rotateRed(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "U'":
                            self.magic_cube.rotateRed(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "U2":
                            self.magic_cube.rotateRed(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "R":
                            self.magic_cube.rotateGreen(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "R'":
                            self.magic_cube.rotateGreen(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "R2":
                            self.magic_cube.rotateGreen(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "D":
                            self.magic_cube.rotateOrange(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "D'":
                            self.magic_cube.rotateOrange(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "D2":
                            self.magic_cube.rotateOrange(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "L":
                            self.magic_cube.rotateBlue(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "L'":
                            self.magic_cube.rotateBlue(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "L2":
                            self.magic_cube.rotateBlue(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "B":
                            self.magic_cube.rotateYellow(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "B'":
                            self.magic_cube.rotateYellow(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "B2":
                            self.magic_cube.rotateYellow(180)

            if self.button_next.is_pressed:
                self.is_playing = 0
                self.button_next.is_pressed = 0
                if len(self.magic_cube.rotation_queue) > 0:
                    while len(self.magic_cube.rotation_queue) > 0:
                        self.magic_cube.rotating()
                else:
                    if self.magic_cube.step < len(self.magic_cube.solution):
                        if self.magic_cube.solution[self.magic_cube.step] == "F":
                            self.magic_cube.rotateWhite(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "F'":
                            self.magic_cube.rotateWhite(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "F2":
                            self.magic_cube.rotateWhite(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "U":
                            self.magic_cube.rotateRed(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "U'":
                            self.magic_cube.rotateRed(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "U2":
                            self.magic_cube.rotateRed(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "R":
                            self.magic_cube.rotateGreen(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "R'":
                            self.magic_cube.rotateGreen(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "R2":
                            self.magic_cube.rotateGreen(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "D":
                            self.magic_cube.rotateOrange(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "D'":
                            self.magic_cube.rotateOrange(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "D2":
                            self.magic_cube.rotateOrange(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "L":
                            self.magic_cube.rotateBlue(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "L'":
                            self.magic_cube.rotateBlue(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "L2":
                            self.magic_cube.rotateBlue(180)

                        if self.magic_cube.solution[self.magic_cube.step] == "B":
                            self.magic_cube.rotateYellow(-90)
                        if self.magic_cube.solution[self.magic_cube.step] == "B'":
                            self.magic_cube.rotateYellow(90)
                        if self.magic_cube.solution[self.magic_cube.step] == "B2":
                            self.magic_cube.rotateYellow(180)
                        
                        self.magic_cube.step += 1

            if len(self.magic_cube.rotation_queue) == 0 and self.is_playing:
                self.magic_cube.processShape()

            if self.button_scan.is_pressed:
                self.set_visible(False)
                self.qbr.run()
                if not self.qbr.state is None:
                    self.magic_cube.setMagicCube(self.qbr.state)
                if not self.qbr.solution is None:
                    self.magic_cube.setSolution(self.qbr.solution)
                self.set_visible(True)
            

    def on_mouse_press(self, x, y, button, modifiers):
        if (button & pyglet.window.mouse.LEFT):
            self.button_scan.IsPressed(x, y)
            self.button_last.IsPressed(x, y)
            self.button_next.IsPressed(x, y)
            self.button_first.IsPressed(x, y)
            self.button_final.IsPressed(x, y)
            self.button_rate.IsPressed(x, y)
            if self.is_playing:
                self.button_pause.IsPressed(x, y)
            else:
                self.button_play.IsPressed(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):

        if (buttons & pyglet.window.mouse.LEFT):

            if(x >= self.main_border.x and x <= self.main_border.x+self.main_border.width and
                    y >= self.main_border.y and y <= self.main_border.y+self.main_border.height):

                th1 = math.atan2(
                    math.sqrt(math.pow(self.cam_z, 2)+math.pow(self.cam_x, 2)), self.cam_y)
                th2 = math.atan2(self.cam_x, self.cam_z)

                self.cam_z = self.cam_r*math.sin(dy/self.cam_r*self.cube_vel+th1) * \
                    math.cos(-dx/self.cam_r*self.cube_vel+th2)
                self.cam_x = self.cam_r*math.sin(dy/self.cam_r*self.cube_vel+th1) * \
                    math.sin(-dx/self.cam_r*self.cube_vel+th2)
                self.cam_y = self.cam_r * \
                    math.cos(dy/self.cam_r*self.cube_vel+th1)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):

        if(self.cam_r - scroll_y * 5 >= 70 and self.cam_r - scroll_y * 5 <= 100):
            self.cam_r -= scroll_y * 5

        self.cube_vel = self.cam_r / 160

        th1 = math.atan2(
            math.sqrt(math.pow(self.cam_z, 2)+math.pow(self.cam_x, 2)), self.cam_y)
        th2 = math.atan2(self.cam_x, self.cam_z)

        self.cam_x = self.cam_r*math.sin(th1) * math.sin(th2)
        self.cam_y = self.cam_r * math.cos(th1)
        self.cam_z = self.cam_r*math.sin(th1) * math.cos(th2)


if __name__ == "__main__":
    window = MainWindow()
    pyglet.app.run(1/30)
