# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:38:48 2020

@author: acubelic
"""
try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter
import tkinter.colorchooser as colorchooser
import math
import numpy as np
import ImagePoints
import pdb


class createCanvas:
    """Create canvas object."""

    @ staticmethod
    def get_scale_factor(x):
        """Return scale factor"""
        k = 1e4
        N0 = 2
        b = -k / (1 + k / (N0 - 1))
        r = -0.1 * math.log(((N0 - 1) / k) * (k / (1 - b) - 1))
        scaleFactor = k / (1 + (k / (N0 - 1))*math.e**(-r * x)) + b
        return scaleFactor

    def __init__(self, rootWindow, canvasWidth, canvasHeight, bgc):
        self._rootWindow = rootWindow
        self._width = canvasWidth
        self._height = canvasHeight
        self._bgc = bgc
        self._id = tkinter.Canvas(self._rootWindow, width=self._width,
                                  height=self._height, background=self._bgc,
                                  highlightthickness=0)

        # to keep track of mouse movement [x, y]
        self._origin = [self._width / 2, self._height / 2]
        self._lastOrigin = [self._width / 2, self._height / 2]
        self._lastViewTipVar = 0
        self._dragData = [0, 0]
        self._zoomData = 25
        self._scaleFactor = self.get_scale_factor(self._zoomData)
        # add bindings for clicking, dragging and releasing canvas
        self._id.bind("<ButtonPress-1>", self.drag_start)
        self._id.bind("<ButtonRelease-1>", self.drag_stop)
        self._id.bind("<B1-Motion>", self.drag)
        self._id.bind("<MouseWheel>", self.mouse_wheel)
        self._id.bind("<Configure>", self.resize_canvas)

    def resize_canvas(self, _):
        # Data from old origin
        xOldOrigin, yOldOrigin = self._origin
        xRatio = xOldOrigin / self._width
        yRatio = yOldOrigin / self._height
        # Updating new origin
        self._width = self._id.winfo_width()
        self._height = self._id.winfo_height()
        self._origin = [self._width * xRatio, self._height * yRatio]

    def update_colour(self, bgc):
        self._bgc = bgc
        self._id.configure(background=bgc)

    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        self._dragData[0] = event.x
        self._dragData[1] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._dragData[0] = 0
        self._dragData[1] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        translateFactor = 50  # Used to scale the amount of movement
        deltaX = (event.x - self._dragData[0]) / translateFactor
        deltaY = (event.y - self._dragData[1]) / translateFactor

        # record the new translation value
        if self._lastViewTipVar != 1:
            self._origin[0] += deltaX
            self._origin[1] += deltaY

    def mouse_wheel(self, event):
        """Handle scrolling of mouse wheel."""
        zoomFactor = 2
        zoomDelta = event.delta / 120 * zoomFactor

        if zoomDelta < 0:
            if self._zoomData == 0 or self._zoomData < abs(zoomDelta):
                self._zoomData == 0
            else:
                self._zoomData += zoomDelta
        else:
            self._zoomData += zoomDelta
        self._scaleFactor = self.get_scale_factor(self._zoomData)

    def centre(self):
        """Centres image."""
        self._origin = [self._width / 2, self._height / 2]


class drawAxes:
    """Draw the x-axis and y-axis within the provided canvas object."""

    def __init__(self, canvasObject, axesColour):
        """Draw the x and y axes on the canvas."""
        self._canvas = canvasObject
        xPos, yPos = self._canvas._origin

        self._xid = canvasObject._id.create_line(0, yPos,
                                                 self._canvas._width, yPos,
                                                 fill=axesColour)

        self._yid = canvasObject._id.create_line(xPos, 0,
                                                 xPos, self._canvas._height,
                                                 fill=axesColour)

    def move_axes(self):
        xPos, yPos = self._canvas._origin

        self._canvas._id.coords(self._xid, 0, yPos, self._canvas._width, yPos)
        self._canvas._id.coords(self._yid, xPos, 0, xPos, self._canvas._height)

    def update_colour(self, axesColour):
        self._canvas._id.itemconfig(self._xid, fill=axesColour)
        self._canvas._id.itemconfig(self._yid, fill=axesColour)


class drawCircle:
    """Draw a circle object at with radius r at (xo, yo)."""

    @ staticmethod
    def point_on_circle(circleInstance, t):
        """Calculate cartesian co-ordinate of point on radius of circle.

        Will convert polar coordinates to cartesian coordinates and return
        (x, y) position of point for entered value of
        theta and self.radius.

        Omega is the angular frequency: w = 2*pi*f*
        Indicates how many cycles per second. Assumed equal to 1 i.e. f = 1/2pi
        phi specifies the start position of oscillatory cycle.
        """
        # Calculate co-ordinate on circle cirumference
        xCentre, yCentre = circleInstance._centrePoint
        Cn = circleInstance._Cn
        n = circleInstance._n

        complexPoint = Cn * math.e**(n * 2 * math.pi * 1j * t)
        xTemp = complexPoint.real
        yTemp = complexPoint.imag

        # Add off-set to account for circle origin
        xEdge = xTemp + xCentre
        yEdge = yTemp + yCentre

        return (xEdge, yEdge)

    @ staticmethod
    def get_coords(centrePoint, edgePoint, scaleFactor, origin):

        # Determine radius
        xc, yc = centrePoint
        xe, ye = edgePoint
        x0, y0 = origin
        radius = ((xc - xe)**2 + (yc - ye)**2)**0.5

        # Determine coordinates for Tkinter to draw circle from
        x1 = ((xc - radius) * scaleFactor + x0)
        y1 = ((yc - radius) * scaleFactor + y0)
        x2 = ((xc + radius) * scaleFactor + x0)
        y2 = ((yc + radius) * scaleFactor + y0)

        return (x1, y1, x2, y2)

    def __init__(self, canvasObject, centrePoint, Cn, n,
                 colour, startTime):
        self._canvas = canvasObject
        self._centrePoint = centrePoint
        self._Cn = Cn
        self._n = n
        self._colour = colour
        self._edgePoint = self.point_on_circle(self, startTime)

        coords = self.get_coords(self._centrePoint, self._edgePoint,
                                 self._canvas._scaleFactor,
                                 self._canvas._origin)

        self._id = canvasObject._id.create_oval(*coords, outline=self._colour)

    def move_circle(self, newCentrePoint, t):
        """Move circle to new coordinate."""
        self._centrePoint = newCentrePoint
        self._edgePoint = self.point_on_circle(self, t)

        coords = self.get_coords(self._centrePoint, self._edgePoint,
                                 self._canvas._scaleFactor,
                                 self._canvas._origin)

        self._canvas._id.coords(self._id, *coords)

    def update_colour(self, circleColour):
        self._colour = circleColour
        self._canvas._id.itemconfig(self._id, outline=self._colour)


class drawWiper:
    """Draw a line from centre of circle to point on circumference.

    or a circle of origin (xo, yo) and radius r, will draw a line from
    the centre to a pre-determined point on the circle's circumference.
    """
    @ staticmethod
    def get_coords(centrePoint, edgePoint, originPoint, scaleFactor):
        xc, yc = centrePoint
        xe, ye = edgePoint
        x0, y0 = originPoint

        x1 = xc * scaleFactor + x0
        y1 = yc * scaleFactor + y0
        x2 = xe * scaleFactor + x0
        y2 = ye * scaleFactor + y0

        return x1, y1, x2, y2

    def __init__(self, canvasObject, circle, colour):

        self._canvas = canvasObject
        self._circle = circle
        self._colour = colour

        coords = self.get_coords(self._circle._centrePoint,
                                 self._circle._edgePoint,
                                 self._canvas._origin,
                                 self._canvas._scaleFactor)

        self._id = self._canvas._id.create_line(*coords,
                                                fill=self._colour)

    def move_wiper(self):
        """Updates position of wiper."""
        coords = self.get_coords(self._circle._centrePoint,
                                 self._circle._edgePoint,
                                 self._canvas._origin,
                                 self._canvas._scaleFactor)

        self._canvas._id.coords(self._id, *coords)

    def update_colour(self, vectorColour):
        self._colour = vectorColour
        self._canvas._id.itemconfig(self._id, fill=self._colour)


class drawArrowHead:
    """Create arrow tip for end of wiper."""

    @ staticmethod
    def get_triangle_coords(centrePoint, edgePoint):
        """Get coordiantes of isosceles triangle.

        Centre_coords is a tuple of the coordinates of the circle's
        centre (x0, y0).
        edge_coords is a tuple of the coordinates of point on circle's
        circumference.

        Uses ratio formula and midpoint formula.
        Let point R(x, y) be the point which divides PQ in the ratio K1:K2
        i.e. PR:PQ = K1:K2
        """
        # Determines ratio of line length : arrow height
        ratioLineArrow = 0.175
        ratioHeightBase = 1.2

        # Using mid-point formula to get midpoint of base of triangle
        xc, yc = centrePoint
        xe, ye = edgePoint
        x3 = (xe + (ratioLineArrow * xc)) / (1 + ratioLineArrow)
        y3 = (ye + (ratioLineArrow * yc)) / (1 + ratioLineArrow)

        # Defining isoscles triangle base and height
        height = math.sqrt((x3 - xe)**2 + (y3 - ye)**2)
        base = height / math.sqrt(ratioHeightBase**2 - 0.25)

        # Defining slope and intercept of base which is perpendicular to height
        # Wiper is horizontal
        if abs(ye - yc) < 1e-2:
            x4 = x5 = x3
            y4 = y3 + 0.5 * base
            y5 = y3 - 0.5 * base
        # Wiper is vertical
        elif abs(xe - xc) < 1e-2:
            y5 = y4 = y3
            x4 = x3 + 0.5 * base
            x5 = x3 - 0.5 * base
        # Wiper has defined slope
        else:
            perpSlope = -(xe - xc) / (ye - yc)
            perpIntercept = y3 - (perpSlope * x3)

            # Defining quadratic equation terms x = (-b +- sqrt(b**2 - 4ac))/2a
            a = 1 + perpSlope**2
            b = 2 * (perpSlope * (perpIntercept - y3) - x3)
            c = x3**2 + (perpIntercept - y3)**2 - (base / 2)**2
            d = math.sqrt(b**2 - 4 * a * c)  # d = sqrt(b**2 - 4ac)

            x4 = (-b + d) / (2 * a)
            x5 = (-b - d) / (2 * a)
            y4 = perpSlope * x4 + perpIntercept
            y5 = perpSlope * x5 + perpIntercept

        return (xe, ye, x4, y4, x5, y5)

    @ staticmethod
    def get_coords(trianglePoints, scaleFactor, originPoint):
        xe, ye, x4, y4, x5, y5 = trianglePoints
        x0, y0 = originPoint

        x1 = xe * scaleFactor + x0
        y1 = ye * scaleFactor + y0
        x2 = x4 * scaleFactor + x0
        y2 = y4 * scaleFactor + y0
        x3 = x5 * scaleFactor + x0
        y3 = y5 * scaleFactor + y0

        return (x1, y1, x2, y2, x3, y3)

    def __init__(self, canvasObject, wiper, colour):
        self._canvas = canvasObject
        self._wiper = wiper
        self._colour = colour

        trianglePoints = self.get_triangle_coords(self._wiper._circle.
                                                  _centrePoint,
                                                  self._wiper._circle.
                                                  _edgePoint)

        coords = self.get_coords(trianglePoints, self._canvas._scaleFactor,
                                 self._canvas._origin)

        self._id = self._canvas._id.create_polygon(coords,
                                                   fill=self._colour)

    def move_arrow(self):
        """Re-positions arrow head for updated positions."""
        trianglePoints = self.get_triangle_coords(self._wiper._circle.
                                                  _centrePoint,
                                                  self._wiper._circle.
                                                  _edgePoint)

        coords = self.get_coords(trianglePoints, self._canvas._scaleFactor,
                                 self._canvas._origin)

        self._canvas._id.coords(self._id, coords)

    def update_colour(self, vectorColour):
        self._colour = vectorColour
        self._canvas._id.itemconfig(self._id, fill=vectorColour)


class drawImageOutline:
    """Contains methods and variables required for image outline."""

    @ staticmethod
    def get_image_outline(CnList, nPoints):
        """Self contained function to get image outline for n circles."""
        def get_n_value(i):
            """Return n value of ith element in Cn List."""
            sign = (-1)**(i + 1)
            value = i // 2 + abs(math.sin(i * math.pi / 2))
            n = int(sign * value)
            return n

        def get_edge_point(t, n, Cn):
            complexPoint = Cn * math.e**(n * 2 * math.pi * 1j * t)
            return complexPoint

        def get_image_point(t, CnList):
            point = 0
            for i, Cn in enumerate(CnList):
                n = get_n_value(i)
                point += get_edge_point(t, n, Cn)
            return point

        # Keep a list of t's
        outline = []
        for t in np.arange(0, 1, 1 / nPoints):
            #outline.append((t, get_image_point(t, CnList)))
            outline.append(get_image_point(t, CnList))
        return outline

    @ staticmethod
    def get_point(CnList, t):
        def get_n_value(i):
            """Return n value of ith element in Cn List."""
            sign = (-1)**(i + 1)
            value = i // 2 + abs(math.sin(i * math.pi / 2))
            n = int(sign * value)
            return n

        def get_edge_point(t, n, Cn):
            complexPoint = Cn * math.e**(n * 2 * math.pi * 1j * t)
            return complexPoint

        point = 0
        for i, Cn in enumerate(CnList):
            n = get_n_value(i)
            point += get_edge_point(t, n, Cn)
        return point

    @ staticmethod
    def get_coords(outline, scaleFactor, origin):
        coords = []
        x0, y0 = origin

        for complexPoint in outline:
            xPoint = complexPoint.real * scaleFactor + x0
            yPoint = complexPoint.imag * scaleFactor + y0
            coords += [xPoint, yPoint]

        return coords

    def __init__(self, CnList, canvasObject, colour, nPoints):
        self._canvasObject = canvasObject
        self._colour = colour
        self._nPoints = nPoints
        self._outline = self.get_image_outline(CnList, self._nPoints)
        # TODO: Add glowing fading image outline
        # define a time list. Fading trail will consist of n points of the
        # image outline. Multiple catogries of points where sum is n points.
        # Each catogory will have different colour to simulate glowing fading
        # trail. From the last edgePoint, find closest time point and make that
        # point the start of the glowing outline.
        # self._time = np.arange(0, 1, 1 / nPoints)
        # Need to re-work outline to have different segments with different colours

        coords = self. get_coords(self._outline,
                                  self._canvasObject._scaleFactor,
                                  self._canvasObject._origin)
        # fill='' to make transparent
        self._id = self._canvasObject._id.create_polygon(coords,
                                                         outline=self._colour,
                                                         fill='')

    def move_outline(self):
        coords = self.get_coords(self._outline,
                                 self._canvasObject._scaleFactor,
                                 self._canvasObject._origin)

        self._canvasObject._id.coords(self._id, coords)

    def update_colour(self, imageOutlineColour):
        self._colour = imageOutlineColour
        self._canvasObject._id.itemconfig(self._id, outline=imageOutlineColour)

    def update_outline(self, CnList, nPoints):
        self._outline = self.get_image_outline(CnList, nPoints)
        coords = self. get_coords(self._outline,
                                  self._canvasObject._scaleFactor,
                                  self._canvasObject._origin)
        self._canvasObject._id.coords(self._id, coords)


class ObjectHandler:
    """Contains methods and variable required to handle all objects."""

    def __init__(self, mainWindow, canvasWidth, windowHeight):
        """Initiate variables"""
        # Start, stop, clear switches
        self._startSwitch = False  # TODO: Correct initial value
        self._clearSwitch = False
        self._time = 0
        self._refreshRate = 17  # 17 ms = 1s / 60 frames
        self._timeFactor = 10
        self._dt = self._refreshRate / 1000 / self._timeFactor
        self._viewTipVar = None
        self._GlowingOutlineVar = None
        self._nColours = 8
        self._nPoints = 1000
        self._timeList = np.arange(0, 1, 1 / self._nPoints)
        self._glowingTrailSwitch = False

        # Initialising variables
        self._circles = []
        self._wipers = []
        self._arrows = []
        self._canvasAxes = None
        self._imageOutline = None

        # Default Settings
        # GUI Colours
        self._nCircles = 5
        self._maxArrows = 50
        self._canvasColour = '#000000'  # 19232D'
        self._axesColour = '#6c7070'
        self._circleColour1 = '#56929c'
        self._circleColour2 = '#3e585c'
        self._vectorColour = '#ffffff'
        self._imageColour = '#FFDE6F'
        self._transitionColours = None

        # Drawing Objects / Variables
        self._imageCanvas = createCanvas(mainWindow, canvasWidth,
                                         windowHeight, self._canvasColour)
        self._imageCanvas._id.pack(side='left', fill="both", expand=True)
        self._CnList = ImagePoints.get_constants(ImagePoints.LMALogo,
                                                 invertY=False)

    @ staticmethod
    def get_n_value(i):
        """Return n value of ith element in Cn List."""
        sign = (-1)**(i + 1)
        value = i // 2 + abs(math.sin(i * math.pi / 2))
        n = int(sign * value)

        return n

    # TODO: Fix methods
    def create_objects(self, end, centrePoint=(0, 0), start=0, startTime=0):
        """Create additional objects when required."""

        for n in range(start, end):
            if n % 2 == 0:
                circleColour = self._circleColour1
            else:
                circleColour = self._circleColour2

            self._circles.append(drawCircle(self._imageCanvas, centrePoint,
                                            self._CnList[n],
                                            self.get_n_value(n),
                                            circleColour,
                                            startTime))
            centrePoint = self._circles[n]._edgePoint

        for circle in self._circles[start:]:
            self._wipers.append(drawWiper(self._imageCanvas, circle,
                                          self._vectorColour))

        for wiper in self._wipers[start:self._maxArrows]:
            self._arrows.append(drawArrowHead(self._imageCanvas, wiper,
                                              self._vectorColour))

    def initiate_objects(self):
        """Initiate objects to be drawn on canvas."""

        self._canvasAxes = drawAxes(self._imageCanvas, self._axesColour)
        self._imageOutline = drawImageOutline(self._CnList[:self._nCircles],
                                              self._imageCanvas,
                                              self._imageColour,
                                              self._nPoints)
        self._transitionColours = self.get_transition_colours()

        # TODO: Fix me
        if self._clearSwitch:
            # _nCircles is the number of circles to draw
            self.create_objects(self._nCircles)
        else:
            self.create_objects(self._nCircles)

    def start(self):
        """Start animation."""
        if self._clearSwitch:
            self.initiate_objects()
            self._clearSwitch = False
        if not self._startSwitch:
            self._startSwitch = True
            # self.animate()

    def stop(self):
        """Stop animation."""
        self._startSwitch = False

    def clear(self):
        """Clear canvas and stop animation."""
        self._clearSwitch = True
        self.stop()
        self._imageCanvas._id.delete('all')
        # TODO: Fix me
        # circles.clear()
        # wipers.clear()
        # arrows.clear()

    def move_objects(self):
        """Moves all objects."""
        circleStartOrigin = (0, 0)
        newViewTipVar = self._viewTipVar.get()
        lastViewTipVar = self._imageCanvas._lastViewTipVar

        # Switches stored origins when check box ticked/un-ticked
        if newViewTipVar != lastViewTipVar:
            newOrigin = self._imageCanvas._lastOrigin
            lastOrigin = self._imageCanvas._origin
            self._imageCanvas._lastOrigin = lastOrigin
            self._imageCanvas._origin = newOrigin
            self._imageCanvas._lastViewTipVar = newViewTipVar

        if self._viewTipVar.get():

            scaleFactor = self._imageCanvas._scaleFactor
            height = self._imageCanvas._height
            width = self._imageCanvas._width
            xEdge, yEdge = self._circles[-1]._edgePoint

            xNew = width / 2 - xEdge * scaleFactor
            yNew = height / 2 - yEdge * scaleFactor
            self._imageCanvas._origin = [xNew, yNew]

        for circle in self._circles:
            circle.move_circle(circleStartOrigin, self._time)
            circleStartOrigin = circle._edgePoint

        for wiper in self._wipers:
            wiper.move_wiper()

        for arrow in self._arrows:
            arrow.move_arrow()

        self._canvasAxes.move_axes()
        self._imageOutline.move_outline()

    # TODO
    # def set_trail_colours(self):
    #     index = np.argmin(np.abs(timeList - currentTime))

    def animate(self):
        """Refresh positions of all objects."""
        if self._startSwitch:
            self._time = (self._time + self._dt) % 1  # Cn[t] where t in (0,1)
        if self._glowingTrailSwitch:
            pass
        self.move_objects()
        self._imageCanvas._id.after(self._refreshRate, self.animate)

    def change_NoCircles(self, sliderValue):
        """Change the number of cirlces used to draw the image."""
        numberCircles = int(sliderValue)
        oldNoCircles = len(self._circles)

        if numberCircles > oldNoCircles:
            xInit, yInit = self._circles[-1]._edgePoint
            self._nCircles = numberCircles
            self.create_objects(numberCircles, centrePoint=(xInit, yInit),
                                start=oldNoCircles, startTime=self._time)
            self._imageOutline.update_outline(self._CnList[:self._nCircles],
                                              self._nPoints)

        if numberCircles < oldNoCircles:
            for circle in self._circles[numberCircles:]:
                self._imageCanvas._id.delete(circle._id)
            self._circles = self._circles[:numberCircles]

            for wiper in self._wipers[numberCircles:]:
                self._imageCanvas._id.delete(wiper._id)
            self._wipers = self._wipers[:numberCircles]

            for arrow in self._arrows[numberCircles:]:
                self._imageCanvas._id.delete(arrow._id)
            self._arrows = self._arrows[:numberCircles]

            # Updating image outline
            self._nCircles = numberCircles
            self._imageOutline.update_outline(self._CnList[:self._nCircles],
                                              self._nPoints)

    def change_speedFactor(self, slider_value):
        """Change the time increment."""
        self._timeFactor = float(slider_value)
        self._dt = self._refreshRate / 1000 / self._timeFactor

    def update_bgc(self, instanceID, colour=None):
        """Update canvas background colour."""
        if colour is None:
            canvasColour = colorchooser.askcolor()[-1]
        else:
            canvasColour = colour
        self._imageCanvas.update_colour(canvasColour)
        instanceID.config(background=canvasColour)
        self.get_transition_colours()

    def update_axes_colour(self, instanceID, colour=None):
        if colour is None:
            axesColour = colorchooser.askcolor()[-1]
        else:
            axesColour = colour
        self._canvasAxes.update_colour(axesColour)
        instanceID.config(background=axesColour)

    def update_circle1_colour(self, instanceID, colour=None):
        if colour is None:
            circleColour = colorchooser.askcolor()[-1]
        else:
            circleColour = colour
        for index, circle in enumerate(self._circles):
            if index % 2 == 0:
                circle.update_colour(circleColour)
        instanceID.config(background=circleColour)

    def update_circle2_colour(self, instanceID, colour=None):
        if colour is None:
            circleColour = colorchooser.askcolor()[-1]
        else:
            circleColour = colour
        for index, circle in enumerate(self._circles):
            if index % 2 != 0:
                circle.update_colour(circleColour)
        instanceID.config(background=circleColour)

    def update_vector_colour(self, instanceID, colour=None):
        if colour is None:
            vectorColour = colorchooser.askcolor()[-1]
        else:
            vectorColour = colour
        for wiper in self._wipers:
            wiper.update_colour(vectorColour)
        for arrow in self._arrows:
            arrow.update_colour(vectorColour)
        instanceID.config(background=vectorColour)

    def update_outline_colour(self, instanceID, colour=None):
        if colour is None:
            imageOutlineColour = colorchooser.askcolor()[-1]
        else:
            imageOutlineColour = colour
        self._imageOutline.update_colour(imageOutlineColour)
        instanceID.config(background=imageOutlineColour)
        self.get_transition_colours()

    def hex_to_rgb(self, hex_colour):
        return tuple(int(hex_colour.strip('#')[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb_colour):
        return '#{:02x}{:02x}{:02x}'.format(*rgb_colour)

    def get_transition_colours(self):
        # unpacking tuples
        x1, y1, z1 = self.hex_to_rgb(self._imageOutline._colour)
        x2, y2, z2 = self.hex_to_rgb(self._imageCanvas._bgc)

        # The number of points required
        dt = 1 / (self._nColours - 1)

        rgbColours = tuple(
            (int((1 - t) * x1 + t * x2),
             int((1 - t) * y1 + t * y2),
             int((1 - t) * z1 + t * z2)
             ) for t in np.arange(0, 1 + dt, dt))

        transitionColours = tuple(self.rgb_to_hex(rgbColour)
                                  for rgbColour in rgbColours)

        # Tuple colour starts at image outline colour and ends in canvas colour
        self._transitionColours = transitionColours


if __name__ == '__main__':
    cnList = ImagePoints.get_constants(ImagePoints.musicNote)
    Outline = drawImageOutline.get_image_outline(cnList, 1000)
