# info.py
# Informasi untuk AI Agent Adaptive Bahasa-lo (.blo)
# Semakin detail, AI bisa menyusun jawaban lebih natural

INFO = {
    # ======================
    # Dasar Python (.blo)
    # ======================
    "tulis": "Gunakan 'tulis' untuk menampilkan teks. Contoh: tulis 'Halo Dunia'.",
    "masukan": "Gunakan 'masukan' untuk meminta input pengguna. Contoh: nama = masukan 'Nama kamu: '",
    "bulat": "Gunakan 'bulat' untuk mengubah nilai menjadi integer. Contoh: x = bulat('123')",
    "pecahan": "Gunakan 'pecahan' untuk mengubah nilai menjadi float. Contoh: y = pecahan('3.14')",
    "panjang": "Gunakan 'panjang' untuk menghitung panjang list atau string. Contoh: panjang([1,2,3])",
    "daftar": "Gunakan 'daftar' untuk membuat list. Contoh: mylist = daftar([1,2,3])",
    "kamus": "Gunakan 'kamus' untuk membuat dictionary. Contoh: mydict = kamus({'a':1})",
    "Benar": "Gunakan 'Benar' untuk True.",
    "Salah": "Gunakan 'Salah' untuk False.",
    "Kosong": "Gunakan 'Kosong' untuk None.",

    # ======================
    # Struktur Kontrol
    # ======================
    "jika": "Gunakan 'jika' untuk if statement. Contoh: jika x > 0:",
    "apabila": "Gunakan 'apabila' untuk elif statement. Contoh: apabila x == 0:",
    "lainnya": "Gunakan 'lainnya' untuk else. Contoh: lainnya:",
    "untuk": "Gunakan 'untuk' untuk for loop. Contoh: untuk i dalam daftar([1,2,3]):",
    "fungsi": "Gunakan 'fungsi' untuk membuat function. Contoh: fungsi salam():",
    "kembalikan": "Gunakan 'kembalikan' untuk return. Contoh: kembalikan x + y",

    # ======================
    # REPL & File
    # ======================
    "jalankan": "Gunakan 'jalankan namafile.blo' untuk menjalankan file .blo dari REPL atau Agent.",
    "scan": "Gunakan 'scan' untuk mengecek file .blo baru di folder downloads.",
    "keluar": "Gunakan 'keluar' untuk keluar dari REPL atau Agent Adaptive.",
    "buat": "Gunakan 'buat nama_file' untuk membuat file baru atau 'buat folder nama_folder' untuk membuat folder.",
    "hapus": "Gunakan 'hapus nama_file' atau 'hapus folder nama_folder' untuk menghapus file/folder.",
    "edit": "Gunakan 'edit nama_file' untuk mengedit file menggunakan nano.",

    # ======================
    # Plugin
    # ======================
    "plugin": "Gunakan 'plugin -i NamaPlugin' untuk mengaktifkan plugin, 'plugin -l' untuk daftar plugin.",
    "auto_reload": "Beberapa plugin akan di-reload otomatis saat start REPL jika diaktifkan.",
    
    # ======================
    # Linux Command (Proot-distro)
    # ======================
    "apt": "Gunakan 'apt' atau command Linux lain di mode Linux untuk menginstall package di distro.",
    "linux": "Gunakan 'linux' untuk masuk ke Proot-distro yang terinstall di Termux/VPS.",
    "wget": "Gunakan 'wget URL' untuk download file dari internet. Semua hasil masuk ./downloads/",
    "git": "Gunakan 'git clone URL' untuk clone repo. Semua hasil masuk ./downloads/",

    # ======================
    # AI / Agent
    # ======================
    "agent": "AI Adaptive Bahasa-lo bisa memberi tips, membaca file .blo baru, dan menjalankan kode.",
    "adaptive": "AI akan menyesuaikan jawaban berdasarkan file .blo, plugin, command, dan info yang diketahui.",
    "thinking": "Saat AI menampilkan 'thinking...', berarti sedang memproses input untuk menyusun jawaban.",
    
    # ======================
    # Tips Pemula
    # ======================
    "error": "Jika muncul error, baca pesan error, cek syntax .blo, dan pastikan nama file benar.",
    "debug": "Mode debug akan menampilkan langkah-langkah eksekusi Python/.blo dan Linux command."
}
