import cv2
import pyautogui
import numpy as np
from bs4 import BeautifulSoup
import requests

from game_vision import (
    choose_resolution,
    resize_template,
    calculate_aspect_ratio,
    is_animation_present
)

from scrapper import (
    extract_box_data,
    extract_fish_data
)

base_res_x = 1280
base_res_y = 800
base_aspect_ratio = 1.6

rod_template = 'nobg_template.png'
itembg_template = 'nobg_item_bg.png'
template = cv2.imread(rod_template)
itembg_template = cv2.imread(itembg_template)

threshold = 0.8

key_to_reel_the_line = '4'
key_to_cast_the_line = '2'


chosen_res = choose_resolution()
template = resize_template(chosen_res, template)


counter = 0
counter_limit = 2
if calculate_aspect_ratio(chosen_res) != base_aspect_ratio:
    counter_limit = 1
    threshold = 0.75


fishery_id = input("Type your fishery ID: ")
url = 'https://nosapki.com/en/side_jobs/fisheries/'+fishery_id
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


fish_data = extract_fish_data(soup)
box_data = extract_box_data(soup)
data = fish_data + box_data


def findLoot(screenshot):
    for loot in data:
        is_present, match_loc = is_animation_present(loot['Image'], screenshot, 0.7)
        if is_present:
            return loot['Name']


print("ENTER THE FISH")
while True:
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    is_present, match_loc = is_animation_present(template, screenshot, threshold)
    if is_present:
        counter += 1
        if counter >= counter_limit:
            print("PULL OUT!")
            print(key_to_reel_the_line)
            counter = 0
            while True:
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                is_present, match_loc = is_animation_present(itembg_template, screenshot, 0.8)
                if is_present:
                    loot = findLoot(screenshot)
                    print(loot)
                    break
                counter += 1
                if counter == 70:
                    break
            # add to eq
            print("-------------")
            print(key_to_cast_the_line)
