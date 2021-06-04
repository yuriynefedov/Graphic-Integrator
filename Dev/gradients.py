from random import choice


PRESETS = {"Relaxing red": ((255, 251, 213), (178, 10, 44)),
           "Evening sunshine": ((185, 43, 39), (21, 101, 192)),
           "Velvet sun": ((225, 238, 195), (240, 80, 83)),
           "Ali": ((225, 75, 31), (31, 221, 255)),
           "Purple bliss": ((54, 0, 51), (11, 135, 147)),
           "Blue raspberry": ((136, 228, 255), (0, 131, 176)),
           "Citrus peel": ((253, 200, 48), (243, 115, 53)),
           "Yoda": ((255, 0, 153), (73, 50, 64)),
           "Blue to red": ((25, 0, 230), (210, 0, 45))}


def discrete_gradient(colors=None, steps=100):
    if colors is None:
        chosen_gradient = choice(list(PRESETS.keys()))
        start_color, end_color = PRESETS[chosen_gradient]
        print("Chosen gradient:", chosen_gradient)
    elif isinstance(colors, str):
        start_color, end_color = PRESETS[colors]
        print("Chosen gradient:", colors)
    else:
        start_color, end_color = colors
    red_delta = (end_color[0] - start_color[0]) / steps
    green_delta = (end_color[1] - start_color[1]) / steps
    blue_delta = (end_color[2] - start_color[2]) / steps
    gradient = []
    current_red, current_green, current_blue = start_color
    for step in range(steps):
        if step == 0:
            gradient.append(start_color)
        else:
            current_red = current_red + red_delta
            current_green = current_green + green_delta
            current_blue = current_blue + blue_delta
            gradient.append((int(current_red), int(current_green), int(current_blue)))
    return gradient


if __name__ == "__main__":
    grad = discrete_gradient((0, 0, 255), (255, 0, 0), 100)
    print(grad)
    print(len(grad))