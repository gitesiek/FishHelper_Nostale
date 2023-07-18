import cv2
import pyautogui
import numpy as np
import random
import time

template_path = 'template.png'
template_mori_path = 'template_mori.png'
key_to_reel_the_line = '4'
key_to_cast_the_line = '2'
threshold = 0.8


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
press2_x = 1222
press2_y = 915

press4_x = 1311
press4_y = 915


while True:
    screenshot = pyautogui.screenshot()

    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(template_mori_path)
    is_present, match_loc = is_animation_present(template, screenshot)
    if is_present:
        counter += 1
        if counter >= 1:
            delay = random.randint(50, 150) / 1000
            # time.sleep(delay)
            print("PULL OUT!")
            print(key_to_reel_the_line)
            pyautogui.typewrite('4')
            counter = 0
            delay = random.randint(4000, 6500) / 1000
            # time.sleep(delay)
            print("-------------")
            pyautogui.moveTo(press4_x, press4_y)
