from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# get
url = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(url)
html_doc = response.text

# bs object
soup = BeautifulSoup(html_doc, 'html.parser')

# Scrape data with bs4
addresses = [addr.text.strip() for addr in soup.find_all('address', {'data-test': 'property-card-addr'})]
prices = [price.text.strip() for price in soup.find_all('span', {'data-test': 'property-card-price'})]
links = [link.get('href') for link in soup.find_all('a', {'data-test': 'property-card-link'})]

# Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://forms.gle/7fdEmSZSvyQbu6Sy6")  # Ganti dengan URL Google Form Anda
time.sleep(2)

# funtion click & fill form
def fill_col(xpath, data):
    try:
        # Menunggu hingga kolom input dapat diklik
        col = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        col.click()  # Klik kolom input
        col.send_keys(data)  # Isi data ke kolom input
        print(f"Berhasil mengisi: {data}")
    except Exception as e:
        print(f"Gagal mengisi kolom: {e}")

# Data yang ingin diinput


# Contoh XPath kolom Google Form
xpath_address = '(//input[@class="whsOnd zHQkBf"])[1]'
xpath_price = '(//input[@class="whsOnd zHQkBf"])[2]'
xpath_link = '(//input[@class="whsOnd zHQkBf"])[3]'
xpath_submit = '//div[@role="button" and contains(@class, "uArJ5e")]'
xpath_another_response = '//a[contains(text(), "Kirim jawaban lain")]'

# filling form
for i in range(len(addresses)):
    print(f"Memasukkan data baris {i+1}:")
    fill_col(xpath_address, addresses[i])
    fill_col(xpath_price, prices[i])
    fill_col(xpath_link, links[i])

    # Submit button click
    try:
        tombol_submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_submit))
        )
        tombol_submit.click()
        print("Berhasil submit form!")
        time.sleep(2)  # Tunggu sebelum lanjut ke form berikutnya
    except Exception as e:
        print(f"Gagal submit form: {e}")
        continue  # Lanjut ke data berikutnya jika gagal submit

    # Klik tombol 'Kirim jawaban lain'
    try:
        another_response = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_another_response))
        )
        another_response.click()
        print("Melanjutkan ke form berikutnya.")
        time.sleep(2)  # Tunggu sebelum mulai mengisi data baru
    except Exception as e:
        print(f"Gagal klik 'Kirim jawaban lain': {e}")
        break  # Hentikan jika tidak bisa melanjutkan ke form berikutnya
