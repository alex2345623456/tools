import os
import threading
import argparse
from queue import Queue

def split_requests(input_file):
    """
    Fungsi untuk memisahkan request dari file input dan hanya menyimpan yang valid (tidak mengandung 'Request Body:(No body)').
    """
    with open(input_file, 'r') as file:
        content = file.read()
    
    # Pisahkan berdasarkan delimiter '================================================================================'
    requests = content.split("\n================================================================================\n")
    
    # Buat folder untuk menampung file request terpisah
    output_dir = 'separated_requests'
    os.makedirs(output_dir, exist_ok=True)
    
    valid_requests = []  # Menyimpan daftar file request yang valid
    
    for i, request in enumerate(requests):
        if request.strip():  # Pastikan request tidak kosong
            # Periksa apakah ada "Request Body:(No body)" dalam request
            if "Request Body:(No body)" not in request:
                # Simpan request yang valid ke file terpisah
                output_file = os.path.join(output_dir, f'request_{i+1}.txt')
                with open(output_file, 'w') as f:
                    f.write(request)
                valid_requests.append(output_file)  # Tambahkan file yang valid ke daftar
                
    return valid_requests  # Mengembalikan daftar file request yang valid

def run_sqli_script(request_file, payload_file):
    """
    Fungsi untuk menjalankan script 'sqli1.py' dengan argumen request dan payload.
    """
    command = f'python3 sqli1.py -l {request_file} -p {payload_file}'
    os.system(command)

def worker(queue, payload_file):
    """
    Fungsi pekerja yang akan mengambil file dari queue dan menjalankan SQL Injection testing.
    """
    while not queue.empty():
        request_file = queue.get()  # Ambil file dari queue
        print(f"Thread {threading.current_thread().name} sedang memproses {request_file}")
        run_sqli_script(request_file, payload_file)
        queue.task_done()  # Tandai bahwa pekerjaan ini telah selesai

def run_in_threads(valid_request_files, payload_file, num_threads):
    """
    Fungsi untuk menjalankan pengujian SQL Injection dengan menggunakan beberapa thread secara paralel.
    """
    queue = Queue()  # Membuat queue untuk mendistribusikan file request ke thread
    
    # Masukkan semua file request ke dalam queue
    for request_file in valid_request_files:
        queue.put(request_file)
    
    threads = []
    
    # Membuat dan memulai thread
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(queue, payload_file))
        threads.append(thread)
        thread.start()
    
    # Tunggu semua thread selesai
    for thread in threads:
        thread.join()

def main(input_file, payload_file, num_threads):
    """
    Fungsi utama untuk memisahkan request dan menjalankan pengujian SQL Injection.
    """
    # Pisahkan request dan hanya simpan yang valid
    valid_request_files = split_requests(input_file)
    
    if not valid_request_files:
        print("Tidak ada request yang valid untuk diuji.")
        return
    
    # Jalankan pengujian SQL Injection untuk request yang valid menggunakan multithreading
    run_in_threads(valid_request_files, payload_file, num_threads)

if __name__ == '__main__':
    # Menambahkan parser untuk argumen command-line
    parser = argparse.ArgumentParser(description='SQL Injection script runner with multithreading.')
    parser.add_argument('-l', '--input_file', required=True, help='Path to the input file (httphistory.txt)')
    parser.add_argument('-p', '--payload_file', required=True, help='Path to the payload file (payload.txt)')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of threads to use (default is 1)')
    
    # Parsing argumen dari baris perintah
    args = parser.parse_args()

    # Menjalankan fungsi utama dengan argumen yang diterima
    main(args.input_file, args.payload_file, args.threads)
