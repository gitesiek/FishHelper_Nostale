import cv2
import pyautogui
import numpy as np
import random
import time

nobg_template = 'nobg_template.png'
template = cv2.imread(nobg_template)
threshold = 0.8

key_to_reel_the_line = '4'
key_to_cast_the_line = '2'

base_res_x = 1280
base_res_y = 800

template_x = 135
template_y = 42

resolutions = [
    [1024, 768],  # not working
    [1280, 1024],  # not working
    [1280, 800],  # base res
    [1440, 900],  # working
    [1024, 700],  # working but slow(?)
    [1680, 1050],  # working
]


def choose_resolution():
    print("Choose your game resolution:")
    for idx, res in enumerate(resolutions):
        print(idx, res)
    user_res = input()

    return resolutions[int(user_res)]


def resize_template(user_resolution):
    new_x_scale = user_resolution[0]/base_res_x
    # new_x_scale = 0.95 # fix for res 0
    new_y_scale = user_resolution[1]/base_res_y
    print(user_resolution[0], user_resolution[1])
    print(new_x_scale, new_y_scale)
    new_x = template_x * new_x_scale
    new_y = template_y * new_y_scale
    new_dim = [int(new_x), int(new_y)]

    resized_template = cv2.resize(template, new_dim)
    print(new_dim)
    return resized_template


template = resize_template(choose_resolution())


def is_animation_present(template, screenshot):
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return True, max_loc
    else:
        return False, None


counter = 0
print("ENTER THE FISH")
while True:
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    is_present, match_loc = is_animation_present(template, screenshot)
    if is_present:
        counter += 1
        if counter >= 2:
            print("PULL OUT!")
            print(key_to_reel_the_line)
            counter = 0
            delay = random.randint(4000, 6500) / 1000
            time.sleep(delay)
            print("-------------")
            print(key_to_cast_the_line)
