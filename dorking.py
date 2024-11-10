import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# Fungsi untuk membaca URL dari file
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Mengatur argumen
parser = argparse.ArgumentParser(description="Buka URL satu per satu untuk menghindari reCAPTCHA.")
parser.add_argument('-l', '--list', type=str, required=True, help="Path ke file yang berisi daftar URL")
args = parser.parse_args()

# Membaca URL dari file
urls = read_urls_from_file(args.list)

# Inisialisasi UserAgent
ua = UserAgent()

# Mengatur opsi Chrome
options = Options()
options.add_argument("--start-maximized")

# Inisialisasi WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Daftar URL yang memenuhi syarat
valid_urls = []

for url in urls:
    try:
        # Menggunakan user agent acak
        user_agent = ua.random
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

        driver.get(url)

        # Tunggu sampai elemen yang menunjukkan bahwa halaman telah dimuat
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Cek apakah reCAPTCHA muncul
        if "recaptcha" in driver.page_source.lower():
            print("reCAPTCHA terdeteksi! Silakan selesaikan reCAPTCHA.")
            input("Tekan Enter setelah menyelesaikan reCAPTCHA...")

        # Memeriksa konten halaman
        page_source = driver.page_source.lower()
        if "tidak cocok dengan dokumen apa pun." not in page_source:
            print(f"URL {url} tidak mengandung kata 'tidak cocok dengan dokumen apa pun.'")
            valid_urls.append(url)

        # Buka tab baru untuk URL berikutnya
        driver.execute_script("window.open('');")  # Membuka tab baru
        driver.switch_to.window(driver.window_handles[-1])  # Beralih ke tab baru

    except Exception as e:
        print(f"Terjadi kesalahan saat membuka {url}: {e}")
        break  # Menghentikan loop jika terjadi kesalahan

# Menutup browser dan menampilkan URL valid
print("Semua permintaan selesai. Menutup browser...")
driver.quit()

# Menampilkan URL yang valid
for valid_url in valid_urls:
    print(valid_url)