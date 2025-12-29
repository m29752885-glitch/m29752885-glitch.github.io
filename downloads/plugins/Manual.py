# Manual_interaktif.py
# Plugin Manual Interaktif Bahasa-lo

def tampilkan_manual():
    print("\n=== Manual Interaktif Bahasa-lo ===")
    print("Selamat datang di manual interaktif Bahasa-lo!")
    print("Pilih topik untuk info lebih detail:")
    print("1. Fitur REPL")
    print("2. Command Python → Bahasa-lo (.blo)")
    print("3. Menggunakan plugin")
    print("4. File dan Folder")
    print("5. Keluar dari manual")
    
    while True:
        pilihan = input("Masukkan nomor topik: ").strip()
        if pilihan == "1":
            print("\n--- Fitur REPL ---")
            print("REPL Bahasa-lo mendukung:")
            print("- Menjalankan kode Python biasa")
            print("- Menjalankan kode .blo dengan 'jalankan namafile.blo'")
            print("- History buffer, tekan Enter untuk eksekusi kode")
        elif pilihan == "2":
            print("\n--- Command Python → Bahasa-lo (.blo) ---")
            print("tulis   → print")
            print("masukan → input")
            print("bulat   → int")
            print("pecahan → float")
            print("panjang → len")
            print("daftar  → list")
            print("kamus   → dict")
            print("jika    → if")
            print("apabila → elif")
            print("lainnya → else")
            print("untuk   → for")
            print("fungsi  → def")
            print("kembalikan → return")
            print("Benar/False → True")
            print("Salah/False → False")
            print("Kosong/None → None")
        elif pilihan == "3":
            print("\n--- Menggunakan plugin ---")
            print("- Plugin auto-load tertentu saat REPL start")
            print("- Bisa aktifkan plugin manual dengan 'plugin -i namaplugin'")
            print("- Bisa nonaktifkan plugin manual, tidak akan auto reload")
        elif pilihan == "4":
            print("\n--- File dan Folder ---")
            print("- Buat file/folder: create file/folder namafile/folder")
            print("- Edit file: edit namafile")
            print("- Hapus file/folder: hapus namafile/folder")
            print("- Navigasi folder: cd nama_folder, ls")
        elif pilihan == "5":
            print("Keluar dari manual interaktif")
            break
        else:
            print("⚠️ Pilihan tidak valid. Masukkan angka 1-5")
            
# Auto-load fungsi jika plugin ini aktif
if __name__ == "__main__":
    tampilkan_manual()
