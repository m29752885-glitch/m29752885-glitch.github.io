# plugin_buku_manual.py
# Plugin Buku Manual Lengkap Bahasa-Lo
# Letakkan di ./downloads/plugins/

import os

BLO_FOLDER = "./downloads/buku_manual"  # tempat file .blo
os.makedirs(BLO_FOLDER, exist_ok=True)

# Isi buku manual utama (dapat disimpan juga dalam .blo)
BUKU_MANUAL = """
=== BUKU MANUAL BAHASA-LO ===

1. Python versi Bahasa-Lo:
   print -> tulis
   input -> masukan
   int -> bulat
   float -> pecahan
   len -> panjang
   list -> daftar
   dict -> kamus
   for -> untuk
   if -> jika
   elif -> apabila
   else -> lainnya
   def -> fungsi
   return -> kembalikan
   True/False/None -> Benar/Salah/Kosong

2. REPL Bahasa-Lo:
   - Jalankan kode langsung
   - Macro: simpan perintah
   - Root mode: akses system level
   - Admin mode: akses penuh termasuk repositori & plugin

3. Plugin:
   - plugin : menu utama plugin
   - plugin -m : aktifkan plugin dari list
   - plugin -c : kontrol plugin lebih lanjut (aktif/nonaktif manual)
   - Auto reload plugin saat REPL jalan

4. File Explorer:
   - ls : list file di folder aktif
   - cd <folder> : pindah folder
   - cd / : ke root REPL
   - keluar_folder : shortcut ke root REPL
   - cat <file> : baca isi file

5. Download / Package:
   - curl, wget, git : semua file masuk ./downloads
   - Proot-distro Linux : hasil download ke ./packages

6. Backup:
   - simpan : backup data REPL (downloads, packages, session)

7. Level akses:
   - User: akses terbatas (downloads)
   - Root: jalankan system
   - Admin: kontrol penuh REPL, plugin, repositori

8. Bahasa-Lo .blo:
   - File skrip khusus kita
   - Bisa dijalankan dengan: jalankan <namafile>.blo
   - Contoh .blo ada di folder ./downloads/buku_manual
"""

# Simpan file .blo utama
BLO_FILE = os.path.join(BLO_FOLDER, "buku_manual.blo")
with open(BLO_FILE, "w", encoding="utf-8") as f:
    f.write(BUKU_MANUAL.strip())

# ----------------------------
# Fungsi baca file .blo
# ----------------------------
def baca_blo(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} tidak ditemukan!")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    halaman = 15
    total = len(lines)
    idx = 0
    while idx < total:
        os.system("clear")
        print(f"=== Buku Manual Bahasa-Lo ({os.path.basename(file_path)}) ===\n")
        for i in range(idx, min(idx + halaman, total)):
            print(lines[i].rstrip())
        idx += halaman
        if idx < total:
            input("\nTekan Enter untuk halaman berikutnya...")
        else:
            print("\n=== Akhir Buku ===")
            break

# ----------------------------
# Fungsi utama plugin
# ----------------------------
def jalankan_buku_manual():
    while True:
        os.system("clear")
        print("=== Plugin Buku Manual Bahasa-Lo ===")
        files = [f for f in os.listdir(BLO_FOLDER) if f.endswith(".blo")]
        if not files:
            print("Belum ada file .blo di folder ./downloads/buku_manual")
            break
        for i, f in enumerate(files, 1):
            print(f"{i}. {f}")
        print("0. Keluar")
        pilih = input("Pilih file (nomor): ").strip()
        if pilih == "0":
            break
        if pilih.isdigit() and 1 <= int(pilih) <= len(files):
            baca_blo(os.path.join(BLO_FOLDER, files[int(pilih)-1]))
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk lanjut...")

# Auto jalankan jika dipanggil langsung
if __name__ == "__main__":
    jalankan_buku_manual()
