from tkinter import *


class Cell:
    def __init__(self, master, x, y, size):
        self.master = master
        self.x = x
        self.y = y
        self.size = size
        self.fill = False

    def switch(self):
        self.fill = not self.fill

    def draw(self):
        if self.master != None:
            fill = 'black'
            outline = 'black'
            if not self.fill:
                fill = 'white'
                outline = 'black'

            xmin = self.x * self.size
            xmax = xmin + self.size
            ymin = self.y * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(
                xmin, ymin, xmax, ymax, fill=fill, outline=outline)


class CellGrid(Canvas):
    def __init__(self, master, row, column, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width=column * cellSize,
                        height=row * cellSize, *args, **kwargs)
        self.cellSize = cellSize
        self.grid = []
        for i in range(row):
            line = []
            for j in range(column):
                line.append(Cell(self, j, i, cellSize))
            self.grid.append(line)

        self.switched = []

        self.bind("<Button-1>", self.handleMouseClick)
        self.bind("<B1-Motion>", self.handleMouseMotion)

        self.draw()

    def handleMouseClick(self, event):
        row, column = self.eventCoord(event)
        cell = self.grid[row][column]
        cell.switch()
        cell.draw()
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self.eventCoord(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell.switch()
            cell.draw()
            self.switched.append(cell)

    def eventCoord(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()


if __name__ == "__main__":
    app = Tk()
    app.title('shortPath')
    app.geometry('1250x900')
    app.resizable(None)

    grid = CellGrid(app, 50, 50, 18)
    grid.pack()
    grid.place(x=0, y=0)

    btn = Button(app, text='Find')
    btn.place(x=910, y=0)
    btn.config(height='3', width='17', font="_ 19 bold")

    app.mainloop()
