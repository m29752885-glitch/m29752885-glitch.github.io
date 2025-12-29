# plugin_plugin_control.py
# Plugin untuk mengontrol auto-reload plugin
# Letakkan di ./downloads/plugins/

import os

# Status auto reload (default True)
AUTO_RELOAD = True

# Fungsi untuk tampilkan status
def status_auto_reload():
    print("=== Status Auto-Reload Plugin ===")
    print("Auto-Reload saat REPL berjalan:", "Aktif" if AUTO_RELOAD else "Nonaktif")

# Fungsi toggle
def toggle_auto_reload():
    global AUTO_RELOAD
    AUTO_RELOAD = not AUTO_RELOAD
    print("Auto-Reload sekarang:", "Aktif" if AUTO_RELOAD else "Nonaktif")

# Fungsi utama plugin
def kontrol_plugin():
    while True:
        os.system("clear")
        print("=== Plugin Kontrol Auto-Reload ===")
        status_auto_reload()
        print("\n1. Toggle Auto-Reload")
        print("0. Keluar")
        pilih = input("Pilih opsi: ").strip()
        if pilih == "0":
            break
        elif pilih == "1":
            toggle_auto_reload()
            input("Tekan Enter untuk lanjut...")
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk lanjut...")

# Auto jalankan jika dipanggil langsung
if __name__ == "__main__":
    kontrol_plugin()
