import subprocess
import argparse

# Fungsi untuk menjalankan perintah grep
def run_grep_command(query, input_file, output_file):
    # Daftar perintah grep yang akan dijalankan
    grep_commands = [
        f"grep -i -o -P '{query}[a-zA-Z]+' {input_file}",  # Menggunakan -P
        f"grep -i -o -P '{query}[a-z0-9]*[0-9][a-z0-9]*' {input_file}",
        f"grep -i -o -P '{query}[a-z0-9-]*-[a-z0-9-]*' {input_file}",
        f"grep -i -o -P '{query}[a-z0-9_]*_[a-z0-9_]*' {input_file}",
        f"grep -i -o -P '/{query}[a-zA-Z]+' {input_file} | sed 's/\\///g'",  # Menggunakan -P
        f"grep -i -o -P '/{query}[a-z0-9]*[0-9][a-z0-9]*' {input_file} | sed 's/\\///g'",
        f"grep -i -o -P '/{query}[a-z0-9-]*-[a-z0-9-]+' {input_file} | sed 's/\\///g'",
        f"grep -i -o -P '/{query}[a-z0-9_]*_[a-z0-9_]*' {input_file} | sed 's/\\///g'"
    ]
    
    with open(output_file, 'w') as f:
        for command in grep_commands:
            print(f"Menjalankan perintah: {command}")
            try:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                f.write(result.decode())
            except subprocess.CalledProcessError as e:
                print(f"Error menjalankan perintah: {e.cmd}")
                print(f"Output error: {e.output.decode()}")

def main():
    parser = argparse.ArgumentParser(description="Menjalankan serangkaian perintah grep berdasarkan query yang diberikan.")
    parser.add_argument("-k", "--query", required=True, help="String query untuk mencari di file output.txt")
    parser.add_argument("-i", "--input_file", default="output.txt", help="File yang akan dicari (default: output.txt)")
    args = parser.parse_args()

    query = args.query  # Tanpa sanitasi input

    output_file = f"{query}.txt"
    
    run_grep_command(query, args.input_file, output_file)
    print(f"Hasil disimpan di {output_file}")

if __name__ == "__main__":
    main()
