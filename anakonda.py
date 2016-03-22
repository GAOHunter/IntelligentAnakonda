import sys
import time
import tkinter
#from PIL import Image
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

    def display(self):
        self.gridDraw.drawSnakeHead(self.body[0], self.headPhoto, self.direction)
        self.gridDraw.drawSnakeBody(self.body[1:-1], self.bodyPhoto, self.direction)
        self.gridDraw.drawSnakeTail(self.body[-1], self.tailPhoto, self.direction)

    def move(self):

        #判断方向操作是否合理，若合理继续，不合理停止。
        direcSet = ('Up', 'Down', 'Left', 'Right')
        currentDirec = ''
        firstBodyGrid = self.body[0]
        secondBodyGrid = self.body[1]
        if firstBodyGrid[0] == secondBodyGrid[0]:
            if firstBodyGrid[1] > secondBodyGrid[1]:
                currentDirec = 'Down'
            else:
                currentDirec = 'Up'
        if firstBodyGrid[1] == secondBodyGrid[1]:
            if firstBodyGrid[0] > secondBodyGrid[0]:
                currentDirec = 'Right'
            else:
                currentDirec = 'Left'
        if direcSet.index(currentDirec) - direcSet.index(self.direction) == -1:
            return
        if direcSet.index(currentDirec) - direcSet.index(self.direction) == 1:
            return

        head = self.body[0]
        if self.direction == 'Up':
            new = (head[0], head[1]-1)
        elif self.direction == 'Down':
            new = (head[0], head[1]+1)
        elif self.direction == 'Left':
            new = (head[0]-1, head[1])
        else: new = (head[0]+1, head[1])

        if not self.food.pos == head:
            pop = self.body.pop()
            self.gridDraw.draw(pop, self.gridDraw.gridDrawColor)
        else:
            self.display_food()
            self.score += 1

        self.body.insert(0, new)

        if new not in self.avilable_gridDraw():
            self.status.reverse()
            self.gameover = True
        else:
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
        #保存移动路径
        self.path = []
        #self.master.bind("<Key>", self.key_release)
        self.snake.display()

    def bfs(self):

        headPos = self.snake.body[0]
        direc = self.snake.direction

        vis = [ [False for i in range(0, 50)] for j in range(0, 50)]
        print(vis, sep=',')

        que = [headPos]
        vis[headPos[0]][headPos[1]] = True

        while not len(que) == 0:
            headPos = que.pop(0)
            print(headPos)
            if headPos == self.snake.food.pos:
                return

            if not vis[headPos[0]+1][headPos[1]]:
                vis[headPos[0]+1][headPos[1]] = True
                que.append((headPos[0]+1, headPos[1]))

            if not vis[headPos[0]-1][headPos[1]]:
                vis[headPos[0]-1][headPos[1]] = True
                que.append((headPos[0]-1, headPos[1]))

            if not vis[headPos[0]][headPos[1]+1]:
                vis[headPos[0]][headPos[1]+1] = True
                que.append((headPos[0], headPos[1]+1))

            if not vis[headPos[0]][headPos[1]-1]:
                vis[headPos[0]][headPos[1]-1] = True
                que.append((headPos[0], headPos[1]-1))
        '''
        direc = ('Up', 'Down', 'Left', 'Right')
        for ix in range(0, 100):
            self.path.append(direc[randint(0, 3)])
        '''

    def run(self):
        if not self.snake.status[0] == 'stop' and not len(self.path) == 0:
            self.snake.direction = self.path[0]
            self.path.pop(0)
            self.snake.move()

        if self.snake.gameover == True:
            print(self.snake.body, self.snake.direction)
            message = messagebox.showinfo("Game Over", "Your Score: %d" % self.snake.score)
            if message == 'ok':
                sys.exit()

        self.after(self.snake.speed, self.run)

    def key_release(self, event):

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
    anakonda.bfs()
    anakonda.run()
    anakonda.mainloop()

if __name__ == '__main__':
    main()