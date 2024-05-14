from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, datetime, pandas as pd

# this is a python code that scrapes data from sugarbeach website, all you need to do is to sit back and run the code while you enjoy the scraping-ride. Thank you. The code automatically installs the chrome webdriver and also set it to path. This developer deserves an applause.. lol

options = ChromeOptions()
options.headless = True
# options.add_argument("--headless=new")

start = time.time()

run_all_sites_once = False

driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

num = 0
todays_date = datetime.date.today()
tomorrow = todays_date + datetime.timedelta(days=1)

def get_room_divs():
        """
        Helper function, associated with sugar beach
        """
        room_divs = driver.find_elements(By.XPATH, "//div[@class='app_row']//div[contains(@class, 'app_col-md-12 app_col-lg-12')]")
        return room_divs

def sugar_beach():
    global num
    """
    This function scrapes sugar beach website
    """
    
    website_url = f"https://reservations.viceroyhotelsandresorts.com/?_ga=2.63980905.754880256.1697504574-1226995346.1697504574&adult=1&arrive={todays_date}&chain=1003&child=1&childages=17&currency=USD&depart={tomorrow}&hotel=22215&level=hotel&locale=en-US&rooms=1"

    driver.get(website_url)

    driver.implicitly_wait(30)

    hotel_name = driver.find_element(By.ID, "heroTitle").text
    print(f"The hotel name is {hotel_name}")

    button = driver.find_element(By.XPATH, "//div[@class='select_container select_hasValue']//button[@class='select_hiddenInput']")
    button.click()
    lis = driver.find_element(By.XPATH, "//ul[@class='select_dropdown']//li")
    lis.click()

    itr = get_room_divs()

    for di in itr:
        room_divs = get_room_divs()
        room_name = room_divs[num].find_element(By.TAG_NAME, "h2").text
        roomsize_guests = room_divs[num].find_element(By.XPATH, "//div[@class='guests-and-roomsize_item guests-and-roomsize_guests']/span").text
        roomsize_guests = roomsize_guests.split()[-1] #get roomsize
        roomsize_bed = room_divs[num].find_element(By.XPATH, "//div[@class='guests-and-roomsize_item guests-and-roomsize_bed']/span").text
        roomsize_area = room_divs[num].find_element(By.XPATH, "//div[@class='thumb-cards_price']/span").text
        roomsize_size = room_divs[num].find_element(By.XPATH, "//div[@class='guests-and-roomsize_item guests-and-roomsize_size']").text.replace(r"\nsquare feet","")
        price = room_divs[num].find_element(By.CLASS_NAME, "thumb-cards_price").text
        other_info = room_divs[num].find_elements(By.TAG_NAME, "li")
        li = [i.text for i in other_info]

        output = {
            'room_name': room_name,
            'roomsize_guests': roomsize_guests,
            'roomsize_bed': roomsize_bed,
            'roomsize_size': roomsize_size,
            'roomsize_area': roomsize_area,
            'price_per_night': price,
            'store_id': 84,
            'other_info': li,
        }
        print(output, end='\n')
        num+=1

    end = time.time()
    print(f'the time used is {end-start}s')

def grace_bay_club():
    global driver, num
    website = f"https://be.synxis.com/?_ga-ft=1bCFhE.0.0.0.0.3ZPUE9-5h0-4io-BlJ-Akmnwggi.0.0&_gl=1*1pw9ceo*_ga*MTIwMjEwNTkwMy4xNjk3NTA0NjEy*_ga_FDTY66CS39*MTY5NzcwODU5MS4yLjEuMTY5NzcwODc0NC41Ni4wLjA.&adult=1&arrive={todays_date}&chain=24447&child=0&config=leading1&currency=USD&depart={tomorrow}&hotel=6905&level=hotel&locale=en-US&roomcategory=JR%2C1BR%2C2BR%2C3BR%2C4BR%2C5BR&rooms=1&src=30&theme=leading1"
    driver.get(website)
    # btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-controls="select-dropdown-wrapper-view-results-by-room-rate"]')
    # btn.click()
    driver.implicitly_wait(30)
    itr = get_room_divs('gracebay')
    rooms = []
    hotel_name = driver.find_element(By.ID, "heroTitle").text
    for div in itr:
        room_divs = get_room_divs('gracebay')
        room_type = room_divs[num].find_element(By.XPATH, "//div[@class='thumb-cards_roomCategory']//div[@class='thumb-cards_header']//h2[@class='app_heading1']").text
        room_name = room_divs[num].find_element(By.XPATH, "//div[@class='app_col-sm-12 app_col-md-8 app_col-lg-8']//div[@class='thumb-cards_cardHeader']//h3").text
        roomsize_guest = room_divs[num].find_element(By.XPATH, "//div[@class='guests-and-roomsize_item guests-and-roomsize_guests']//span").text
        roomsize_bed = room_divs[num].find_element(By.XPATH, "//div[@class='guests-and-roomsize_item guests-and-roomsize_bed']//span").text
        beachEscape_price = room_divs[num].find_element(By.XPATH, "//div[@class='thumb-cards_priceContainer']//ins").text
        standardRate_price = room_divs[num].find_element(By.XPATH, "//div[@class='thumb-cards_price']//span").text
        roomsize_size = room_divs[num].find_element(By.XPATH, "//div[@class='guests-and-roomsize_item guests-and-roomsize_size']").text.replace("\nsquare feet", "")
        print(room_type, room_name, roomsize_guest, roomsize_bed, roomsize_size, beachEscape_price, standardRate_price)

        output = {
            'hotel_name': hotel_name,
            'room_type': room_type,
            'no_of_rooms': 1,
            'rooms': [{
                'room_name': room_name,
                'roomsize_guest': roomsize_guest,
                'roomsize_bed': roomsize_bed,
                'roomsize_size': roomsize_size,
                'beachEscape_price': beachEscape_price,
                'standardRate_price': standardRate_price,
            }]
        }
        print(output)
        num+=1



# def nizuc():
#     global num, driver
#     website = f"https://be.synxis.com/?adult=2&arrive={todays_date}&chain=10237&child=0&currency=USD&depart={tomorrow}&hotel=58283&level=hotel&locale=en-US&rooms=1"
#     driver.get(website)
#     itr = get_room_divs()
#     for div in itr:
#         room_div = get_room_divs()[num]
#         room_name = room_div.find_element(By.XPATH, "//h2[@class='app_heading1']").text
#         print(room_name)
#         num+=1


# # nizuc()
# # grace_bay_club()
# sugar_beach()
