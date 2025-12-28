# Ultimate Bahasa Lo REPL – Final v5

Ultimate Bahasa Lo REPL adalah REPL custom berbasis Python untuk pengalaman coding ringan, fun, dan fleksibel. Cocok untuk Termux/Linux.

## Fitur Utama

1. **Bahasa Lo alias**
   - Echo → tulis
   - If → jika
   - Elif → apabila
   - Then / : → Maka

2. **File Manager**
   - ls → list file/folder dengan style Linux vibes
   - cat <file> → lihat isi file (10 baris pertama)
   - pindah <file> <folder> → pindahkan file ke folder tujuan
   - Folder aktif ditampilkan di prompt

3. **Folder Management**
   - cd <folder> → masuk folder
   - cd .. → naik 1 level
   - cd / → aman kembali ke root REPL (.)
   - keluar_folder → shortcut balik root REPL (.)
   - Prompt otomatis:
     - Root REPL → (+) >
     - Root mode → [Root]>
     - Folder lain → (+) / folder> / [Root]/folder>

4. **Plugin System**
   - plugin -m → menu aktifkan plugin
   - plugin → buat plugin baru / upload dari GitHub
   - Plugin menggunakan Python

5. **Network & Download**
   - ping <host> → cek koneksi
   - curl <url> → download file ke folder downloads/
   - wget <url> → download file ke folder downloads/
   - git <repo> → clone repo Git ke downloads/

6. **Proot-Distro**
   - linux → daftar distro tersedia
   - Bisa install & login smooth
   - Distro yang sudah terinstall otomatis ditandai (installed)

7. **Backup & Root Mode**
   - simpan → backup data & session ke folder backup/
   - root -a → ubah prompt menjadi [Root]>

8. **Admin Menu**
   - admin → tweak repositori & update paket
   - Pilihan:
     1. Repo GitHub
     2. Repo Linux (update/mirror)

9. **Session**
   - Session tersimpan otomatis di .session
   - Variabel & macro bisa dipakai ulang saat restart

10. **Macros**
    - Bisa buat shortcut perintah custom

11. **Bantuan**
    - Ketik bantuan → daftar semua command & fitur

## Cara Pakai

1. Jalankan di Termux/Linux:
```git clone https://github.com/m29752885-glitch/Bahasa-lo.git
cd Bahasa-lo```
```python bahasa-lo.py```
