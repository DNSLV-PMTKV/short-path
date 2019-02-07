from PIL import Image, ImageDraw
from tkinter import Tk, Canvas

WIDTH = 250
HEIGHT = 250
PIXEL = 25


app = Tk()

gridCanvas = Canvas(app, width=WIDTH, height=HEIGHT, bg='white')
gridCanvas.pack()

image = Image.new('RGB', (WIDTH, HEIGHT), 'white')
draw = ImageDraw.Draw(image)

app.mainloop()
