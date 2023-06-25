from constants import *


cost_rotation = 1
cost_grab = 1


class Node:
    def __init__(self, color_l, color_r, last, step, action, dist) -> None:
        self.color_l = color_l
        self.color_r = color_r
        self.last = last
        self.step = step
        self.action = action
        self.dist = dist


class Controllor:
    def __init__(self, color_l="white", color_r="red", solution: str = "F D' U2") -> None:
        self.goal = {"F": "white0", "F'": "white2", "F2": "white1",
                     "U": "red0", "U'": "red2", "U2": "red1",
                     "R": "greed0", "R'": "greed2", "R2": "greed1",
                     "D": "orange0", "D'": "orange2", "D2": "orange1",
                     "L": "blue0", "L'": "blue2", "L2": "blue1",
                     "B": "yellow0", "B'": "yellow2", "B2": "yellow1"}
        self.edge = {"white": ["red", "green", "orange", "blue"],
                     "red": ["white", "blue", "yellow", "greeb"],
                     "green": ["white", "red", "yellow", "orange"],
                     "orange": ["white", "green", "yellow", "blue"],
                     "blue": ["white", "orange", "yellow", "red"],
                     "yellow": ["red", "blue", "orange", "green"]}

        self.queue = []
        self.result = []
        self.solution = []
        self.ans_index = -1
        self.color_l = color_l
        self.color_r = color_r
        for act in solution.split(" "):
            self.solution.append(act)

    def solve(self):
        head = 0
        tail = 1
        node = Node(self.color_l, self.color_r, -1, 0, [], 0)
        self.queue.append(node)

        while (head < tail):
            if self.queue[head].step >= len(self.solution):
                if self.ans_index == -1:
                    self.ans_index = head
                elif self.queue[self.ans_index].dist > self.queue[head].dist:
                    self.ans_index = head
                head = head + 1
                continue

            color_next = self.goal[self.solution[self.queue[head].step]]
            print(color_next)

            if self.queue[head].color_l in color_next:
                self.queue[head].step = self.queue[head].step + 1
                self.queue[head].action.append("L3")
                self.queue[head].action.append("R3")
                if "0" in color_next:
                    self.queue[head].action.append("L0")
                if "1" in color_next:
                    self.queue[head].action.append("L1")
                if "2" in color_next:
                    self.queue[head].action.append("L2")

            elif self.queue[head].color_r in color_next:
                self.queue[head].step = self.queue[head].step + 1
                self.queue[head].action.append("L3")
                self.queue[head].action.append("R3")
                if "0" in color_next:
                    self.queue[head].action.append("R0")
                if "1" in color_next:
                    self.queue[head].action.append("R1")
                if "2" in color_next:
                    self.queue[head].action.append("R2")

            else:
                if color_next[:len(color_next)-1] in self.edge[self.queue[head].color_l]:
                    node_next = Node(self.queue[head].color_l, color_next[:len(
                        color_next)-1], head, self.queue[head].step, [], self.queue[head].dist+cost_rotation)
                    n1 = int(self.edge[self.queue[head].color_l].index(
                        color_next[:len(color_next)-1]))
                    n2 = int(self.edge[self.queue[head].color_l].index(
                        self.queue[head].color_r))
                    diff = (n1-n2+4) % 4
                    node_next.action.append("L3")
                    node_next.action.append("R4")
                    if diff == 1:
                        node_next.action.append("L0")
                    if diff == 2:
                        node_next.action.append("L1")
                    if diff == 3:
                        node_next.action.append("L2")
                    self.queue.append(node_next)
                    tail = tail + 1

                if color_next[:len(color_next)-1] in self.edge[self.queue[head].color_r]:
                    node_next = Node(color_next[:len(color_next)-1], self.queue[head].color_l, head, self.queue[head].step, [
                    ], self.queue[head].dist+cost_rotation)
                    n1 = int(self.edge[self.queue[head].color_r].index(
                        color_next[:len(color_next)-1]))
                    n2 = int(self.edge[self.queue[head].color_r].index(
                        self.queue[head].color_l))
                    diff = (n1-n2+4) % 4
                    node_next.action.append("R3")
                    node_next.action.append("L4")
                    if diff == 1:
                        node_next.action.append("R0")
                    if diff == 2:
                        node_next.action.append("R1")
                    if diff == 3:
                        node_next.action.append("R2")
                    self.queue.append(node_next)
                    tail = tail + 1

                head = head + 1

    def getResult(self, index=-1) -> list:
        if self.queue[index].last != -1:
            self.getResult(self.queue[index].last)
        for act in self.queue[index].action:
            self.result.append(act)
        return self.result


controllor = Controllor()
controllor.solve()
if controllor.ans_index != -1:
    print(controllor.getResult(controllor.ans_index))
