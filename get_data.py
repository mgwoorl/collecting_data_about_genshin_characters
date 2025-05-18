from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

genshin_base_url = "https://genshin-info.ru"
genshin_characters_url = genshin_base_url + "/wiki/personazhi/"
driver.get(genshin_characters_url)

time.sleep(3)

genshin_soup = BeautifulSoup(driver.page_source, 'html.parser')
genshin_cards = genshin_soup.find_all('a', class_='itemcard')

print(f"Найдено карточек: {len(genshin_cards)}")

characters_data = []

for card in genshin_cards:
    try:
        char_link = card.get('href')
        if not char_link:
            continue

        driver.get(genshin_base_url + char_link)
        time.sleep(2)

        char_soup = BeautifulSoup(driver.page_source, 'html.parser')
        info = char_soup.find('div', class_='characterPromo__info')

        if not info:
            continue

        name = info.find('div', class_='characterPromo__name').text.strip()
        props = info.find_all('div', class_='characterPromo__prop')
        stars = len(props[0].find('span', class_='characterPromo__propV').find_all('i'))
        element = props[1].find('span', class_='characterPromo__propV').text.strip()
        weapon = props[2].find('span', class_='characterPromo__propV').text.strip()

        characters_data.append({
            "Имя": name,
            "Элемент": element,
            "Оружие": weapon,
            "Редкость": stars
        })

        print(f"Добавлен: {name}")

    except Exception as e:
        print("Ошибка при обработке персонажа:", e)

driver.quit()

df = pd.DataFrame(characters_data)
df.to_csv("genshin_characters.csv")
print(df.head())
