import argparse
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Daftar User Agent acak
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36"
]

# Fungsi untuk mendapatkan user-agent acak
def get_random_user_agent():
    return random.choice(USER_AGENTS)

# Fungsi untuk memeriksa apakah halaman mengarah ke https://www.google.com/
def check_google_redirect(driver, url, payload_file):
    # Membaca payload dari file
    with open(payload_file, 'r') as file:
        payloads = file.readlines()

    for payload in payloads:
        full_url = url + payload.strip()  # Gabungkan URL dan payload

        try:
            print(f"Testing URL: {full_url}")
            driver.get(full_url)  # Coba buka halaman
            driver.set_page_load_timeout(10)  # Set timeout 10 detik

            time.sleep(8)  # Tunggu selama 8 detik

            # Mengecek apakah URL halaman yang dimuat adalah https://www.google.com/
            if driver.current_url == "https://www.google.com/":
                print(f"Success: {full_url} mengarah ke https://www.google.com/")
            else:
                print(f"Failed: {full_url} tidak mengarah ke https://www.google.com/")

        except Exception as e:
            print(f"Error saat memuat {full_url}: {str(e)}")

def setup_driver():
    # Setup Chrome dengan Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Menjalankan di background
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Driver setup
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cek apakah URL mengarah ke https://www.google.com/")
    parser.add_argument("-u", "--url", required=True, help="URL dasar untuk diuji")
    parser.add_argument("-p", "--payload", required=True, help="File teks berisi payload (URL+payload)")

    args = parser.parse_args()

    # Setup browser driver sekali
    driver = setup_driver()

    # Melakukan pengecekan
    check_google_redirect(driver, args.url, args.payload)

    # Tutup driver setelah selesai
    driver.quit()
