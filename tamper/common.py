import argparse
import random

def space2comment(payload):
    """Mengganti spasi dengan komentar SQL."""
    return payload.replace(" ", "/**/")

def randomcase(payload):
    """Mengubah huruf besar/kecil secara acak."""
    return ''.join(char.upper() if random.choice([True, False]) else char.lower() for char in payload)

def equaltolike(payload):
    """Mengganti operator = dengan LIKE."""
    return payload.replace("=", " LIKE ")

def apply_tamper(payload):
    """Gabungkan semua tamper: space2comment, randomcase, equaltolike."""
    tampered = space2comment(payload)
    tampered = randomcase(tampered)
    tampered = equaltolike(tampered)
    return tampered

def process_payloads(input_file):
    """Baca file payload, terapkan tamper, dan cetak hasilnya."""
    try:
        with open(input_file, 'r') as f:
            payloads = f.readlines()

        print("Payloads Setelah Tamper:\n")
        for i, payload in enumerate(payloads, 1):
            original = payload.strip()
            tampered = apply_tamper(original)
            print(f"Payload {i}:\nOriginal: {original}\nTampered: {tampered}\n")
    except FileNotFoundError:
        print(f"File {input_file} tidak ditemukan. Periksa kembali nama file atau path-nya.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tamper script untuk mengubah payload.")
    parser.add_argument("-l", "--list", required=True, help="File teks yang berisi daftar payload.")
    args = parser.parse_args()

    process_payloads(args.list)
