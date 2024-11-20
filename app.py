from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = Driver(uc=True)

url = "https://www.inmuebles24.com/inmuebles-en-venta-en-ciudad-de-mexico.html"
driver.uc_open_with_reconnect(url, 4)

WebDriverWait(driver, 15).until(
    EC.invisibility_of_element_located((By.ID, "captcha"))
)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@data-qa="POSTING_CARD_PRICE"]'))
)

cards = driver.find_elements(By.XPATH, '//div[@data-id]')

for index, card in enumerate(cards):
    card_id = card.get_attribute("data-id")
    price = card.find_element(By.XPATH, './/*[@data-qa="POSTING_CARD_PRICE"]').text
    location = card.find_element(By.XPATH, './/*[@data-qa="POSTING_CARD_LOCATION"]').text
    description = card.find_element(By.XPATH, './/*[@data-qa="POSTING_CARD_DESCRIPTION"]').text

    print(f"Card ID: {card_id}")
    print(f"Price: {price}")
    print(f"Location: {location}")
    print(f"Description: {description}")

    detail_link = card.find_element(By.XPATH, './/a').get_attribute("href")

    driver.execute_script(f"window.open('{detail_link}', '_blank');")

    driver.switch_to.window(driver.window_handles[-1])

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nf-container"))
        )

        additional_details = driver.find_elements(By.CLASS_NAME, "label")
        print("Additional Details:")
        for detail in additional_details:
            print(detail.text)

    except Exception as e:
        print(f"Failed to scrape details for Card ID {card_id}: {e}")

    driver.close()

    driver.switch_to.window(driver.window_handles[0])
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-id]'))
    )

    cards = driver.find_elements(By.XPATH, '//div[@data-id]')

    print("-" * 50)

driver.quit()
