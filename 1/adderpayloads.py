import subprocess

# Fungsi untuk menjalankan perintah dengan payload tertentu
def run_command(payload):
    command = f'python3 adder.py -p "{payload}" -w wafwaf'
    try:
        # Menjalankan perintah di shell
        subprocess.run(command, shell=True, check=True)
        print(f'Perintah berhasil dijalankan dengan payload: {payload}')
    except subprocess.CalledProcessError as e:
        print(f'Gagal menjalankan perintah untuk payload: {payload}\nError: {e}')

# Membaca file wafwaf.txt dan menjalankan perintah untuk setiap payload
def process_payloads(filename):
    try:
        # Membuka file wafwaf.txt
        with open(filename, 'r') as file:
            # Membaca setiap baris (payload) dari file
            payloads = file.readlines()
            
            # Menghapus karakter newline (newline characters) di setiap baris
            payloads = [payload.strip() for payload in payloads]
            
            # Menjalankan perintah untuk setiap payload
            for payload in payloads:
                run_command(payload)
    
    except FileNotFoundError:
        print(f'File {filename} tidak ditemukan!')
    except Exception as e:
        print(f'Error: {e}')

# Menjalankan proses untuk file wafwaf.txt
if __name__ == "__main__":
    process_payloads('wafwaf.txt')
