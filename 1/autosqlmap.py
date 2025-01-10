import os
import subprocess
import argparse

# Daftar metode HTTP yang dikenal
HTTP_METHODS = [
    "GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD",
    "CONNECT", "TRACE", "PATCH"
]

# Fungsi untuk membaca file dan memisahkan request berdasarkan delimiter
def split_requests(filename):
    with open(filename, "r") as file:
        content = file.read()
    # Memisahkan request berdasarkan delimiter
    return content.split("=" * 80)

# Fungsi untuk menulis request ke file sementara
def write_request_to_file(request, filename):
    with open(filename, "w") as file:
        file.write(request.strip())

# Fungsi untuk mengambil request line dari request
def get_request_line(request):
    for line in request.splitlines():
        # Periksa apakah baris diawali dengan metode HTTP yang dikenal
        if any(line.startswith(method) for method in HTTP_METHODS):
            return line
    return "Unknown Request Line"

# Fungsi untuk mengambil Host dari request
def get_host(request):
    for line in request.splitlines():
        if line.lower().startswith("host:"):
            return line.split(":", 1)[1].strip()
    return "Unknown Host"

# Fungsi untuk menjalankan perintah sqlmap
def run_sqlmap(request_file, tamper_script=None):
    command = [
        "python3", "sqlmap.py",
        "-r", request_file,
        "--technique=T",
        "--random-agent",
        "--level", "5",
        "--batch",
        "--flush-session"
    ]
    # Tambahkan opsi tamper jika diberikan
    if tamper_script:
        command.extend(["--tamper", tamper_script])
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout, result.stderr

# Proses utama
def main():
    # Parsing argumen untuk file request, tamper script, dan output
    parser = argparse.ArgumentParser(description="Run SQLMap with multiple requests and optional tamper script")
    parser.add_argument("-l", "--list", required=True, help="File containing all requests")
    parser.add_argument("-t", "--tamper", help="Tamper script to use with SQLMap (optional)")
    parser.add_argument("-o", "--output", help="File to save the output logs (optional)")
    args = parser.parse_args()

    all_requests_file = args.list
    tamper_script = args.tamper
    output_file = args.output

    # Membuka file output jika diberikan
    log_file = None
    if output_file:
        log_file = open(output_file, "w")

    # Membaca dan memisahkan request dari file
    requests = split_requests(all_requests_file)

    # Iterasi untuk setiap request
    for i, request in enumerate(requests):
        temp_request_file = f"request_{i + 1}.txt"  # Nama file sementara
        write_request_to_file(request, temp_request_file)  # Simpan request ke file

        # Ambil Request line dan Host untuk ditampilkan
        request_line = get_request_line(request)
        host = get_host(request)
        log_message = f"Running sqlmap for request {i + 1} {request_line} {host}"

        # Cetak dan tulis log_message ke file log
        print(log_message)
        if log_file:
            log_file.write(f"{log_message}\n")

        # Jalankan sqlmap dan ambil outputnya
        stdout, stderr = run_sqlmap(temp_request_file, tamper_script)

        # Simpan log hasil eksekusi sqlmap ke file log jika diberikan
        if log_file:
            log_file.write(f"STDOUT:\n{stdout}\n")
            log_file.write(f"STDERR:\n{stderr}\n")
            log_file.write("=" * 80 + "\n")

        os.remove(temp_request_file)  # Hapus file sementara

    # Tutup file output jika dibuka
    if log_file:
        log_file.close()

if __name__ == "__main__":
    main()
