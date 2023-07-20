import cv2
import requests
import numpy as np


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
