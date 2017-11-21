# -*- coding: utf-8 -*-

from tkinter import *

import numpy as np
from PIL import ImageTk, Image
from tkinter import filedialog
from scipy import misc


def weightedAverage(pixel):
    return 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]


def toGrey(image):
    grey = np.zeros((image.shape[0], image.shape[1]))  # init 2D numpy array
    # get row number

    for rownum in range(len(image)):
        for colnum in range(len(image[rownum])):
            grey[rownum][colnum] = weightedAverage(image[rownum][colnum])
    return grey
def invertCol(image):
    inverse = np.zeros((image.shape[0], image.shape[1]))  # init 2D numpy array

    for rownum in range(len(image)):
        for colnum in range(len(image[rownum])):
            inverse[rownum][colnum] = (0xFFFFFF - image[rownum][colnum])
            # inverse[rownum][colnum] = np.invert(image[rownum][colnum])

    return inverse
okno = Tk()

okno.geometry('800x800')
canvas = Canvas(okno,width=799,height=799)
canvas.pack()
path = filedialog.askopenfile()

image = Image.open(path.name)

im = misc.fromimage(image)



imgr = toGrey(im)
imgr = np.rot90(imgr,-1)
img = misc.toimage(imgr)
imga = ImageTk.PhotoImage(img)
imageS = canvas.create_image(200,200,image=imga)

inim = np.invert(im)
img1 = misc.toimage(inim)
imga1 = ImageTk.PhotoImage(img1)
imageA = canvas.create_image(500,200,image=imga1)

okno.mainloop()


