# coding:utf-8
import sys
import time
import tkinter
from queue import Queue
from tkinter import messagebox
from random import randint

class gridDrawDraw(object):
    def __init__(self, master=None, window_width=800, window_height=600, gridDraw_width=50, offset=10):
        self.width = window_width
        self.height = window_height
        self.gridDraw_width = gridDraw_width
        self.gridDraw_height = gridDraw_width

        self.offset = offset
        self.gridDraw_x = int(self.width/self.gridDraw_width)
        self.gridDraw_y = int(self.height/self.gridDraw_width)

        self.gridDrawColor = '#FFFFFF'
        self.bg = '#EBEBEB'
        self.canvas = tkinter.Canvas(master, width=self.width+2*self.offset, height=self.height+2*self.offset, bg=self.bg)
        self.canvas.pack()
        self.gridDraw_list()

    def drawAll(self):
        for x in range(0, int((self.width-self.offset)/self.gridDraw_width+1)):
            for y in range(0, int((self.height-self.offset)/self.gridDraw_height+1)):
                self.draw((x, y), self.gridDrawColor)

    def draw(self, pos, color):
        x = pos[0]*self.gridDraw_width + self.offset
        y = pos[1]*self.gridDraw_height + self.offset
        self.canvas.create_rectangle(x, y, x+self.gridDraw_width, y+self.gridDraw_height, fill=color, outline='#000000')

    def drawSnakeHead(self, pos, headPhoto, direction):
        x = int(pos[0]*self.gridDraw_width + self.offset + self.gridDraw_width/2)
        y = int(pos[1]*self.gridDraw_height + self.offset + self.gridDraw_height/2)
        self.canvas.create_image(x, y, image=headPhoto)

    def drawSnakeBody(self, body, bodyPhoto, direction):
        for x, y in body:
            self.draw((x, y), self.gridDrawColor)
            x = int(x*self.gridDraw_width + self.offset + self.gridDraw_width/2)
            y = int(y*self.gridDraw_width + self.offset + self.gridDraw_height/2)
            self.canvas.create_image(x, y, image=bodyPhoto)

    def drawSnakeTail(self, pos, tailPhoto, direction):
        x = int(pos[0]*self.gridDraw_width + self.offset + self.gridDraw_width/2)
        y = int(pos[1]*self.gridDraw_width + self.offset + self.gridDraw_height/2)
        self.canvas.create_image(x, y, image=tailPhoto)

    def drawFood(self, pos, photo):
        x = int(pos[0]*self.gridDraw_width + self.offset + self.gridDraw_width/2)
        y = int(pos[1]*self.gridDraw_height + self.offset + self.gridDraw_width/2)
        self.canvas.create_image(x, y, image=photo)

    def gridDraw_list(self):
        gridDrawList = []
        for x in range(0, self.gridDraw_x):
            for y in range(0, self.gridDraw_y):
                gridDrawList.append((x, y))
        self.gridDrawList = gridDrawList

class Food(object):
    def __init__(self, gridDraw):
        self.gridDraw = gridDraw
        self.color = '#23D978'
        self.photo = tkinter.PhotoImage(file='food.png')
        self.set_pos()

    def set_pos(self):
        x = randint(0, self.gridDraw.gridDraw_x-1)
        y = randint(0, self.gridDraw.gridDraw_y-1)
        self.pos = (x, y)

    def display(self):
        self.gridDraw.draw(self.pos, self.gridDraw.gridDrawColor)
        self.gridDraw.drawFood(self.pos, self.photo)

class Snake(object):
    def __init__(self, gridDraw):
        self.gridDraw = gridDraw

        self.body = [(10, 6), (10, 7), (10, 8)]
        self.food = Food(self.gridDraw)
        self.display_food()

        self.headPhoto = tkinter.PhotoImage(file='head.png')
        self.bodyPhoto = tkinter.PhotoImage(file='body.png')
        self.tailPhoto = tkinter.PhotoImage(file='tail.png')

        #保存bfs中的路径节点关系
        self.forward = []

        #保存是否访问过的状态
        self.vis = []

        #保存移动路径
        self.path = []

        self.direction = 'Up'
        self.status = ['run', 'stop']
        self.speed = 300
        self.color = '#5FA8D9'
        self.gameover = False
        self.score = 0

    def avilable_gridDraw(self):
        return [i for i in self.gridDraw.gridDrawList if i not in self.body[2:]]

    def change_direction(self, direction):
        self.direction = direction

    def display_food(self):
        while(self.food.pos in self.body):
            self.food.set_pos()
        self.food.display()

    def getDirec(self, lastPoint, currPoint):
        if currPoint[0] == lastPoint[0]:
            if currPoint[1] - lastPoint[1] == 1:
                return 'Down'
            if currPoint[1] - lastPoint[1] == -1:
                return 'Up'
        if currPoint[1] == lastPoint[1]:
            if currPoint[0] - lastPoint[0] == 1:
                return 'Right'
            if currPoint[0] - lastPoint[0] == -1:
                return 'Left'

    def callDFS(self):
        self.forward = [ [ (-1, -1) for i in range(0, 50) ] for j in range(0, 50)]
        self.vis = [ [ False for i in range(0, 50) ] for j in range(0, 50) ]
        self.dfs(self.body[0])
        print(self.path)
        self.path.pop()

    #dfs搜索路径
    def dfs(self, point):
        self.vis[point[0]][point[1]] = True
        if point == self.food.pos:
            self.path.append(point)
            return True

        if self.forward[point[0]][point[1]] == (-1, -1):
            lastPoint = self.body[1]
        else:
            lastPoint = self.forward[point[0]][point[1]]

        #向右搜索
        newPoint = (point[0]+1, point[1])
        self.forward[newPoint[0]][newPoint[1]] = (point[0], point[1])
        if not self.getDirec(lastPoint, point) == 'Left' and not self.vis[newPoint[0]][newPoint[1]] and newPoint[0] in range(self.gridDraw.gridDraw_x) and newPoint[1] in range(self.gridDraw.gridDraw_y):
            if self.dfs(newPoint) == True:
                self.path.append(point)
                return True
            else:
                self.vis[newPoint[0]][newPoint[1]] = False
                self.forward[newPoint[0]][newPoint[1]] = (-1, -1)

        #向下搜索
        newPoint = (point[0], point[1]+1)
        self.forward[newPoint[0]][newPoint[1]] = (point[0], point[1])
        if not self.getDirec(lastPoint, point) == 'Up' and not self.vis[newPoint[0]][newPoint[1]] and newPoint[0] in range(self.gridDraw.gridDraw_x) and newPoint[1] in range(self.gridDraw.gridDraw_y):
            if self.dfs(newPoint) == True:
                self.path.append(point)
                return True
            else:
                self.vis[newPoint[0]][newPoint[1]] = False
                self.forward[newPoint[0]][newPoint[1]] = (-1, -1)

        #向左搜索
        newPoint = (point[0]-1, point[1])
        self.forward[newPoint[0]][newPoint[1]] = (point[0], point[1])
        if not self.getDirec(lastPoint, point) == 'Right' and not self.vis[newPoint[0]][newPoint[1]] and newPoint[0] in range(self.gridDraw.gridDraw_x) and newPoint[1] in range(self.gridDraw.gridDraw_y):
            if self.dfs(newPoint) == True:
                self.path.append(point)
                return True
            else:
                self.vis[newPoint[0]][newPoint[1]] = False
                self.forward[newPoint[0]][newPoint[1]] = (-1, -1)

        #向上搜索
        newPoint = (point[0], point[1]-1)
        self.forward[newPoint[0]][newPoint[1]] = (point[0], point[1])
        if not self.getDirec(lastPoint, point) == 'Down' and not self.vis[newPoint[0]][newPoint[1]] and newPoint[0] in range(self.gridDraw.gridDraw_x) and newPoint[1] in range(self.gridDraw.gridDraw_y):
            if self.dfs(newPoint) == True:
                self.path.append(point)
                return True
            else:
                self.vis[newPoint[0]][newPoint[1]] = False
                self.forward[newPoint[0]][newPoint[1]] = (-1, -1)

    #bfs搜索路径
    def bfs(self):

        headPos = self.body[0]

        self.forward = [ [ (-1, -1) for i in range(0, 50) ] for j in range(0, 50)]
        self.vis = [ [False for i in range(0, 50)] for j in range(0, 50)]

        que = Queue()
        que.put(headPos)
        self.vis[headPos[0]][headPos[1]] = True

        while not que.empty():
            headPos = que.get()
            if headPos == self.food.pos:            #吃到食物
                while not headPos == (-1, -1):      #保存路径
                    self.path.append(headPos)
                    x = headPos[0]
                    y = headPos[1]
                    headPos = self.forward[x][y]
                self.path.pop(-1)                   #退出头节点
                return

            if self.forward[headPos[0]][headPos[1]] == (-1, -1): #头节点开始搜索，需要判定可行搜索方向
                lastPoint = self.body[1]
            else:
                lastPoint = self.forward[headPos[0]][headPos[1]]

            if not self.getDirec(lastPoint, headPos) == 'Left' and not self.vis[headPos[0]+1][headPos[1]]:  #当前方向不向左时向右搜索
                self.vis[headPos[0]+1][headPos[1]] = True
                self.forward[headPos[0]+1][headPos[1]] = (headPos[0], headPos[1])
                que.put((headPos[0]+1, headPos[1]))

            if not self.getDirec(lastPoint, headPos) == 'Up' and not self.vis[headPos[0]][headPos[1]+1]:  #向下搜索
                self.vis[headPos[0]][headPos[1]+1] = True
                self.forward[headPos[0]][headPos[1]+1] = (headPos[0], headPos[1])
                que.put((headPos[0], headPos[1]+1))

            if not self.getDirec(lastPoint, headPos) == 'Right' and not self.vis[headPos[0]-1][headPos[1]]:  #向左搜索
                self.vis[headPos[0]-1][headPos[1]] = True
                self.forward[headPos[0]-1][headPos[1]] = (headPos[0], headPos[1])
                que.put((headPos[0]-1, headPos[1]))

            if not self.getDirec(lastPoint, headPos) == 'Down' and not self.vis[headPos[0]][headPos[1]-1]:  #向上搜索
                self.vis[headPos[0]][headPos[1]-1] = True
                self.forward[headPos[0]][headPos[1]-1] = (headPos[0], headPos[1])
                que.put((headPos[0], headPos[1]-1))

    def display(self):
        self.gridDraw.drawSnakeHead(self.body[0], self.headPhoto, self.direction)
        self.gridDraw.drawSnakeBody(self.body[1:-1], self.bodyPhoto, self.direction)
        self.gridDraw.drawSnakeTail(self.body[-1], self.tailPhoto, self.direction)

    def move(self):

        head = self.body[0]
        if self.direction == 'Up':
            new = (head[0], head[1]-1)
        elif self.direction == 'Down':
            new = (head[0], head[1]+1)
        elif self.direction == 'Left':
            new = (head[0]-1, head[1])
        else: new = (head[0]+1, head[1])

        print(new)
        self.body.insert(0, new)

        if new not in self.avilable_gridDraw():
            self.status.reverse()
            self.gameover = True
        else:

            if not self.food.pos == new:
                pop = self.body.pop()
                self.gridDraw.draw(pop, self.gridDraw.gridDrawColor)
            else:
                print('当前食物位置：', self.food.pos)
                self.display_food()
                self.score += 1
                self.callDFS()
                print('新的食物位置', self.food.pos)
                print('吃到食物，获取新路径：', self.path)

            #画头
            self.gridDraw.draw(new, self.gridDraw.gridDrawColor)
            self.gridDraw.drawSnakeHead(new, self.headPhoto, self.direction)
            #画身体
            self.gridDraw.drawSnakeBody(self.body[1:-1], self.bodyPhoto, self.direction)
            #画尾巴
            self.gridDraw.draw(self.body[-1], self.gridDraw.gridDrawColor)
            self.gridDraw.drawSnakeTail(self.body[-1], self.tailPhoto, self.direction)

class Anakonda(tkinter.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.gridDraw = gridDrawDraw(master, *args, **kwargs)
        self.gridDraw.drawAll()
        self.snake = Snake(self.gridDraw)

        #self.master.bind("<Key>", self.key_release)
        self.snake.display()
        self.snake.callDFS()

    def run(self):
        if not self.snake.status[0] == 'stop':
            pos = self.snake.path.pop(-1)
            if pos[0] - self.snake.body[0][0] == 1:
                self.snake.direction = 'Right'
            if pos[0] - self.snake.body[0][0] == -1:
                self.snake.direction = 'Left'
            if pos[1] - self.snake.body[0][1] == -1:
                self.snake.direction = 'Up'
            if pos[1] - self.snake.body[0][1] == 1:
                self.snake.direction = 'Down'
            self.snake.move()

        if self.snake.gameover == True:
            message = messagebox.showinfo("Game Over", "Your Score: %d" % self.snake.score)
            if message == 'ok':
                sys.exit()

        self.after(self.snake.speed, self.run)

    def key_release(self, event):       #绑定键盘操作

        key = event.keysym
        key_dict = {"Up":"Down", "Down":"Up", "Left":"Right", "Right":"Left"}
        if key in key_dict and not key == key_dict[self.snake.direction]:
            self.snake.change_direction(key)
            self.snake.move()
        elif key == 'p':
            self.snake.status.reverse()


def main():
    root = tkinter.Tk()
    anakonda = Anakonda(master=root)
    anakonda.run()
    anakonda.mainloop()

if __name__ == '__main__':
    main()