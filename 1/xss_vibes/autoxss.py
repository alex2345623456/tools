import argparse
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fungsi untuk menjalankan command dengan subprocess
def run_command(url, output_file):
    # Command yang akan dijalankan dengan main.py
    command = ['sudo', 'python3', 'main.py', '-u', url, '-t', '7', '--waf']

    # Menjalankan command dan menambahkan output ke file
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        with open(output_file, 'a') as outfile:  # mode append agar hasil tetap tersimpan
            # Menambahkan URL yang sedang diproses ke dalam file output
            outfile.write(f"===== Output untuk URL: {url} =====\n")
            outfile.write(f"Command: {' '.join(command)}\n")
            outfile.write(f"Standard Output:\n{result.stdout}\n")
            outfile.write(f"Standard Error:\n{result.stderr}\n")
            outfile.write("\n" + "="*50 + "\n")
    except Exception as e:
        with open(output_file, 'a') as outfile:
            outfile.write(f"Error menjalankan command untuk URL {url}: {e}\n")
            outfile.write("="*50 + "\n")

# Fungsi utama untuk parsing argumen dan mengelola threading
def main():
    # Setup parser untuk argumen
    parser = argparse.ArgumentParser(description="Script untuk menjalankan main.py dengan daftar URL dan menyimpan output.")
    
    # Menambahkan argumen yang diperlukan
    parser.add_argument('-l', '--list', required=True, help='File txt yang berisi daftar URL untuk dijalankan.')
    parser.add_argument('-o', '--output', required=True, help='File output untuk menyimpan hasil dari setiap perintah.')
    parser.add_argument('-t', '--threads', type=int, required=True, help='Jumlah thread yang akan dijalankan bersamaan.')

    # Parsing argumen yang dimasukkan pengguna
    args = parser.parse_args()

    # Memeriksa apakah file input ada
    if not os.path.isfile(args.list):
        print(f"File daftar URL {args.list} tidak ditemukan.")
        return

    # Memastikan file output ada
    with open(args.output, 'a') as outfile:
        outfile.write("Hasil Pengujian:\n")
        outfile.write("="*50 + "\n")
    
    # Membaca file yang berisi daftar URL
    with open(args.list, 'r') as file:
        urls = [url.strip() for url in file.readlines()]

    # Menentukan jumlah threads yang akan dijalankan bersamaan
    threads = args.threads

    # Menggunakan ThreadPoolExecutor untuk menjalankan threads secara bersamaan
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Menjalankan command untuk setiap URL
        futures = [executor.submit(run_command, url, args.output) for url in urls]

        # Menunggu hasil dari semua thread dan menangani error jika ada
        for future in as_completed(futures):
            try:
                future.result()  # Mengambil hasil dari task
            except Exception as e:
                print(f"Error dalam menjalankan thread: {e}")

    print("Proses selesai. Semua hasil disimpan di", args.output)

if __name__ == '__main__':
    main()
