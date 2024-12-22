import argparse
import requests
import re
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Daftar pola regex untuk mendeteksi data sensitif (semua pola dari js-detection.yaml)
sensitive_patterns = [
    ("Access Key", r"access_key[^\s]*"),
    ("Access Token", r"access_token[^\s]*"),
    ("Admin Password", r"admin_pass[^\s]*"),
    ("Admin User", r"admin_user[^\s]*"),
    ("Algolia Admin Key", r"algolia_admin_key[^\s]*"),
    ("Algolia API Key", r"algolia_api_key[^\s]*"),
    ("Alias Password", r"alias_pass[^\s]*"),
    ("Alicloud Access Key", r"alicloud_access_key[^\s]*"),
    ("Amazon Secret Access Key", r"amazon_secret_access_key[^\s]*"),
    ("Amazon AWS", r"amazonaws[^\s]*"),
    ("Ansible Vault Password", r"ansible_vault_password[^\s]*"),
    ("AOS Key", r"aos_key[^\s]*"),
    ("API Key", r"api_key[^\s]*"),
    ("API Key Secret", r"api_key_secret[^\s]*"),
    ("API Key SID", r"api_key_sid[^\s]*"),
    ("API Secret", r"api_secret[^\s]*"),
    ("APIDocs", r"apidocs[^\s]*"),
    ("API Secret", r"apiSecret[^\s]*"),
    ("App Debug", r"app_debug[^\s]*"),
    ("App ID", r"app_id[^\s]*"),
    ("App Key", r"app_key[^\s]*"),
    ("App Log Level", r"app_log_level[^\s]*"),
    ("App Secret", r"app_secret[^\s]*"),
    ("App Key", r"appkey[^\s]*"),
    ("App Key Secret", r"appkeysecret[^\s]*"),
    ("Application Key", r"application_key[^\s]*"),
    ("App Secret", r"appsecret[^\s]*"),
    ("Appspot", r"appspot[^\s]*"),
    ("Auth Token", r"auth_token[^\s]*"),
    ("Authorization Token", r"authorizationToken[^\s]*"),
    ("Auth Secret", r"authsecret[^\s]*"),
    ("AWS Access", r"aws_access[^\s]*"),
    ("AWS Access Key ID", r"aws_access_key_id[^\s]*"),
    ("AWS Bucket", r"aws_bucket[^\s]*"),
    ("AWS Key", r"aws_key[^\s]*"),
    ("AWS Secret Key", r"aws_secret_key[^\s]*"),
    ("AWS Token", r"aws_token[^\s]*"),
    ("AWS Secret Key", r"AWSSecretKey[^\s]*"),
    ("B2 App Key", r"b2_app_key[^\s]*"),
    ("Bashrc Password", r"bashrc\s*password[^\s]*"),
    ("Bintray API Key", r"bintray_apikey[^\s]*"),
    ("Bintray GPG Password", r"bintray_gpg_password[^\s]*"),
    ("Bintray Key", r"bintray_key[^\s]*"),
    ("Bintray Key (Alt)", r"bintraykey[^\s]*"),
    ("Bluemix API Key", r"bluemix_api_key[^\s]*"),
    ("Bluemix Password", r"bluemix_pass[^\s]*"),
    ("BrowserStack Access Key", r"browserstack_access_key[^\s]*"),
    ("Bucket Password", r"bucket_password[^\s]*"),
    ("Bucketeer AWS Access Key ID", r"bucketeer_aws_access_key_id[^\s]*"),
    ("Bucketeer AWS Secret Access Key", r"bucketeer_aws_secret_access_key[^\s]*"),
    ("Built Branch Deploy Key", r"built_branch_deploy_key[^\s]*"),
    ("BX Password", r"bx_password[^\s]*"),
    ("Cache Driver", r"cache_driver[^\s]*"),
    ("Cache S3 Secret Key", r"cache_s3_secret_key[^\s]*"),
    ("Cattle Access Key", r"cattle_access_key[^\s]*"),
    ("Cattle Secret Key", r"cattle_secret_key[^\s]*"),
    ("Certificate Password", r"certificate_password[^\s]*"),
    ("CI Deploy Password", r"ci_deploy_password[^\s]*"),
    ("Client Secret", r"client_secret[^\s]*"),
    ("Client ZPK Secret Key", r"client_zpk_secret_key[^\s]*"),
    ("Clojars Password", r"clojars_password[^\s]*"),
    ("Cloud API Key", r"cloud_api_key[^\s]*"),
    ("Cloud Watch AWS Access Key", r"cloud_watch_aws_access_key[^\s]*"),
    ("Cloudant Password", r"cloudant_password[^\s]*"),
    ("Cloudflare API Key", r"cloudflare_api_key[^\s]*"),
    ("Cloudflare Auth Key", r"cloudflare_auth_key[^\s]*"),
    ("Cloudinary API Secret", r"cloudinary_api_secret[^\s]*"),
    ("Cloudinary Name", r"cloudinary_name[^\s]*"),
    ("Codecov Token", r"codecov_token[^\s]*"),
    ("Config", r"config[^\s]*"),
    ("Connection Login", r"conn\.login[^\s]*"),
    ("Connection String", r"connectionstring[^\s]*"),
    ("Consumer Key", r"consumer_key[^\s]*"),
    ("Consumer Secret", r"consumer_secret[^\s]*"),
    ("Credentials", r"credentials[^\s]*"),
    ("Cypress Record Key", r"cypress_record_key[^\s]*"),
    ("Database Password", r"database_password[^\s]*"),
    ("Database Schema Test", r"database_schema_test[^\s]*"),
    ("Datadog API Key", r"datadog_api_key[^\s]*"),
    ("Datadog App Key", r"datadog_app_key[^\s]*"),
    ("DB Password", r"db_password[^\s]*"),
    ("DB Server", r"db_server[^\s]*"),
    ("DB Username", r"db_username[^\s]*"),
    ("DB Password (Alt)", r"dbpasswd[^\s]*|dbpassword[^\s]*"),
    ("DB User", r"dbuser[^\s]*"),
    ("Deploy Password", r"deploy_password[^\s]*"),
    ("DigitalOcean SSH Key Body", r"digitalocean_ssh_key_body[^\s]*"),
    ("DigitalOcean SSH Key IDs", r"digitalocean_ssh_key_ids[^\s]*"),
    ("Docker Hub Password", r"docker_hub_password[^\s]*"),
    ("Docker Key", r"docker_key[^\s]*"),
    ("Docker Password", r"docker_pass[^\s]*|docker_passwd[^\s]*|docker_password[^\s]*"),
    ("Dockerhub Password", r"dockerhub_password[^\s]*|dockerhubpassword[^\s]*"),
    ("Dot Files", r"dot-files[^\s]*|dotfiles[^\s]*"),
    ("Droplet Travis Password", r"droplet_travis_password[^\s]*"),
    ("DynamoDB Access Key ID", r"dynamoaccesskeyid[^\s]*"),
    ("DynamoDB Secret Access Key", r"dynamosecretaccesskey[^\s]*"),
    ("Elastica Host", r"elastica_host[^\s]*"),
    ("Elastica Port", r"elastica_port[^\s]*"),
    ("Elasticsearch Password", r"elasticsearch_password[^\s]*"),
    ("Encryption Key", r"encryption_key[^\s]*"),
    ("Encryption Password", r"encryption_password[^\s]*"),
    ("Heroku API Key", r"heroku_api_key[^\s]*"),
    ("Sonatype Password", r"sonatype_password[^\s]*"),
    ("AWS Secret Key (Alt)", r"awssecretkey[^\s]*"),
]

# Fungsi untuk mengunduh file JavaScript dan mencari data sensitif
def detect_sensitive_data(url):
    try:
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0',
                'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
            ])
        }
        # Mengunduh file JavaScript
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"[INFO] Berhasil mengunduh file: {url}")
            for label, pattern in sensitive_patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    print(f"[Peringatan] Ditemukan {label}: {matches}")
        else:
            print(f"[ERROR] Gagal mengunduh file. Status code: {response.status_code} - URL: {url}")
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat mengunduh file {url}: {e}")

# Fungsi untuk menguji URL dalam beberapa thread
def scan_url_thread(urls):
    for url in urls:
        detect_sensitive_data(url)
        time.sleep(random.uniform(0, 1))  # Tidur acak antara 0 hingga 1 detik

# Fungsi utama
def main():
    parser = argparse.ArgumentParser(description="Deteksi Data Sensitif di File JavaScript")
    parser.add_argument("-l", "--list", type=str, required=True, help="File yang berisi daftar URL untuk diuji")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Jumlah thread yang digunakan untuk pengujian")

    args = parser.parse_args()

    # Membaca daftar URL dari file
    with open(args.list, "r") as file:
        urls = [line.strip() for line in file.readlines()]

    # Membagi URL menjadi beberapa bagian untuk setiap thread
    chunk_size = len(urls) // args.threads
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    # Menjalankan thread
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(scan_url_thread, url_chunks)

if __name__ == "__main__":
    main()
