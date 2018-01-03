# -*- coding: utf-8 -*-

from tkinter import *

import numpy as np
from PIL import ImageTk, Image
from tkinter import filedialog


def weightedAverage(pixel):
    return 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]


def toGrey(img, canvas):
    grey = np.zeros((img.shape[0], img.shape[1]))
    global func
    func = (toGrey,0)
    for rownum in range(len(img)):
        for colnum in range(len(img[rownum])):
            grey[rownum][colnum] = weightedAverage(img[rownum][colnum])
    showImage(grey, canvas)
    return grey


def invertCol(img, canvas):

    global func
    func = (invertCol,0)
    inverse = img
    inverse = np.invert(inverse)
    showImage(inverse, canvas)
    return inverse


def rotate(img, canvas, deg):
    global func
    func = (rotate,deg)
    tmp = img
    tmp = np.rot90(tmp, deg)
    showImage(tmp, canvas)
    return tmp


def highlight(img, canvas):

    global func
    func = (highlight,0)
    tmp = np.array(img).copy()

    w, h, c = img.shape

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            for z in range(c):
                col = (
                    + 9 * img[x, y, z]
                    - img[x - 1, y, z]
                    - img[x + 1, y, z]
                    - img[x, y + 1, z]
                    - img[x, y - 1, z]
                    - img[x - 1, y + 1, z]
                    - img[x - 1, y - 1, z]
                    - img[x + 1, y - 1, z]
                    - img[x + 1, y + 1, z])

                if col < 0:
                    col = 0

                if col > 255:
                    col = 255

                tmp[x, y, z] = col

    showImage(tmp, canvas)
    return tmp


def mirrorX(img, canvas):

    global func
    func = (mirrorX,0)
    tmp = img
    tmp = tmp[::-1]
    showImage(tmp, canvas)
    return tmp


def mirrorY(img, canvas):
    global func
    func = (mirrorY, 0)
    tmp = img
    tmp = tmp[:, ::-1]
    showImage(tmp, canvas)
    return tmp


def dark(img, canvas):
    global func
    func = (dark, 0)
    tmp = img
    tmp[...] = tmp[...] * (1 - 0.25)
    showImage(tmp, canvas)
    return tmp


def light(img, canvas):
    global func
    func = (light, 0)
    tmp = img
    tmp[...] = tmp[...] + (256 - tmp[...]) * 0.25
    showImage(tmp, canvas)
    return tmp


def showImage(img, canvas):
    global tmpa
    tmpa = ImageTk.PhotoImage(Image.fromarray(img))
    imgs = canvas.delete("all")
    imgs = canvas.create_image(0 + img.shape[1] // 2, 0 + img.shape[0] // 2, image=tmpa)


def delC(canvas):
    canvas.delete("all")


def getExt(path):
    it = 0
    for i in reversed(path):
        it += 1
        if i == '.':
            return path[len(path) - it + 1:len(path)]


def getFileame(path):
    it = 0
    for i in reversed(path):
        it += 1
        if i == '\\' or i == '/':
            return path[len(path) - it + 1:len(path) - (len(getExt(path)) + 1)]


def resizeImage(image):
    tmp = image
    size = tmp.size
    if size[0] > size[1]:
        while size[0] > 800:
            size = size[0] // 2, size[1] // 2
        return size
    else:
        while size[1] > 600:
            size = size[0] // 2, size[1] // 2
        return size


def extractPath(path):
    it = 0
    for i in reversed(path):
        it += 1
        if i == '\\' or i == '/':
            return path[:len(path) - it + 1]


def save(img,  path, canvas):
    if func[1] != 0:
        img = func[0](img=img, canvas=canvas, deg=func[1])
    else:
        img = func[0](img=img, canvas=canvas)
    tmp = Image.fromarray(img)
    tmp = tmp.convert('RGB')
    ext = getExt(path)
    if ext == "jpg":
        ext = "JPEG"
    tmp.save(extractPath(path) + getFileame(path) + "_changed." + getExt(path), ext)
    canvas.delete("all")


okno = Tk()
okno.geometry('800x800')
okno.title("Semestrální Práce : zpracování obrazu")
canvas = Canvas(okno, width=799, height=600)
canvas.place(height=600,width=799)

path = filedialog.askopenfile()

image = Image.open(path.name)
tmpim = image

final = np.array(image)
tmpim.thumbnail(resizeImage(tmpim), Image.ANTIALIAS)
im = np.array(tmpim)

b = Button(master=okno, text='Rotate 90 deg', command=lambda: rotate(im, canvas, 3))
b.place(height=50,width=100, x=0,y=600)
b = Button(master=okno, text='Rotate 180 deg', command=lambda: rotate(im, canvas, 2))
b.place(height=50,width=100, x=100,y=600)
b = Button(master=okno, text='Rotate 270 deg', command=lambda: rotate(im, canvas, 1))
b.place(height=50,width=100, x=200,y=600)
b = Button(master=okno, text='Mirror on X', command=lambda: mirrorX(im, canvas))
b.place(height=50,width=100, x=300,y=600)
b = Button(master=okno, text='Mirror on Y', command=lambda: mirrorY(im, canvas))
b.place(height=50,width=100, x=400,y=600)

b = Button(master=okno, text='To greyscale', command=lambda: toGrey(im, canvas))
b.place(height=50,width=100, x=0,y=650)
b = Button(master=okno, text='Inverse Colors', command=lambda: invertCol(im, canvas))
b.place(height=50,width=100, x=100,y=650)
b = Button(master=okno, text='Highlight edges', command=lambda: highlight(im, canvas))
b.place(height=50,width=100, x=200,y=650)
b = Button(master=okno, text='Darken', command=lambda: dark(im, canvas))
b.place(height=50,width=100, x=300,y=650)
b = Button(master=okno, text='Lighten', command=lambda: light(im, canvas))
b.place(height=50,width=100, x=400,y=650)

b = Button(master=okno, text='SAVE', command=lambda: save(final, path.name, canvas))
b.place(height=50,width=100, x=100,y=750)
b = Button(master=okno, text='DEFAULT', command=lambda: showImage(im, canvas))
b.place(height=50,width=100, x=0,y=750)

showImage(im, canvas)

okno.mainloop()
