import string
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_create_ad(browser):
    browser.get("http://tech-avito-intern.jumpingcrab.com/")
    
    # переменные для заполнения формы
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    price = 100
    description = "Новое описание"
    image = "https://www.gstatic.com/webp/gallery/4.sm.jpg"

    search_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='Поиск по объявлениям']")
    search_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Найти')]")

    # Нажать на кнопку "Создать объявление" (по тексту)
    create_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Создать')]")
    create_button.click()

    modal = browser.find_element(By.CSS_SELECTOR, "section.chakra-modal__content")

    # Заполнить поля
    title_input = modal.find_element(By.NAME, "name")
    title_input.send_keys(name)
    
    price_input = modal.find_element(By.NAME, "price")
    price_input.send_keys(price)

    description_input = modal.find_element(By.NAME, "description")
    description_input.send_keys(description)

    image_input = modal.find_element(By.NAME, "imageUrl")
    image_input.send_keys(image)
    
    # Нажать на кнопку "Сохранить" (по тексту)
    save_button = modal.find_element(By.XPATH, "//button[contains(text(), 'Сохранить')]")
    save_button.click()

    # Ожидание закрытия модального окна
    WebDriverWait(browser, 10).until(
        EC.staleness_of(modal)
    )

    search_input.send_keys(name)

    search_button.click()

    # Ждём 1 секунду после нажатия кнопки "Найти"
    time.sleep(1)

    # Находим первый элемент "a" внутри списка с классом "css-1w07v7s"
    ad_element = browser.find_element(By.CSS_SELECTOR, ".css-1w07v7s a")

    # Проверка имени
    h3_element = ad_element.find_element(By.TAG_NAME, "h4")
    assert h3_element.text == name, "Текст названия не соответствует ожидаемому"

    # Проверка ссылки
    img_element = ad_element.find_element(By.TAG_NAME, "img")
    assert img_element.get_attribute("src") == image, "Атрибут src у img не соответствует ожидаемому"

    # Проверка цены
    pr_element = ad_element.find_element(By.CSS_SELECTOR, "div.css-1n43xc7")
    assert pr_element.text == "%d₽" % price, "Текст названия не соответствует ожидаемому"
