# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:20:14 2020

@author: acubelic
"""

try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter

import FourierClasses
from functools import partial

# Drawing on Tkinter
# creating main window
mainWindow = tkinter.Tk()
mainWindow.title('Fourier Series')
windowWidth, windowHeight,  = 1200, 650
mainWindow.geometry('{}x{}'.format(windowWidth, windowHeight))
mainWindow.wm_attributes('-topmost', 1)
mainWindow.minsize(windowWidth, windowHeight)
mainWindow.update()

# Option Menu
FONT1 = 'Helvetica 14'
FONT2 = 'Helvetica 11'

menuFrame = tkinter.Frame(mainWindow, relief='flat', padx=20, borderwidth=1)
menuFrame.pack(side='left', fill='y')
menuFrame.update()

# Drawing menu options
label = tkinter.Label(menuFrame, text="Options Menu",
                      font='Helvetica 20 bold')
label.grid(row=0, column=0)  # inserts the label

# Drawing Buttons
buttonFrame = tkinter.Frame(menuFrame)
buttonFrame.grid(row=1, column=0)

startButton = tkinter.Button(buttonFrame, text='Start', font=FONT1)
startButton.grid(row=0, column=0, sticky='we')

stopButton = tkinter.Button(buttonFrame, text='Stop', font=FONT1)
stopButton.grid(row=0, column=1, sticky='we')

clearButton = tkinter.Button(buttonFrame, text='Clear', font=FONT1)
clearButton.grid(row=0, column=2, sticky='we')

centreButton = tkinter.Button(buttonFrame, text='Centre', font=FONT1)
centreButton.grid(row=1, column=1, sticky='we')

resetButton = tkinter.Button(buttonFrame, text='Reset', font=FONT1)
resetButton.grid(row=1, column=2, sticky='we')
mainWindow.update()

# Sliders
scaleFrame = tkinter.LabelFrame(menuFrame, text='Drawing Options',
                                font=FONT1)
scaleFrame.grid(row=2, column=0, sticky='we')


circleSlider = tkinter.Scale(scaleFrame, from_=1, to=301,
                             orient='horizontal',
                             length=menuFrame.winfo_width())
circleSlider.set(5)  # TODO: replace 5 with variable 'nCircles'
circleSlider.grid(row=0, column=0, sticky='we')
circleSliderLabel = tkinter.Label(scaleFrame, text='Number of Circles',
                                  font=FONT2)
circleSliderLabel.grid(row=1, column=0, sticky='we')

SpeedSlider = tkinter.Scale(scaleFrame, from_=1, to=100,
                            digits=2, resolution=1,
                            orient='horizontal',
                            length=menuFrame.winfo_width())
SpeedSlider.set(10)
SpeedSlider.grid(row=2, column=0, sticky='we')
SpeedSliderLabel = tkinter.Label(scaleFrame, text='Speed Factor',
                                 font=FONT2)
SpeedSliderLabel.grid(row=3, column=0, columnspan=3, sticky='w')

# Check Buttons
viewTipVar = tkinter.IntVar()
viewTip = tkinter.Checkbutton(scaleFrame, text="Centre camera on drawing tip",
                              variable=viewTipVar)
viewTip.grid(row=4, column=0, sticky='w')

glowingOutlineVar = tkinter.IntVar()
glowingOutline = tkinter.Checkbutton(scaleFrame,
                                     text="Enable glowing/fading" +
                                     " image outline",
                                     variable=glowingOutlineVar)
glowingOutline.grid(row=5, column=0, sticky='w')

# Colour Options
colourOptionsFrame = tkinter.LabelFrame(menuFrame, text='Colour Options',
                                        font=FONT1)
colourOptionsFrame.grid(row=3, column=0, sticky='we')

# Background Colour
bcgColourButton = tkinter.Button(colourOptionsFrame, background='black',
                                 width=2, height=1)
bcgColourButton.grid(row=0, column=0, sticky='we')
bcgColorLabel = tkinter.Label(colourOptionsFrame, text='Background',
                              font=FONT2)
bcgColorLabel.grid(row=0, column=1, sticky='w')

# Axes Colour
axesColourButton = tkinter.Button(colourOptionsFrame, background='#6c7070')
axesColourButton.grid(row=1, column=0, sticky='we')
axesColourLabel = tkinter.Label(colourOptionsFrame, text='Axes', font=FONT2)
axesColourLabel.grid(row=1, column=1, sticky='w')

# Circles 1 Colour
circleColourButton1 = tkinter.Button(colourOptionsFrame, background='#56929c')
circleColourButton1.grid(row=2, column=0, sticky='we')
circleColourLabel1 = tkinter.Label(colourOptionsFrame, text='Circles 1',
                                   font=FONT2)
circleColourLabel1.grid(row=2, column=1, sticky='w')

# Circles 2 Colour
circleColourButton2 = tkinter.Button(colourOptionsFrame, background='#3e585c')
circleColourButton2.grid(row=3, column=0, sticky='we')
circleColourLabel2 = tkinter.Label(colourOptionsFrame, text='Circles 2',
                                   font=FONT2)
circleColourLabel2.grid(row=3, column=1, sticky='w')

# Vector Colour
vectorColourButton = tkinter.Button(colourOptionsFrame, background='white')
vectorColourButton.grid(row=4, column=0, sticky='we')
vectorColourLabel = tkinter.Label(colourOptionsFrame, text='Vectors',
                                  font=FONT2)
vectorColourLabel.grid(row=4, column=1, sticky='w')

# Outline Colour
OutlineColourButton = tkinter.Button(colourOptionsFrame, background='#FFDE6F')
OutlineColourButton.grid(row=5, column=0, sticky='we')
OutlineColourLabel = tkinter.Label(colourOptionsFrame, text='Image Outline',
                                   font=FONT2)
OutlineColourLabel.grid(row=5, column=1, sticky='w')

menuFrame.rowconfigure((1, 2, 3, 4), pad=10)

# Drawing Canvas
mainWindow.update()
menuWidth = menuFrame.winfo_width()
canvasWidth = (windowWidth - menuWidth)

# imageCanvas = FourierClasses.createCanvas(mainWindow, canvasWidth,
#                                           windowHeight,'#19232D')
# TODO: replace colour with variable
# imageCanvas._id.pack(side='left', fill="both", expand=True)
# imageCanvas.id.bind("<Configure>", canvas_sizeChange) # TODO: updated function

mainWindow.update()
Objects = FourierClasses.ObjectHandler(mainWindow, canvasWidth, windowHeight)
Objects.initiate_objects()

# Assign button commands
startButton.configure(command=Objects.start)
stopButton.configure(command=Objects.stop)
clearButton.configure(command=Objects.clear)
centreButton.configure(command=Objects._imageCanvas.centre)

# Assign Slide bar commands
SpeedSlider.configure(command=Objects.change_speedFactor)
circleSlider.configure(command=Objects.change_NoCircles)

# Assign Check commands
Objects._viewTipVar = viewTipVar

# Assign colour button commands
bcgColourButton.configure(command=partial(Objects.update_bgc, bcgColourButton))
axesColourButton.configure(command=partial(Objects.update_axes_colour,
                                           axesColourButton))
circleColourButton1.configure(command=partial(Objects.update_circle1_colour,
                                              circleColourButton1))
circleColourButton2.configure(command=partial(Objects.update_circle2_colour,
                                              circleColourButton2))
vectorColourButton.configure(command=partial(Objects.update_vector_colour,
                                             vectorColourButton))
OutlineColourButton.configure(command=partial(Objects.update_outline_colour,
                                              OutlineColourButton))

Objects.animate()
mainWindow.mainloop()
