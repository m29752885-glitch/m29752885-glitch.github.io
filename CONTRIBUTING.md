CONTRIBUTING.md – Bahasa-lo
Terima kasih sudah mau berkontribusi ke Bahasa-lo! 🎉
Ikuti panduan singkat ini supaya kontribusi lo lancar.
Cara Mulai
Fork repo ini
Clone ke lokal / VPS:
git clone https://github.com/<username-lo>/Bahasa-lo.git
Masuk folder repo:
cd Bahasa-lo
Buat branch baru untuk fitur / bug fix:
git checkout -b nama-fitur
Struktur Folder

Bahasa-lo/
├── main.py
├── blo_interpreter.py
├── blo_repl.py
├── plugin_loader.py
├── downloads/
│   ├── plugins/
│   └── packages/
├── README.md
└── config/
    └── pkg_config.py
Semua plugin diletakkan di ./downloads/plugins.
Plugin
Gunakan .py
Nama plugin tanpa spasi
Fungsi utama plugin harus bisa dipanggil saat di-load
Aktifkan plugin manual atau auto reload:
Python
from plugin_loader import auto_reload_all
auto_reload_all()

from plugin_loader import activate_single_plugin
activate_single_plugin("NamaPlugin")
REPL & .blo
.blo → versi Python bahasa Indonesia
Jalankan REPL: python blo_repl.py
Contoh perintah:

tulis "Halo Dunia"
masukan "Nama kamu: "
Jalankan file .blo: jalankan namafile.blo
Coding Style
Indentasi 4 spasi
Snake_case untuk variabel/fungsi
Tambahkan komentar
Jangan hapus fitur lama tanpa izin
Bug & Pull Request
Laporkan bug via Issues
Sertakan deskripsi, langkah reproduksi, log/error
Commit:
git add .
git commit -m "Menambahkan fitur XYZ"
Push: git push origin nama-branch
Buat Pull Request ke main
Aturan
Jangan hapus main.py, blo_interpreter.py
Plugin auto hanya plugin aman
Gunakan bahasa Indonesia di .blo
Semua download masuk ./downloads
