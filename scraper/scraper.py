import time
import random
import argparse
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

# Fungsi untuk login ke GitHub
def login_to_github(driver):
    driver.get("https://github.com/login")
    input("Login ke akun GitHub, kemudian tekan Enter di terminal untuk melanjutkan...")

# Fungsi untuk mengambil page source dari URL tertentu dan menyimpannya ke file
def fetch_page_source(driver, url, output_file):
    driver.get(url)
    time.sleep(random.uniform(3, 6))  # Tidur acak antara 3 hingga 6 detik
    page_source = driver.page_source
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(page_source + "\n" + "="*80 + "\n")  # Pisahkan setiap page source dengan garis
    return page_source

# Fungsi untuk menghasilkan URL berdasarkan batch dan query
def generate_urls(query, batch):
    urls = []
    for i in range(1, 6):  # Loop untuk halaman 1 hingga 5
        url = batch.format(query=query, number=i)
        urls.append(url)
    return urls

# Fungsi untuk setup WebDriver dengan random user-agent
def setup_driver():
    ua = UserAgent()
    user_agent = ua.random
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")  # Menambahkan User-Agent acak

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Fungsi untuk menjalankan perintah shell setelah selesai
def run_post_scraping_commands(query):
    # Menyusun command yang telah direvisi
    command = f"python3 grep.py -k {query} && rm -rf output.txt && sed -i 's/.*/\\L&/' {query}.txt && sort -f {query}.txt | uniq -i > temp.txt && mv temp.txt {query}.txt"
    
    # Menjalankan command shell
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Perintah setelah scraping berhasil dijalankan untuk query: {query}")
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat menjalankan perintah shell: {e}")

# Fungsi utama untuk menjalankan scraping
def main():
    parser = argparse.ArgumentParser(description="Scraper GitHub")
    parser.add_argument("-k", "--query", required=True, help="Query untuk digunakan dalam URL dan nama file output")
    args = parser.parse_args()
    
    query = args.query
    output_file = "output.txt"  # Nama file output selalu output.txt
    
    driver = setup_driver()

    try:
        # Langkah 1: Login ke GitHub
        login_to_github(driver)
        
        batches = [
            "https://github.com/search?q=%2F%28%3Fi%29%28{query}%5Ba-z%5D%2B%29%2F&type=code&p={number}",
            "https://github.com/search?q=%2F%28%3Fi%29%28{query}%5Ba-z0-9%5D*%5Cd%5Ba-z0-9%5D*%29%2F&type=code&p={number}",
            "https://github.com/search?q=%2F%28%3Fi%29%28{query}%5Ba-z0-9-%5D*-%5Ba-z0-9-%5D%2B%29%2F&type=code&p={number}",
            "https://github.com/search?q=%2F%28%3Fi%29%28{query}%5Ba-z0-9_%5D*_%2B%5Ba-z0-9_%5D*%29%2F&type=code&p={number}",
            "https://github.com/search?q=%2F%28%3Fi%29%5C%2F{query}%5Ba-z%5D%2B%2F&type=code&p={number}",
            "https://github.com/search?q=%2F%28%3Fi%29%5C%2F{query}%5Ba-z0-9%5D*%5Cd%5Ba-z0-9%5D*%2F&type=code&p={number}",
            "https://github.com/search?q=%2F%28%3Fi%29%5C%2F{query}%5Ba-z0-9-%5D*-%5Ba-z0-9-%5D%2B%2F&type=code&p={number}",
            "https://github.com/search?q=%2F%28%3Fi%29%5C%2F{query}%5Ba-z0-9%5D*_%2B%5Ba-z0-9_%5D*%2F&type=code&p={number}",
        ]

        for batch in batches:
            print(f"Memproses batch: {batch}")
            urls = generate_urls(query, batch)
            batch_completed = False
            
            for url in urls:
                print(f"Mengambil page source dari {url}")
                page_source = fetch_page_source(driver, url, output_file)

                if "Your search did not match any" in page_source:
                    print(f"Halaman {url} tidak ditemukan hasilnya. Keluar dari batch ini dan lanjutkan batch berikutnya.")
                    batch_completed = True
                    break  # Keluar dari loop untuk batch ini

                time.sleep(random.uniform(3, 6))  # Tidur acak

            if batch_completed:
                continue

        print(f"Proses scraping selesai. Hasil disimpan dalam file: {output_file}")

        # Langkah 3: Jalankan perintah setelah scraping selesai
        run_post_scraping_commands(query)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
