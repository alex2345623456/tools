from mitmproxy import http

# Fungsi untuk menangkap dan memproses HTTP request
def request(flow: http.HTTPFlow):
    # Hanya menyimpan request (bukan response)
    request_data = flow.request
    
    # Mengecek apakah URL mengandung kata "chatgpt."
    if "chatgpt." in request_data.url:
        # Menyusun informasi yang akan disimpan
        method = request_data.method           # GET, POST, PUT, DELETE, etc.
        url = request_data.url                 # URL yang diminta
        http_version = request_data.http_version  # Versi HTTP (misalnya 1.1 atau 2)
        body = request_data.content            # Body request (bila ada)
        
        # Mengambil headers request
        headers = request_data.headers         # Dictionary berisi header request
        
        # Cek apakah URL mengandung tanda "="
        url_contains_equal_sign = "=" in request_data.url
        
        # Cek apakah body request mengandung tanda "=" atau ":"
        body_contains_special_chars = ("=" in body.decode('utf-8', 'ignore') or ":" in body.decode('utf-8', 'ignore')) if body else False
        
        # Syarat untuk menyimpan request:
        # - URL mengandung "chatgpt." dan tanda "=" di URL
        # - URL mengandung "chatgpt." dan body mengandung tanda "=" atau ":"
        if (url_contains_equal_sign and "chatgpt." in request_data.url) or body_contains_special_chars:
            # Membuka file httphistory.txt dan menambahkan request yang baru
            with open("httphistory.txt", "a") as f:
                # Menulis URL, method, dan HTTP Version sesuai format yang diminta
                f.write(f"{url}\n")
                f.write(f"Method:{method}\n")
                f.write(f"HTTP Version:{http_version}\n")
                
                # Menulis headers request sesuai format yang diminta
                for header, value in headers.items():
                    f.write(f"Request Headers:{header}: {value}\n")
                
                # Menulis body request jika ada
                if body:
                    try:
                        f.write(f"Request Body:{body.decode('utf-8', 'ignore')}\n")
                    except UnicodeDecodeError:
                        # Jika body tidak bisa di-decode dengan UTF-8, tampilkan dalam format hexadecimal
                        f.write(f"Request Body:{body.hex()}\n")
                else:
                    f.write("Request Body:(No body)\n")
                
                f.write("=" * 80 + "\n")  # Pembatas antar request

# Menjalankan mitmproxy dengan script ini
if __name__ == "__main__":
    from mitmproxy import proxy
    from mitmproxy.options import Options

    # Menyiapkan options untuk mitmproxy
    options = Options(listen_host="0.0.0.0", listen_port=8080)
    m = proxy.ProxyServer(options)
    
    # Menyiapkan addon untuk menangani request
    p = proxy.ProxyConfig(options)
    addons = [request]
    
    # Menjalankan proxy dengan addon
    m = mitmproxy.controller.Master(p, addons)
    m.run()
