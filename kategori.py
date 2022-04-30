from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time

url = "https://www.blibli.com/promosi/bigpayday?appsWebview=true"

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--window-size=1420,1080")
opts.add_argument("--disable-gpu")
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
driver.get(f"{url}")
time.sleep(5)  # Allow 2 seconds for the web page to open
a = ActionChains(driver)

# Hover to "kategori" button
btn_kategori = driver.find_element(By.XPATH, "//*[@id='blibliApp']/div/header/div[2]/div[1]/div[2]/div")
a.move_to_element(btn_kategori).perform()
time.sleep(5)

# # =======================================================================
# # =======================================================================
# menu = driver.find_element(By.CLASS_NAME, "categories__menu-item")
# a.move_to_element(menu).perform()
# page_soup = BeautifulSoup(driver.page_source, "html.parser")
# print(page_soup)
# # =======================================================================
# # =======================================================================

# Get all kategori level1
menu = driver.find_elements(By.CLASS_NAME, "categories__menu-item")

# Hover into each of kategori level1 and scrap it
list_category = []
for x in menu:
    a.move_to_element(x).perform()
    print(x.text.strip())
    list_category.append(x.text.strip())
    time.sleep(5)
    page_soup = BeautifulSoup(driver.page_source, "html.parser")

    # Get menu content
    menu_soup = page_soup.find("div", {"class": "categories__content b-full-width"})
    level2_tag = menu_soup.find_all("div", {"class": "categories__item-block"})
    for y in level2_tag:
        level2 = y.find("div", {"class": "categories__item-heading"})
        print(f";{level2.text.strip()}")
        list_category.append(f";{level2.text.strip()}")
        level3_tag = y.find_all("div", {"class": "b-ellipsis"})
        for z in level3_tag:
            print(f";;{z.text.strip()}")
            list_category.append(f";;{z.text.strip()}")

driver.close()

# Write scraped data to a csv file (semicolon separated)
f = open(f"blibli_kategori.csv", "w+", encoding="utf-8")  # open/create file and then append some item (a+)
headers = "Level 1;Level 2;Level 3\n"
f.write(headers)
for i in range(len(list_category)):
    f.write(f"{list_category[i]}\n")
f.close()
