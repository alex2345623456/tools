import re

# Fungsi untuk memeriksa apakah URL mengandung parameter
def has_parameters(url):
    return '?' in url

# Fungsi untuk memeriksa apakah Request Body tidak kosong (tidak ada (No body))
def has_body(request):
    return '(No body)' not in request and bool(request.strip())

# Membaca file httphistory.txt
with open('httphistory.txt', 'r') as file:
    content = file.read()

# Split konten berdasarkan delimiter yang dipisahkan dengan '================================================================================'
requests = content.split('================================================================================')

# Menyaring request yang memenuhi kondisi
valid_requests = []
for request in requests:
    url_match = re.match(r'http[s]?://[^\s]+', request.strip())  # Gunakan strip untuk mengabaikan spasi awal/akhir

    if url_match:
        url = url_match.group(0)

        # Jika URL memiliki parameter atau body tidak kosong
        if has_parameters(url) or has_body(request):
            valid_requests.append(request)

# Menyimpan hasil yang valid ke dalam file baru
with open('filtered_httphistory.txt', 'w') as output_file:
    output_file.write('\n================================================================================\n'.join(valid_requests))

# Membaca kembali file untuk proses editing lebih lanjut
with open('filtered_httphistory.txt', 'r') as file:
    lines = file.readlines()

# Menghapus baris kosong
lines = [line for line in lines if line.strip()]

# Menambahkan separator di akhir file
lines.append('================================================================================\n')

# Menambahkan baris kosong antara 'Request Headers:' dan 'Request Body:'
edited_lines = []
skip_next = False
for line in lines:
    if 'Request Headers:' in line and not skip_next:
        edited_lines.append(line)
        skip_next = True
    elif 'Request Body:' in line and skip_next:
        edited_lines.append('\n')  # Menambahkan baris kosong sebelum 'Request Body:'
        edited_lines.append(line)
        skip_next = False
    else:
        edited_lines.append(line)

# Menghapus 'Request Body:(No body)' dan 'Request Headers:' serta 'Request Body:' tags
final_lines = []
for line in edited_lines:
    line = line.replace('Request Body:(No body)', '').replace('Request Headers:', '').replace('Request Body:', '')
    final_lines.append(line)

# Menyimpan hasil akhir ke dalam file yang sudah dibersihkan
with open('filtered_httphistory.txt', 'w') as output_file:
    output_file.writelines(final_lines)
