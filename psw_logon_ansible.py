import requests
import json
from flask import Flask
from flask import jsonify

app = Flask(__name__)


# Konfigurasi
AWX_IP = "172.18.53.100"
AWX_TOKEN = "crGU7ZVYLkMjpXPq30L2LlQjdKVkqd"
JOB_TEMPLATE_ID = 36  # Ganti dengan ID templat pekerjaan yang ingin Anda jalankan
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {AWX_TOKEN}"}
url = "http://172.18.53.100"

import os
no_proxy_hosts = ["localhost", "127.0.0.1", "172.18.53.100"]
os.environ["no_proxy"] = ",".join(no_proxy_hosts)
response = requests.get(url)
print(response.text)


# Fungsi untuk meluncurkan pekerjaan menggunakan templat pekerjaan ID
def launch_job():
    try:
        response = requests.post(f"http://{AWX_IP}/api/v2/job_templates/{JOB_TEMPLATE_ID}/launch/", headers=HEADERS)
        response.raise_for_status()
        print("Pekerjaan berhasil diluncurkan.")
    except requests.exceptions.RequestException as e:
        print("Gagal meluncurkan pekerjaan:", e)
        print(response.text)

def main():
    # Lakukan peluncuran pekerjaan
    launch_job()

if __name__ == "__main__":
    main()
