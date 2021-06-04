import turtle
from math import *
import numpy as np
from pynput import keyboard
from datetime import datetime

import gradients

ZERO_POINT = (-700, 0)
ZERO_POINT_POSITIVE = (-700, -300)
X_RANGE = 1300
Y_RANGE = 300
AXES_SPEED = 100
X_AXIS_LENGTH = 1400
AXIS_COLOR = "white"
GRAPH_COLOR = "red"
BG_COLOR = "black"
AXIS_WIDTH = 2
GRAPH_WIDTH = 4
AREA_COORDS = (0, -300)
ARROW_LENGTH = 5
CURRENT_PIXELS_PER_UNIT = None
CURRENT_AREA = 0
LAST_INPUT = ""
ROUND_TO = 3
JUST_LOADED = True


def space_pressed():
    fresh_start(ZERO_POINT)
    draw_axes(ZERO_POINT, X_RANGE, Y_RANGE)


turtle.onkey(space_pressed, "Down")
turtle.colormode(255)
t = turtle.Pen()
turtle.bgcolor(BG_COLOR)
t.hideturtle()
t.color(GRAPH_COLOR)
t.pensize(GRAPH_WIDTH)


def draw_axes(zero_point, negatives=True, color="black", return_to=None):
    t.pensize(AXIS_WIDTH)
    t.speed(AXES_SPEED)
    t.color(AXIS_COLOR)
    t.up()
    t.setpos(*zero_point)
    if negatives:
        t.down()
        t.setpos(zero_point[0], zero_point[1]+Y_RANGE)
        t.setpos(t.pos()[0]-ARROW_LENGTH, t.pos()[1]-ARROW_LENGTH)
        t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
        t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
        t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
        t.up()
        t.setpos(*zero_point)
        t.down()
        t.setpos(zero_point[0], zero_point[1]-Y_RANGE)
        t.up()
        t.setpos(*zero_point)
        t.down()
        t.setpos(zero_point[0]+X_AXIS_LENGTH, zero_point[1])
        t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
        t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
        t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
        t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
        t.up()
        t.setpos(*zero_point)
    else:
        t.down()
        t.setpos(zero_point[0], zero_point[1] + Y_RANGE*2)
        t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
        t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
        t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
        t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
        t.up()
        t.setpos(*zero_point)
        t.down()
        t.setpos(zero_point[0] + X_AXIS_LENGTH, zero_point[1])
        t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
        t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
        t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
        t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
        t.up()
        t.setpos(*zero_point)
    t.color(GRAPH_COLOR)
    t.pensize(GRAPH_WIDTH)
    if return_to is not None:
        t.setpos(return_to)


def express_draw_axes(zero_point, negatives=True, color="black", return_to=None):
    t.pensize(AXIS_WIDTH)
    t.speed(AXES_SPEED)
    t.color(AXIS_COLOR)
    t.up()
    t.setpos(*zero_point)
    t.down()
    t.setpos(zero_point[0]+X_AXIS_LENGTH, zero_point[1])
    t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
    t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
    t.setpos(t.pos()[0] - ARROW_LENGTH, t.pos()[1] - ARROW_LENGTH)
    t.setpos(t.pos()[0] + ARROW_LENGTH, t.pos()[1] + ARROW_LENGTH)
    t.up()
    t.setpos(*zero_point)
    t.color(GRAPH_COLOR)
    t.pensize(GRAPH_WIDTH)
    t.setpos(*zero_point)
    if return_to is not None:
        t.setpos(*return_to)


def draw_rect(axis_point, outside_point, color="red", mind_axes=True, zero_point=ZERO_POINT):
    global CURRENT_AREA, CURRENT_PIXELS_PER_UNIT
    t.up()
    t.color(color)
    t.pencolor(color)
    t.pensize(1)
    x_start, x_end = axis_point[0], outside_point[0]
    y_start, y_end = axis_point[1], outside_point[1]
    CURRENT_AREA += (x_end - x_start) * (y_end - y_start) / (CURRENT_PIXELS_PER_UNIT**2)
    # print("CURRENT AREA:", CURRENT_AREA)
    if mind_axes:
        if outside_point[1] >= zero_point[1]:
            # outside point is above the axis
            y_start += AXIS_WIDTH
            # print("above")
        else:
            y_start -= AXIS_WIDTH
            # print("below")
    t.begin_fill()
    t.down()
    t.setpos(outside_point)
    t.setpos(x_start, y_end)
    t.setpos(x_start, y_start)
    t.setpos(x_end, y_start)
    t.setpos(outside_point)
    t.end_fill()
    t.color(GRAPH_COLOR)
    t.pensize(GRAPH_WIDTH)


def display_area(area):
    t.color(BG_COLOR)
    t.begin_fill()
    draw_rect((AREA_COORDS[0] - 120, AREA_COORDS[1] - 15), (AREA_COORDS[0] + 120, AREA_COORDS[1] + 15), "black")
    t.up()
    t.setpos(AREA_COORDS)
    t.down()
    t.write("Current estimated area: " + str(area), align="center", font=("Arial", 16, "normal"))
    t.up()
    t.color(GRAPH_COLOR)


def get_points(function, pixels_per_unit, x_interval=(0, 1), negatives=False, pixel_step=1):
    x_step = (x_interval[1] - x_interval[0]) * pixel_step / X_RANGE
    points = []
    zero_point = ZERO_POINT if negatives else ZERO_POINT_POSITIVE
    for pixel_x, x in enumerate(np.arange(x_interval[0], x_interval[1], x_step)):
        try:
            # print(pixel_x)
            # print("Function:", function)
            y = eval(function)
            # print("Y from", str(x), "is", str(y))
            graphed_x = zero_point[0] + pixel_x * pixel_step
            graphed_y = int(zero_point[1] + y*pixels_per_unit)
            # print("Graphed Y:", graphed_y)
            points.append((graphed_x+AXIS_WIDTH+GRAPH_WIDTH//2, graphed_y))
        except (ValueError, OverflowError):
            # print("Graphed Y unsuitable")
            # UNSUITABLE X / NaN
            pass
    # old_x, old_y = x, y
    # print(points)
    return points


def turtle_graph(function, x_range=X_RANGE, y_range=Y_RANGE, speed=1000, x_interval=(0, 1),
                 negatives=False, rectangles=10, grad_colors=None, pixel_step=1):
    global GRAPH_COLOR, CURRENT_PIXELS_PER_UNIT, CURRENT_AREA

    rectangles *= pixel_step

    zero_point = ZERO_POINT if negatives else ZERO_POINT_POSITIVE
    pixels_per_unit = X_RANGE / (x_interval[1] - x_interval[0])
    CURRENT_PIXELS_PER_UNIT = pixels_per_unit

    draw_axes(zero_point, negatives=negatives)
    t.speed(speed)
    graphed_points = get_points(function, pixels_per_unit, x_interval=x_interval, negatives=negatives,
                                pixel_step=pixel_step)
    print("Total points:", len(graphed_points))
    t.up()
    t.setpos(*graphed_points[0])
    t.down()

    # integration
    # print(rectangles)
    rectangle_step = x_range / rectangles
    gradient = gradients.discrete_gradient(grad_colors, rectangles // pixel_step)
    # print("Gradient length:", len(gradient))
    grad_index = 0

    start_point = graphed_points[0][0], zero_point[1]
    ind = 0
    CURRENT_AREA = 0

    while ind < len(graphed_points):
        point = graphed_points[ind]
        # print("Current point:", point)
        try:
            GRAPH_COLOR = gradient[grad_index]
        except IndexError:
            GRAPH_COLOR = gradient[-1]
        t.color(GRAPH_COLOR)
        # t.down()
        # t1 = datetime.now()
        if point[1] in range(zero_point[1]-AXIS_WIDTH//2, zero_point[1]+AXIS_WIDTH//2+1):
            t.up()
            t.setpos(*point)
            start_point = point[0], zero_point[1]
        else:
            t.setpos(*point)
            # print(datetime.now() - t1)
            # t.up()
            # print(point[0] % rectangle_step)
            # print(int((point[0]-zero_point[0])/pixel_step % rectangle_step))
            if (int((point[0]-zero_point[0])/pixel_step % rectangle_step) == 0 and point != zero_point) or point == graphed_points[-1]:
                draw_rect(start_point, point, color=GRAPH_COLOR, zero_point=zero_point)
                start_point = point[0], zero_point[1]
                # display_area(point[0])
                # print("Drew a rectangle; Grad index:", grad_index)
                grad_index += 1
                # if grad_index % 5 == 0:
                #     draw_axes(zero_point, negatives, AXIS_COLOR, return_to=point)
            #     pass
        ind += 1
        modify_title(function, x_interval, rectangles//pixel_step, CURRENT_AREA)


def fresh_start(zero_point=None):
    t.clear()
    t.up()
    if zero_point is not None:
        t.setpos(*zero_point)
    t.down()


def modify_title(func, x_interval, rectangles, current_area):
    turtle.title("f(x) = {}        interval: {}        rectangles: {}        estimated area: {}"\
                 .format(func, [round(x, ROUND_TO) for x in x_interval], rectangles, round(current_area, ROUND_TO)))


def title_error():
    turtle.title("Error! [For more info, open the Python console]")


def swift_loop(path="/Users/yuriynefedov/Library/Containers/com.yuriynefedov.\
Second-Try-Input-Interface/Data/Documents/file.txt"):
    global LAST_INPUT, JUST_LOADED
    swift_input = open(path, "r").readlines()
    # print(swift_input)
    if swift_input != LAST_INPUT and not JUST_LOADED:
        fresh_start()
        try:
            func, from_, to = swift_input[0][:-1], float(eval(swift_input[1][:-1])), float(eval(swift_input[2][:-1]))
            rectangles, pixel_step = int(swift_input[3][:-1]), int(swift_input[4])
            # print(func, from_, to)
        except IndexError:
            pass
            # file is empty, should wait it out
        try:
            turtle_graph(func, x_interval=(from_, to), rectangles=rectangles, pixel_step=pixel_step,
                         grad_colors="Blue raspberry", negatives=False)
        except BaseException as err:
            print("error!", err)
            title_error()

    LAST_INPUT = swift_input


if __name__ == "__main__":
    # t1 = datetime.now()
    # turtle.listen()
    # turtle_graph("1/x", x_interval=(0, 12), negatives=False, rectangles=1000, pixel_step=1,
    #              grad_colors="Blue to red")
    # turtle.done()
    # print("Time taken:", datetime.now() - t1)
    while True:
        swift_loop()
        JUST_LOADED = False
