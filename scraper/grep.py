import subprocess
import argparse

# Fungsi untuk menjalankan perintah grep
def run_grep(query):
    # Menyiapkan perintah grep dengan opsi -o untuk hanya menampilkan hasil yang cocok
    command = ['grep', '-Pi', '-o', f'{query}[a-z0-9-_]+', 'output.txt']
    
    try:
        # Menjalankan perintah dan menangkap hasilnya
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Menyimpan hasil output ke file dengan nama {query}.txt
        output_filename = f'{query}.txt'
        with open(output_filename, 'w') as f:
            f.write(result.stdout)
        
        print(f'Hasil pencarian disimpan di {output_filename}')
    
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat menjalankan perintah grep: {e}")

def main():
    # Parsing argument
    parser = argparse.ArgumentParser(description="Menjalankan grep dengan query tertentu.")
    parser.add_argument('-k', '--query', required=True, help="Query untuk pencarian dengan grep.")
    args = parser.parse_args()
    
    # Menjalankan fungsi dengan query yang diberikan
    run_grep(args.query)

if __name__ == "__main__":
    main()
