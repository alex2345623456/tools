import argparse
import subprocess
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

# Fungsi untuk menjalankan command dengan subprocess
def run_command(url, output_file):
    # Command yang akan dijalankan dengan sqlmap
    command = [
        'sudo', 'python3', 'sqlmap.py', '-u', url,
        '--technique=T', '--level=3', '--risk=3', '--batch',
        '--random-agent', '--tamper=randomcase,between',
        '--delay=2'
    ]

    # Menjalankan command dan menambahkan output ke file
    try:
        logging.info(f"Running sqlmap on {url}")
        result = subprocess.run(command, capture_output=True, text=True)
        with open(output_file, 'a') as outfile:  # mode append agar hasil tetap tersimpan
            outfile.write(f"===== Output untuk URL: {url} =====\n")
            outfile.write(f"Command: {' '.join(command)}\n")
            outfile.write(f"Standard Output:\n{result.stdout}\n")
            outfile.write(f"Standard Error:\n{result.stderr}\n")
            outfile.write("\n" + "="*50 + "\n")
    except Exception as e:
        with open(output_file, 'a') as outfile:
            outfile.write(f"Error menjalankan command untuk URL {url}: {e}\n")
            outfile.write("="*50 + "\n")
        logging.error(f"Error running sqlmap for {url}: {e}")

# Fungsi utama untuk parsing argumen dan mengelola threading
def main():
    # Setup parser untuk argumen
    parser = argparse.ArgumentParser(description="Script untuk menjalankan sqlmap.py dengan daftar URL dan menyimpan output.")
    
    # Menambahkan argumen yang diperlukan
    parser.add_argument('-l', '--list', required=True, help='File txt yang berisi daftar URL untuk dijalankan.')
    parser.add_argument('-o', '--output', required=True, help='File output untuk menyimpan hasil dari setiap perintah.')
    parser.add_argument('-t', '--threads', type=int, required=True, help='Jumlah thread yang akan dijalankan bersamaan.')

    # Parsing argumen yang dimasukkan pengguna
    args = parser.parse_args()

    # Memeriksa apakah file input ada
    if not os.path.isfile(args.list):
        logging.error(f"File daftar URL {args.list} tidak ditemukan.")
        sys.exit(1)

    # Memastikan file output ada dan bisa ditulis
    try:
        with open(args.output, 'a') as outfile:
            outfile.write("Hasil Pengujian:\n")
            outfile.write("="*50 + "\n")
    except IOError as e:
        logging.error(f"Error membuka file output {args.output}: {e}")
        sys.exit(1)

    # Membaca file yang berisi daftar URL
    with open(args.list, 'r') as file:
        urls = [url.strip() for url in file.readlines()]

    # Menentukan jumlah threads yang akan dijalankan bersamaan
    threads = args.threads

    # Memastikan jumlah thread valid
    if threads <= 0:
        logging.error("Jumlah thread harus lebih besar dari 0.")
        sys.exit(1)

    # Menggunakan ThreadPoolExecutor untuk menjalankan threads secara bersamaan
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Menjalankan command untuk setiap URL
        futures = [executor.submit(run_command, url, args.output) for url in urls]

        # Menunggu hasil dari semua thread dan menangani error jika ada
        for future in as_completed(futures):
            try:
                future.result()  # Mengambil hasil dari task
            except Exception as e:
                logging.error(f"Error dalam menjalankan thread: {e}")

    logging.info("Proses selesai. Semua hasil disimpan di %s", args.output)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Set default logging level to INFO
    main()
