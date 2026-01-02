# info.py
# Semua info sistem, plugin, command, panduan .blo

INFO = {
    # ==========================
    # REPL dasar Bahasa-lo
    # ==========================
    "tulis": "Menampilkan teks ke layar. Contoh: tulis 'Halo Dunia'",
    "masukan": "Menerima input dari user. Contoh: nama = masukan 'Nama: '",
    "jalankan": "Menjalankan file .blo. Contoh: jalankan test.blo",
    "plugin -i": "Aktifkan satu plugin tertentu. Contoh: plugin -i Optimasi",
    "plugin -l": "Menampilkan list semua plugin yang tersedia",
    "plugin -c": "Control plugin lebih lanjut (backend, non-output)",
    "CD": "Ganti direktori kerja saat ini. Contoh: CD downloads",
    "ls": "Menampilkan daftar file/folder di direktori saat ini",
    "hapus": "Hapus file atau folder. Contoh: hapus file.txt / hapus folder/",
    "buat": "Membuat file/folder baru. Contoh: buat file.txt / buat folder/",
    "clear": "Membersihkan layar REPL",
    "bantuan": "Menampilkan menu bantuan Bahasa-lo",
    "linux": "Masuk ke proot-distro (hanya root/admin). Pilih distro yang sudah di-install.",
    "downloads": "Folder default untuk semua hasil download wget/curl/git",
    "packages": "Folder tempat paket dari proot-distro tersimpan",
    "agent": "Masuk ke Agent Adaptive Bahasa-lo (.blo), scan file baru, jalankan file, berikan tips",
    
    # ==========================
    # Command Linux / Download
    # ==========================
    "wget": "Download file dari URL. Hasil masuk ./downloads",
    "curl": "Download file dari URL. Hasil masuk ./downloads",
    "git": "Clone repository git. Hasil masuk ./downloads",
    "nano": "Editor teks di terminal (user friendly)",

    # ==========================
    # Plugins
    # ==========================
    "Explorer_fix": "Plugin untuk memperbaiki bug navigasi file (CD, ls, path)",
    "Optimasi": "Plugin untuk optimasi performa REPL dan auto reload plugin",
    "crash_handle": "Plugin agar bug kecil tidak crash sistem",
    "int_mod": "Plugin backend untuk kontrol sistem dan permission engine",
    "manual_install_distro": "Plugin untuk install proot-distro secara manual",
    
    # ==========================
    # Panduan .blo (Python Bahasa Indonesia)
    # ==========================
    "tulis 'teks'": "Print di layar (tulis 'Halo')",
    "masukan 'prompt'": "Input user (nama = masukan 'Nama: ')",
    "bulat('123')": "Convert string ke integer",
    "pecahan('3.14')": "Convert string ke float",
    "panjang(daftar)": "Menghitung jumlah item di list atau string",
    "daftar()": "Membuat list",
    "kamus()": "Membuat dictionary",
    "jika kondisi:": "If statement",
    "apabila kondisi:": "Elif statement",
    "lainnya:": "Else statement",
    "untuk x in daftar:": "For loop",
    "fungsi nama_fungsi():": "Mendefinisikan fungsi",
    "kembalikan nilai": "Return dari fungsi",
    "Benar": "Boolean True",
    "Salah": "Boolean False",
    "Kosong": "None / null",
    
    # ==========================
    # Tips tambahan
    # ==========================
    "auto_reload_plugins": "Auto reload plugin tertentu. Hanya plugin yang aman",
    "manual_plugin": "Aktifkan plugin satu per satu menggunakan plugin -i",
    "permission_engine": "Kontrol akses user, root, admin",
}
