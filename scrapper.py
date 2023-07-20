from bs4 import BeautifulSoup
import cv2
import requests
import numpy as np

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


def download_image(image_url):
    response = requests.get(image_url)
    image_data = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    return image


def extract_fish_data(soup):
    fish_data = []
    fish_section = soup.find('div', class_='oknoNT', style='width: 650px; display:inline-block')
    if fish_section:
        fish_table = fish_section.find('table', class_='table-basar fishes-table')
        if fish_table:
            rows = fish_table.find_all('tr')[1:]
            for row in rows:
                columns = row.find_all('td')
                img = columns[0].find('img')['src']
                image = download_image('https://nosapki.com' + img)
                name = columns[1].text.strip()
                chance = columns[2].text.strip()
                price = columns[3].text.strip()
                exp_profession = columns[4].text.strip()
                fish_data.append({'Image': image, 'Name': name, 'Chance': chance, 'Price': price, 'EXP Profession': exp_profession})

    return fish_data


def extract_box_data(soup):
    box_data = []

    box_section = soup.find('div', class_='oknoNT', style='width: 550px; margin-left: 20px; display:inline-block')
    if box_section:
        box_table = box_section.find('table', class_='table-basar')
        if box_table:
            rows = box_table.find_all('tr')[1:]
            for row in rows:
                columns = row.find_all('td')
                img = columns[0].find('img')['src']
                image = download_image('https://nosapki.com' + img)
                name = columns[1].text.strip()
                chance = columns[2].text.strip()
                box_data.append({'Image': image, 'Name': name, 'Chance': chance})

    return box_data


fishery_id = input("Type your fishery ID: ")
url = 'https://nosapki.com/en/side_jobs/fisheries/'+fishery_id
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


fish_data = extract_fish_data(soup)
box_data = extract_box_data(soup)

test = 'test_bigres.png'
template = cv2.imread(test)
print('start compare')
for fish in fish_data:
    is_present, match_loc = is_animation_present(fish['Image'], template)
    if is_present:
        print(fish['Name'])

for box in box_data:
    pass
