from PIL import Image, ImageDraw
from tkinter import Tk, Canvas, Button, Label
from path import Point, PathFinder

WIDTH = 300
HEIGHT = 300
PIXEL = 30


class grid:
    def __init__(self, master, width, height, *argv, **kwargs):
        self.grid = Canvas(master, width=width, height=height, *argv, **kwargs)
        self.grid.pack()
        self.image = Image.new('RGB', (width, height), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.hasStart = False
        self.hasEnd = False

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
        if not self.hasStart:
            self.grid.create_rectangle(
                x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='blue')
            self.draw.rectangle(
                [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='blue')
            self.hasStart = True

    def drawEndPoint(self, event):
        x, y = event.x // PIXEL, event.y // PIXEL
        if not self.hasEnd:
            self.grid.create_rectangle(
                x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='red')
            self.draw.rectangle(
                [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='red')
            self.hasEnd = True

    def cellColor(self, x, y):
        r, g, b = self.image.getpixel((x+1, y+1))
        return r, g, b

    def toArray(self):
        arr = []
        for x in range(0, WIDTH, PIXEL):
            arr.append([])
            for y in range(0, HEIGHT, PIXEL):
                arr[x // PIXEL].append(0)
                if(self.cellColor(x, y) == (0, 0, 255)):
                    start = [x, y]
                if(self.cellColor(x, y) == (255, 0, 0)):
                    end = [x, y]
                if(self.cellColor(x, y) == (0, 0, 0)):
                    arr[x // PIXEL][y // PIXEL] = '#'
        print(arr, start, end)
        return arr, start, end

    def getShortestPath(self):
        field, startXY, endXY = self.toArray()
        if startXY and endXY:
            startPoint = Point(startXY[0] // PIXEL, startXY[1] // PIXEL)
            endPoint = Point(endXY[0] // PIXEL, endXY[1] // PIXEL)
            a = PathFinder(field)
            return a.shortest_path(startPoint, endPoint)
        else:
            return None

    def drawPath(self):
        shortesPath = self.getShortestPath()
        if shortesPath:
            for i in shortesPath:
                self.grid.create_rectangle(
                    i.x * PIXEL, i.y * PIXEL, i.x * PIXEL + PIXEL, i.y * PIXEL + PIXEL, fill='orange')
                self.draw.rectangle(
                    [i.x * PIXEL, i.y * PIXEL, i.x * PIXEL + PIXEL, i.y * PIXEL + PIXEL], fill='orange')

    def clearAll(self):
        self.grid.delete('all')
        self.drawGrid()
        self.hasStart = False
        self.hasEnd = False


app = Tk()

layout = grid(app, width=WIDTH, height=HEIGHT, bg='white')
layout.drawGrid()

btn = Button(app, text='find', command=layout.drawPath)
btn.pack()

btn2 = Button(app, text='restart', command=layout.clearAll)
btn2.pack()

app.mainloop()
