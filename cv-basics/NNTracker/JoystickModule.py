import pygame
from time import sleep

# this module uses pygame to get
# value from controller
# Using this lib, the whole program is not interupted

pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()
buttons = {'s':0, 'x': 0, 'o': 0, 't': 0,
            'L1': 0, 'R1': 0, 'L2': 0, 'R2': 0,
            'share': 0, 'options': 0,
            'axis1': 0., 'axis2': 0., 'axis3:': 0, 'axis4': 0.
        }
axiss = [0., 0., 0., 0., 0., 0.]

def getCurrentJSValue(name=''):
    global buttons

    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION: #analog sticks
            axiss[event.axis] = round(event.value, 2)
        elif event.type == pygame.JOYBUTTONDOWN: #button pressed, set button value to 1
            for x, (key, val) in enumerate(buttons.items()):
                if x < 10:
                    if controller.get_button(x): buttons[key] = 1
        elif event.type == pygame.JOYBUTTONUP: # button released, set button value back to 0
            for x, (key, val) in enumerate(buttons.items()):
                if x < 10:
                    if event.button == x: buttons[key] = 0
    buttons['axis1'], buttons['axis2'], buttons['axis3'], buttons['axis4'] = [axiss[0], axiss[1], axiss[3], axiss[4]]
    if name == '':
        return buttons
    else:
        return buttons[name]

def main():
    print(getCurrentJSValue())
    sleep(0.05)

def jsVal():
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            print(event.axis)
            print(round(event.value,2))

if __name__ == '__main__':
    while True:
        main()


