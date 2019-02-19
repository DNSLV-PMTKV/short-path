from PIL import Image, ImageDraw
from tkinter import Tk, Canvas, Button
from path import Point, PathFinder

WIDTH = 600
HEIGHT = 600
PIXEL = 30


class grid:
    def __init__(self, master, *argv, **kwargs):
        self.grid = Canvas(master, *argv, **kwargs)
        self.grid.pack()
        self.image = Image.new('RGB', (WIDTH, HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.startPointLoc = []
        self.endPointLoc = []

        self.gridArray = []

        self.grid.bind('<Button-2>', self._drawObstacle)
        self.grid.bind('<B2-Motion>', self._drawObstacle)
        self.grid.bind('<Button-1>', self._drawStartPoint)
        self.grid.bind('<Button-3>', self._drawEndPoint)

    def drawGrid(self):
        for x in range(PIXEL, HEIGHT, PIXEL):
            self.grid.create_line(0, x, WIDTH, x, fill="grey")
        for y in range(PIXEL, WIDTH, PIXEL):
            self.grid.create_line(y, 0, y, HEIGHT, fill="grey")

    def _drawObstacle(self, event):
        x, y = event.x // PIXEL, event.y // PIXEL
        self.grid.create_rectangle(
            x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='black')
        self.draw.rectangle(
            [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='black')

    def _drawStartPoint(self, event):
        x, y = event.x // PIXEL, event.y // PIXEL
        if not self.startPointLoc:
            self.startPointLoc.append((x, y))
            self.grid.create_rectangle(
                x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='blue')
            self.draw.rectangle(
                [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='blue')
        else:
            x1, y1 = self.startPointLoc.pop(0)
            self.grid.create_rectangle(
                x1 * PIXEL, y1 * PIXEL, x1 * PIXEL + PIXEL, y1 * PIXEL + PIXEL, fill='white', outline='gray')
            self.draw.rectangle(
                [x1 * PIXEL, y1 * PIXEL, x1 * PIXEL + PIXEL, y1 * PIXEL + PIXEL], fill='white', outline='gray')
            self.startPointLoc.append((x, y))
            self.grid.create_rectangle(
                x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='blue')
            self.draw.rectangle(
                [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='blue')

    def _drawEndPoint(self, event):
        x, y = event.x // PIXEL, event.y // PIXEL
        if not self.endPointLoc:
            self.endPointLoc.append((x, y))
            self.grid.create_rectangle(
                x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='red')
            self.draw.rectangle(
                [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='red')
        else:
            x1, y1 = self.endPointLoc.pop(0)
            self.grid.create_rectangle(
                x1 * PIXEL, y1 * PIXEL, x1 * PIXEL + PIXEL, y1 * PIXEL + PIXEL, fill='white', outline='gray')
            self.draw.rectangle(
                [x1 * PIXEL, y1 * PIXEL, x1 * PIXEL + PIXEL, y1 * PIXEL + PIXEL], fill='white', outline='gray')
            self.endPointLoc.append((x, y))
            self.grid.create_rectangle(
                x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL, fill='red')
            self.draw.rectangle(
                [x * PIXEL, y * PIXEL, x * PIXEL + PIXEL, y * PIXEL + PIXEL], fill='red')

    def cellColor(self, x, y):
        r, g, b = self.image.getpixel((x+1, y+1))
        return r, g, b

    def toArray(self):
        for x in range(0, WIDTH, PIXEL):
            self.gridArray.append([])
            for y in range(0, HEIGHT, PIXEL):
                self.gridArray[x // PIXEL].append(0)
                if(self.cellColor(x, y) == (0, 0, 255)):
                    start = [x, y]
                    self.gridArray[x // PIXEL][y // PIXEL] = 'S'
                if(self.cellColor(x, y) == (255, 0, 0)):
                    end = [x, y]
                    self.gridArray[x // PIXEL][y // PIXEL] = 'E'
                if(self.cellColor(x, y) == (0, 0, 0)):
                    self.gridArray[x // PIXEL][y // PIXEL] = '#'
        for i in self.gridArray:
            print(i)
        print(start, end)
        return self.gridArray, start, end

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
        self.grid.delete("all")
        del self.image
        del self.draw
        self.image = Image.new('RGB', (WIDTH, HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.startPointLoc = []
        self.endPointLoc = []

        self.gridArray = []
        self.drawGrid()


app = Tk()

layout = grid(app, width=WIDTH, height=HEIGHT, bg='white')
layout.drawGrid()

btn = Button(app, text='find', command=layout.drawPath)
btn.pack()

btn2 = Button(app, text='restart', command=layout.clearAll)
btn2.pack()

app.mainloop()
