import cv2
import pyautogui
import numpy as np
from bs4 import BeautifulSoup
import requests
import keyboard
import time
import datetime
import json

from game_vision import (
    choose_resolution,
    resize_template,
    calculate_aspect_ratio,
    is_animation_present
)

from scrapper import (
    extract_box_data,
    extract_fish_data,
    extract_fisheries
)

from classes import (
    Inventory,
    InventoryItem
)

#base_res_x = 1280
#base_res_y = 800
base_aspect_ratio = 1.6

rod_template = 'nobg_template.png'
itembg_template = 'nobg_item_bg.png'
template = cv2.imread(rod_template)
itembg_template = cv2.imread(itembg_template)

threshold = 0.8

key_to_reel_the_line = '4'
key_to_cast_the_line = '2'

player_inventory = Inventory()

chosen_res = choose_resolution()
template = resize_template(chosen_res, template)

MISSED_FISH = InventoryItem('Missed fish', 0, 1, 0)

counter = 0
counter_limit = 2
if calculate_aspect_ratio(chosen_res) != base_aspect_ratio:
    counter_limit = 1
    threshold = 0.75

url = 'https://nosapki.com/en/side_jobs/fisheries/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

print("List of ID's and fisheries")
fisheries = extract_fisheries(soup)
for fishery in fisheries:
    print(fishery['Index'], fishery['Name'])
fishery_id = input("Type your fishery ID: ")

url = 'https://nosapki.com/en/side_jobs/fisheries/'+fishery_id
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


fish_data = extract_fish_data(soup)
box_data = extract_box_data(soup)
data = fish_data + box_data


def find_loot(screenshot):
    for loot in data:
        is_present, match_loc = is_animation_present(loot['Image'], screenshot, 0.7)
        if is_present:
            return InventoryItem(loot['Name'], loot['Price'], 1, loot['EXP_Profession'])


def is_key_pressed(key):
    return keyboard.is_pressed(key)


print("You can start fishing")
start_time = time.time()
fishing_date = datetime.datetime.now()
while not is_key_pressed('esc'):
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
                    loot = find_loot(screenshot)
                    player_inventory.add_item(loot)
                    break
                counter += 1
                if counter == 70:
                    player_inventory.add_item(MISSED_FISH)
                    break
            print("-------------")
            print(key_to_cast_the_line)


end_time = time.time()
time_spent = end_time - start_time
time_spent = '{:.2f}'.format(time_spent)

print("Time spent on fishing:" + time_spent + " seconds")
print("Total value of fished items: " + str(player_inventory.get_total_value()))
print("You gained total: " + str(player_inventory.get_total_exp_profession()) + " profession experience ")


fishing_data = {
    "date": fishing_date.strftime('%Y-%m-%d %H:%M:%S'),
    "fish_info": player_inventory.get_items(),
    "summary_data": {
        "time_spent_seconds": time_spent,
        "total_value_of_items": player_inventory.get_total_value(),
        "total_profession_experience": player_inventory.get_total_exp_profession()
    }
}

file_path = 'fishing_data.json'
try:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    data = []

data.append(fishing_data)

with open(file_path, 'w') as json_file:
    json.dump(data, json_file)
