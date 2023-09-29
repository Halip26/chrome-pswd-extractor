# Mengambil Password Chrome

Kode ini adalah program berbasis Python yang digunakan untuk mengambil password yang tersimpan di Google Chrome. Program ini akan terkoneksi ke database SQLite lokal yang digunakan oleh Chrome untuk menyimpan informasi login, dan mengambil username dan password dari setiap entri. Password yang diambil akan didekripsi menggunakan kunci enkripsi yang terdapat dalam file "Local State" Chrome.

## Instalasi dan Penggunaan

1. Pastikan Anda memiliki Python yang terpasang di sistem Anda.
2. Pastikan Anda memiliki semua pustaka yang diperlukan yang terdaftar di bagian impor kode.
3. Simpan kode dalam file dengan ekstensi .py.
4. Jalankan kode dengan menjalankan perintah `python nama_file.py` pada terminal atau command prompt.
5. To run this:

   - `pip3 install -r requirements.txt`
   - To extract Chrome passwords on Windows, run:

       ```bash
       python chrome-pswd-extract.py
       ```

   - To delete saved passwords on Chrome:

       ```bash
       python delete-chrome-pswd.py
       ```

## Penjelasan setiap baris kodenya

Berikut adalah penjelasan untuk setiap baris kodenya teman-teman:

```import os```: Baris ini mengimpor modul os yang digunakan untuk berinteraksi dengan sistem operasi.

```import json```: Baris ini mengimpor modul json yang digunakan untuk memanipulasi data dalam format JSON.

```import base64```: Baris ini mengimpor modul base64 yang digunakan untuk melakukan operasi enkripsi dan dekripsi Base64.

```import sqlite3```: Baris ini mengimpor modul sqlite3 yang digunakan untuk berinteraksi dengan database SQLite.

```import win32crypt```: Baris ini mengimpor modul win32crypt yang digunakan untuk operasi enkripsi dan dekripsi menggunakan API Windows. Namun, harap diperhatikan bahwa penggunaan modul win32crypt dan fungsi CryptUnprotectData mungkin tidak kompatibel dengan versi Windows yang lebih baru, termasuk Windows 11. Microsoft telah membuat perubahan pada model keamanan (TPM 2.0) yang mendasarinya, yang mungkin mencegah kode ini bekerja dengan benar atau memberikan hasil yang diinginkan.

```from Crypto.Cipher import AES```: Baris ini mengimpor modul AES dari pustaka pihak ketiga Crypto yang digunakan untuk operasi enkripsi dan dekripsi menggunakan algoritma AES.

```import shutil```: Baris ini mengimpor modul shutil yang digunakan untuk melakukan operasi penggandaan dan pemindahan file.

```from datetime import timezone, datetime, timedelta```: Baris ini mengimpor kelas timezone, datetime, dan timedelta dari modul datetime yang digunakan untuk operasi terkait waktu.

```def dapatkan_waktu_chrome(chromedate):```: Baris ini mendefinisikan fungsi dapatkan_waktu_chrome yang menerima satu argumen chromedate dan mengembalikan objek datetime yang dihasilkan dari waktu format Chrome.

```return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)```: Baris ini mengembalikan objek datetime yang dihasilkan dengan menambahkan jumlah mikrodetik dari chromedate ke tanggal awal yang ditentukan (Januari 1601).

```def dapatkan_kunci_enkripsi():```: Baris ini mendefinisikan fungsi dapatkan_kunci_enkripsi yang mengembalikan kunci enkripsi yang digunakan oleh Chrome.

```local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")```: Baris ini mendefinisikan path untuk file "Local State" yang berisi informasi konfigurasi lokal Chrome.

with open(local_state_path, "r", encoding="utf-8") as f:: Baris ini membuka file "Local State" dalam mode pembacaan ("r") dengan pengkodean UTF-8.

```local_state = f.read()```: Baris ini membaca isi file "Local State" dan menyimpannya dalam variabel local_state.

```local_state = json.loads(local_state)```: Baris ini menguraikan isi local_state dari format JSON menjadi objek Python.

```key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])```: Baris ini mendekode kunci enkripsi dari Base64 yang terletak di dalam local_state.

key = key[5:]: Baris ini menghapus karakter pertama dari kunci enkripsi yang berasal dari DPAPI.

```return win32crypt.CryptUnprotectData[key, None, None, None, 0](1)```: Baris ini mengembalikan kunci enkripsi terdekripsi dengan menggunakan fungsi CryptUnprotectData dari modul win32crypt.

```def dekripsi_password(password, key):```: Baris ini mendefinisikan fungsi dekripsi_password yang menerima dua argumen password dan key, dan mengembalikan password terdekripsi.

```iv = password[3:15]```: Baris ini mengambil vektor inisialisasi dari password dan menyimpannya dalam variabel iv.

```password = password[15:]```: Baris ini menghapus vektor inisialisasi dari password dan menyimpan password terenkripsi dalam variabel password.

```cipher = AES.new(key, AES.MODE_GCM, iv)```: Baris ini membuat objek cipher dengan menggunakan kunci key, mode AES GCM, dan vektor inisialisasi iv.

```return cipher.decrypt[password](:-16).decode()```: Baris ini mendekripsi password dengan menggunakan objek cipher dan mengembalikan password terdekripsi dengan menghapus padding terakhir dan mengonversi

## Kontribusi

Kontribusi terbuka untuk perbaikan dan peningkatan lainnya. Harap merujuk pada panduan kontribusi untuk informasi lebih lanjut.

## Lisensi

Distribusi kode di bawah lisensi MIT. Lihat file [LICENSE](LICENSE) untuk informasi lebih lanjut.
