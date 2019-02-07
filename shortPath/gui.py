from PIL import Image, ImageDraw
from tkinter import Tk, Canvas, Button
from path import Point, PathFinder

WIDTH = 250
HEIGHT = 250
PIXEL = 25


class grid():
    def __init__(self, master, width, height, *argv, **kwargs):
        self.grid = Canvas(master, width=width, height=height, *argv, **kwargs)
        self.grid.pack()
        self.image = Image.new('RGB', (width, height), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.grid.bind('<Button-2>', self.drawObstacle)
        self.grid.bind('<B2-Motion>', self.drawObstacle)
        self.grid.bind('<Button-1>', self.drawStartPoint)
        self.grid.bind('<Button-3>', self.drawEndPoint)

    def drawGrid(self):
        for x in range(PIXEL, HEIGHT, PIXEL):
            self.grid.create_line(0, x, WIDTH, x, fill="grey")
        for y in range(PIXEL, WIDTH, PIXEL):
            self.grid.create_line(y, 0, y, HEIGHT, fill="grey")

    def drawObstacle(self, event):
        x, y = event.x // PIXEL, event.y // PIXEL
        self.grid.create_rectangle(
            x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='black')
        self.draw.rectangle(
            [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='black')

    def drawStartPoint(self, event):
        x, y = event.x // PIXEL, event.y // PIXEL
        self.grid.create_rectangle(
            x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='blue')
        self.draw.rectangle(
            [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='blue')

    def drawEndPoint(self, event):
        x, y = event.x // PIXEL, event.y // PIXEL
        self.grid.create_rectangle(
            x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='red')
        self.draw.rectangle(
            [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='red')

    def cellColor(self, x, y):
        r, g, b = self.image.getpixel((x+1, y+1))
        return r, g, b

    def toArray(self):
        arr = []
        start = []
        end = []
        for x in range(0, WIDTH, PIXEL):
            arr.append([])
            for y in range(0, HEIGHT, PIXEL):
                arr[x // PIXEL].append(0)
                if(self.cellColor(x, y) == (0, 0, 255)):
                    start = [x, y]
                if(self.cellColor(x, y) == (255, 0, 0)):
                    end = [x, y]
                if(self.cellColor(x, y) == (0, 0, 0)):
                    arr[x][y] = '#'
        return arr, start, end

    def getShortestPath(self):
        field, startXY, endXY = self.toArray()
        print(field, startXY, endXY)
        startPoint = Point(startXY[0], startXY[1])
        print(startPoint)
        endPoint = Point(endXY[0], endXY[1])
        print(endPoint)
        a = PathFinder(field)
        return a.shortest_path(startPoint, endPoint)

    def drawPath(self):
        shortesPath = list(self.getShortestPath())
        if shortesPath:
            for i in shortesPath:
                self.grid.create_rectangle(
                    i[0] * PIXEL, i[1] * PIXEL, i[0] * PIXEL + PIXEL, i[1] * PIXEL + PIXEL, fill='orange')
                self.draw.rectangle(
                    [i[0] * PIXEL, i[1] * PIXEL, i[0] * PIXEL + PIXEL, i[1] * PIXEL + PIXEL], fill='orange')


app = Tk()

layout = grid(app, width=WIDTH, height=HEIGHT, bg='white')
layout.drawGrid()
print(layout.toArray())
layout.getShortestPath()

btn = Button(app, text='find', command=layout.drawPath())
btn.pack()

app.mainloop()
