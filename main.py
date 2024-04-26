import csv
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def kirpy_find_element(driver, path, method=By.XPATH, timeout=0.1):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((method, path)))

def get_chromedriver(block_image=True, background=False, lang="de"):
    service = Service()
    chrome_options = webdriver.ChromeOptions()
    if block_image:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
    if background:
        chrome_options.add_argument("--headless")
    if lang:
        chrome_options.add_argument(f"--lang={lang}")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

driver = get_chromedriver(background=False, block_image=True)
fields = ['name', 'category', 'address', 'website', "plus_code", "comment_avg", "comment_count"]

with open("input.txt", "r", encoding="utf-8") as in_file:
    in_data = in_file.readlines()
    in_file.close()

with open("data.csv", 'w', encoding="utf-8") as csvfile:
    csvfile.write("")
    csvfile.close()

counter = 0
mylist = []
start = datetime.datetime.now()
print("Başlangıç:", start)
for place_link in in_data:
    try:
        place_link.replace("\n", "")

        driver.get(place_link)

        name = str(kirpy_find_element(driver,
                                  "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1",
                                  timeout=2).text).replace('"', "")
        category = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button").text
        address = str(driver.find_element(By.XPATH, "//button[@data-item-id='address']").text).split("\n")[1]
        # print("name:", name)
        # print("category:", category)
        # print("address:", address)

        try:
            website = str(driver.find_element(By.XPATH, "//a[@data-item-id='authority']").text).split("\n")[1]
            # print("website:", website)
        except:
            website = None
            # print("website: None")

        try:
            plus_code = str(
                driver.find_element(By.XPATH, "//button[@data-item-id='oloc']").get_attribute("aria-label")).replace(
                "Plus Code: ", "")

            # print("plus_code:", plus_code)
        except:
            plus_code = None
            # print("plus_code: None")

        try:
            phone_number = str(driver.find_elements(By.XPATH, "//button[@data-tooltip='Telefonnummer kopieren']")[0].text).split("\n")[1]
            # print("phone_number:", phone_number)
        except:
            phone_number = None
            # print("phone_number: None")

        try:
            comment_avg = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]").text
            # print("comment_avg:", comment_avg)
        except:
            comment_avg = None
            # print("comment_avg: None")

        try:
            comment_count = str(driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span").text).replace("(", "").replace(")", "")
            # print("comment_count:", comment_count)
        except:
            comment_count = None
            # print("comment_count: None")

        mylist.append({
            "name": name,
            "category":category,
            "address": address,
            "website": website,
            "plus_code": plus_code,
            "comment_avg": comment_avg,
            "comment_count": comment_count})
    except:
        # print("Hata verdi:", place_link)
        pass
    counter += 1
    if counter > 1000:
        with open("data.csv", 'a', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(mylist)
            csvfile.close()
            mylist = []
            counter = 0

print("Bitiş:", datetime.datetime.now())
print("Geçen süre:", (datetime.datetime.now() - start).total_seconds()/60, "dakika")

if len(mylist) > 0:
    with open("data.csv", 'a', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(mylist)
        csvfile.close()




