import argparse
import subprocess

def run_scraper(query):
    """Menjalankan command untuk menjalankan scraper dengan keyword tertentu."""
    command = ["python3", "scraper.py", "-k", query]
    try:
        subprocess.run(command, check=True)
        print(f"Scraping untuk '{query}' selesai.")
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat menjalankan scraper untuk '{query}': {e}")

def main():
    # Setup parser argument
    parser = argparse.ArgumentParser(description="Menjalankan scraper dengan keyword dari file teks.")
    parser.add_argument('-l', '--list', required=True, help="File teks berisi list keyword.")
    args = parser.parse_args()

    # Membaca file yang berisi list keyword
    try:
        with open(args.list, 'r') as file:
            keywords = file.readlines()
            # Hilangkan karakter newline dari setiap keyword
            keywords = [keyword.strip() for keyword in keywords]
    except FileNotFoundError:
        print(f"File {args.list} tidak ditemukan.")
        return

    # Jalankan scraper untuk setiap keyword
    for keyword in keywords:
        run_scraper(keyword)

if __name__ == '__main__':
    main()
