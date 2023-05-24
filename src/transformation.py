from colordetection import color_detector


class Transform:

    def __init__(self) -> None:
        '''[3, 5, 6, 7, 10, 11, 17, 20, 21, 24, 25, 34, 36, 38, 40, 42, 48, 52, 56]'''
        self.success: bool = 0
        self.current_cube = [0, 0, 0, 0, 0, 0]
        self.colors_order = {"white": 0, "red": 1,
                             "green": 2, "orange": 3, "blue": 4, "yellow": 5}
        self.colors_value = {"white": 32, "green": 16,
                             "red": 8, "yellow": 4, "blue": 2, "orange": 1}
        self.colors_opposite = [(32, 4), (8, 1), (16, 2)]

    def tranform_3D_to_2D(self):
        result = {}

        for key, value in self.colors_order.items():
            preview = self.current_cube[value]
            result[key] = [preview[0], preview[1], preview[2],
                           preview[7], preview[8], preview[3], preview[6], preview[5], preview[4]]

        self.current_cube = [0, 0, 0, 0, 0, 0]

        return result

    def transform_2D_to_3D(self, current_cube: dict):

        for side, preview in current_cube.items():
            value = [preview[0], preview[1], preview[2], preview[5],
                     preview[8], preview[7], preview[6], preview[3], preview[4]]
            self.current_cube[self.colors_order[side]] = value
            # print(side)

        self.check_side(0)

    def judge_color(self, color) -> str:
        for key, value in color_detector.cube_color_palette.items():
            if value == color:
                return key

    def rotate_side(self, side):
        result = []
        preview = self.current_cube[side]
        for i in range(8):
            result.append(preview[(i+2) % 8])
        result.append(preview[8])
        self.current_cube[side] = result

    def calc(self, *args):
        n = len(args)
        sum = 0
        for i in range(n):
            sum |= self.colors_value[self.judge_color(args[i])]
        return sum

    def check(self):
        cube_num = []

        cube_num.append(self.calc(
            self.current_cube[0][0], self.current_cube[1][6], self.current_cube[4][2]))
        cube_num.append(self.calc(
            self.current_cube[0][1], self.current_cube[1][5]))
        cube_num.append(self.calc(
            self.current_cube[0][2], self.current_cube[1][4], self.current_cube[2][0]))
        cube_num.append(self.calc(
            self.current_cube[0][3], self.current_cube[2][7]))
        cube_num.append(self.calc(
            self.current_cube[0][4], self.current_cube[2][6], self.current_cube[3][2]))
        cube_num.append(self.calc(
            self.current_cube[0][5], self.current_cube[3][1]))
        cube_num.append(self.calc(
            self.current_cube[0][6], self.current_cube[3][0], self.current_cube[4][4]))
        cube_num.append(self.calc(
            self.current_cube[0][7], self.current_cube[4][3]))
        cube_num.append(self.calc(
            self.current_cube[1][7], self.current_cube[4][1]))
        cube_num.append(self.calc(
            self.current_cube[1][3], self.current_cube[2][1]))
        cube_num.append(self.calc(
            self.current_cube[3][3], self.current_cube[2][5]))
        cube_num.append(self.calc(
            self.current_cube[3][7], self.current_cube[4][5]))
        cube_num.append(self.calc(
            self.current_cube[1][0], self.current_cube[4][0], self.current_cube[5][2]))
        cube_num.append(self.calc(
            self.current_cube[1][1], self.current_cube[5][1]))
        cube_num.append(self.calc(
            self.current_cube[1][2], self.current_cube[2][2], self.current_cube[5][0]))
        cube_num.append(self.calc(
            self.current_cube[2][3], self.current_cube[5][7]))
        cube_num.append(self.calc(
            self.current_cube[2][4], self.current_cube[3][4], self.current_cube[5][6]))
        cube_num.append(self.calc(
            self.current_cube[3][5], self.current_cube[5][5]))
        cube_num.append(self.calc(
            self.current_cube[3][6], self.current_cube[4][6], self.current_cube[5][4]))

        cube_num.sort()
        for i in range(len(cube_num)-1):
            if cube_num[i] == cube_num[i+1]:
                return False

        # print(cube_num)

        for n in cube_num:
            for m in self.colors_opposite:
                if n & m[0] > 0 and n & m[1] > 0:
                    return False

        return True

    def check_side(self, side):
        if side == 6:
            self.success = self.check()
            return

        for i in range(4):
            self.rotate_side(side)
            self.check_side(side+1)
            if self.success:
                break


transform = Transform()
