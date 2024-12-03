import json
import time
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from classes import OPCard


def setup_driver():
    """Set up the Selenium WebDriver."""
    driver = webdriver.Edge()
    return driver

def parse_card(card: Tag):
    name_element = card.find(class_='cardName')
    number_element = card.select_one('.infoCol span:nth-of-type(1)')
    image_url_element = card.select_one('.frontCol img').get("data-src")
    power_element = card.find(class_='power')
    effect_element = card.find(class_='text')
    counter_element = card.find(class_='counter')
    set_element = card.find(class_='getInfo')
    color_element = card.find(class_='color')
    rarity_element = card.select_one('.infoCol span:nth-of-type(2)')
    card_type_element = card.select_one('.infoCol span:nth-of-type(3)')
    feature_element = card.find(class_='feature')
    attribute_element = card.select_one('.attribute img')
    cost_element = card.find(class_='cost')

    name = name_element.text.strip() if name_element else None
    number = number_element.text if number_element else None
    image_url = image_url_element if image_url_element else None
    power = power_element.text if power_element else None
    effect = effect_element.decode_contents().strip() if effect_element else None
    counter = counter_element.text.strip() if counter_element else None
    set_info = set_element.text.strip() if set_element else None
    color = color_element.decode_contents().strip() if color_element else None
    rarity = rarity_element.text.strip() if rarity_element else None
    card_type = card_type_element.text.strip() if rarity_element else None
    feature = feature_element.text.strip() if feature_element else None
    attribute = attribute_element.get('alt').strip() if attribute_element else None
    cost = cost_element.text.strip() if cost_element else None

    alternate = True if "_p" in image_url else False
    
    try:
        trigger = card.find(class_="trigger").decode_contents()
    except:
        trigger = ""


    card_instance = OPCard(
        name=name,
        ID=number,
        imageUrl=image_url.replace("..", "https://asia-hk.onepiece-cardgame.com/"),
        alternate=alternate,  
        power=power,
        effect=effect,
        counter=counter,
        card_set=set_info,
        color=color,  # Assuming you have color ID or object
        rarity=rarity,  # Assuming you have rarity ID or object
        card_type=card_type,
        feature=feature,  # Set feature appropriately if applicable
        attribute=attribute,
        cost=cost,
        trigger = trigger
    )

    return card_instance

def store_json(cards:list[OPCard], file_name):
    opcard_json_list = [card.to_json() for card in cards]

    with open(f"cards/{file_name}.json", 'w', encoding="utf-8") as json_file:
        json.dump(opcard_json_list, json_file, indent=2, ensure_ascii=False)
       

def get_page(driver, cards_switch=None):
    pack_name = driver.find_element(By.CSS_SELECTOR, ".selModalClose:nth-of-type(5)").get_attribute("innerText")
    # OP-10 is 5th elements
    if cards_switch:
        driver.find_element(By.CLASS_NAME, "selModalButton").click()
        driver.find_element(By.CSS_SELECTOR, f".selModalClose:nth-of-type({cards_switch})").click()
        pack_name = driver.find_element(By.CSS_SELECTOR, f".selModalClose:nth-of-type({cards_switch})").get_attribute("innerText")
        driver.find_element(By.CSS_SELECTOR, ".submitBtn input").submit()
        
        time.sleep(10)
    """Click different set filter to get the card list"""
    html = BeautifulSoup(driver.page_source, 'lxml')
    return html, pack_name

def main(baseURL):
    driver = setup_driver()
    driver.get(baseURL)
    driver.implicitly_wait(10)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    

    # Display index and the corresponding card set
    all_ops = driver.find_elements(By.CSS_SELECTOR, "li.selModalClose")
    for _index in range(len(all_ops)):
        print(f"{_index+1}:\t{all_ops[_index].get_attribute("innerText")} ")
    
    for card_switch in range(4,34):
        html, pack_name = get_page(driver, card_switch)
        cards = html.find_all("dl", class_="modalCol")
        cards = [parse_card(card) for card in cards]
        store_json(cards, pack_name)


if __name__ == "__main__":
    main("https://asia-hk.onepiece-cardgame.com/cardlist")
