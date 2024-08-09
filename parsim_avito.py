# Импортируем модули
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализируем браузер
driver = webdriver.Chrome()

# В отдельной переменной указываем сайт, который будем просматривать
url = "https://www.divan.ru/krasnodar/category/matrasy"

# Открываем веб-страницу
driver.get(url)

# Ожидаем, пока элементы с матрасами будут видны на странице
try:
    # Устанавливаем явное ожидание до 10 секунд
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ui-GPFV8'))
    )
except Exception as e:
    print(f"Произошла ошибка при ожидании элементов: {e}")
    driver.quit()
    exit()

# Находим все карточки с матрасами
mattresses = driver.find_elements(By.CLASS_NAME, 'WdR1o')

# Выводим количество найденных элементов на экран для проверки
print(f"Найдено элементов: {len(mattresses)}")

# Создаём список, в который потом всё будет сохраняться
parsed_data = []

# Перебираем коллекцию карточек матрасов
for mattress in mattresses:
    try:
        # Находим название матраса
        product_name = mattress.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text
        # Находим цену матраса
        price = mattress.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute('content')
        # Находим ссылку на матрас с помощью атрибута 'href'
        link = mattress.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

        # Формируем полный URL, если ссылка относительная
        if not link.startswith('http'):
            link = 'https://www.divan.ru' + link

        # Вносим найденную информацию в список
        parsed_data.append([product_name, price, link])

    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

# Закрываем браузер
driver.quit()

# Прописываем открытие нового файла, задаём ему название и форматирование
with open("mattresses.csv", 'w', newline='', encoding='utf-8') as file:
    # Используем модуль csv и настраиваем запись данных в виде таблицы
    writer = csv.writer(file)
    # Создаём первый ряд
    writer.writerow(['Название матраса', 'Цена', 'Ссылка на матрас'])
    # Записываем остальные данные
    writer.writerows(parsed_data)

print("Парсинг завершен. Данные сохранены в mattresses.csv.")

