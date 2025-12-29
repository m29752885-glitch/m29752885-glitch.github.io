# ===============================
# Bahasa-lo MAIN FINAL
# ===============================

import os
import subprocess
import json
import time

from blo_interpreter import jalankan_blo

# ===============================
# KONFIGURASI
# ===============================
DOWNLOADS = "./downloads"
PLUGINS = "./downloads/plugins"
BACKUP = "./backup"

AUTO_RELOAD_PLUGINS = [
    "explorer_fix.py",
    "optimasi.py",
    "crash_handle.py"
]

ADMIN_PASSWORD = "12345"

os.makedirs(DOWNLOADS, exist_ok=True)
os.makedirs(PLUGINS, exist_ok=True)
os.makedirs(BACKUP, exist_ok=True)

# ===============================
# STATUS SISTEM
# ===============================
LEVEL = "user"   # user | root | admin
AKTIF_PLUGINS = {}

# ===============================
# UTIL
# ===============================
def clear():
    os.system("clear")

def header():
    print("\n=== Bahasa-lo REPL FINAL ===")
    print(f"Level: {LEVEL}")
    print("============================")

# ===============================
# PLUGIN SYSTEM
# ===============================
def load_plugin(path):
    try:
        with open(path, "r") as f:
            kode = f.read()
        exec(kode, globals())
        print(f"✓ Plugin aktif: {os.path.basename(path)}")
        return True
    except Exception as e:
        print(f"✗ Plugin error: {e}")
        return False

def auto_reload_plugins():
    for p in AUTO_RELOAD_PLUGINS:
        path = os.path.join(PLUGINS, p)
        if os.path.exists(path):
            load_plugin(path)

def plugin_menu():
    files = [f for f in os.listdir(PLUGINS) if f.endswith(".py")]

    if not files:
        print("Tidak ada plugin.")
        return

    print("\nPlugin tersedia:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    pilih = input("Aktifkan plugin nomor: ").strip()
    if pilih.isdigit():
        idx = int(pilih) - 1
        if 0 <= idx < len(files):
            path = os.path.join(PLUGINS, files[idx])
            load_plugin(path)

# ===============================
# LINUX (PROOT-DISTRO)
# ===============================
def menu_linux():
    try:
        out = subprocess.getoutput("proot-distro list")
    except:
        print("proot-distro tidak tersedia")
        return

    distro_status = {}
    print("\nDistro tersedia:")
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("*"):
            name = line[1:].strip()
            distro_status[name] = True
            print(f"- {name} (diinstal)")
        elif line:
            distro_status[line] = False
            print(f"- {line}")

    pilih = input("Pilih distro: ").strip()
    if not pilih:
        return

    if not distro_status.get(pilih, False):
        print("Menginstall distro...")
        subprocess.run(f"proot-distro install {pilih}", shell=True)

    print("Login ke distro...")
    subprocess.run(f"proot-distro login {pilih}", shell=True)

# ===============================
# ADMIN MODE
# ===============================
def masuk_admin():
    global LEVEL
    pwd = input("Password admin: ").strip()
    if pwd == ADMIN_PASSWORD:
        LEVEL = "admin"
        print("✓ Admin mode aktif")
    else:
        print("✗ Password salah")

def keluar_admin():
    global LEVEL
    LEVEL = "user"
    print("Keluar dari admin mode")

# ===============================
# BACKUP
# ===============================
def backup_data():
    ts = time.strftime("%Y%m%d_%H%M%S")
    target = os.path.join(BACKUP, f"backup_{ts}")
    os.makedirs(target, exist_ok=True)

    subprocess.run(f"cp -r {DOWNLOADS} {target}/", shell=True)
    print(f"✓ Backup tersimpan di {target}")

# ===============================
# BANTUAN
# ===============================
def bantuan():
    print("""
Perintah dasar:
- bantuan                : tampilkan bantuan
- jalankan file.blo      : jalankan script Bahasa-lo
- linux                  : masuk menu proot-distro
- plugin                 : aktifkan plugin manual
- simpan                 : backup data
- admin                  : masuk admin mode
- keluar_admin           : keluar admin mode
- root                   : masuk root mode
- keluar_root            : keluar root mode
- exit / keluar          : keluar REPL

Catatan:
- .blo = Python Bahasa Indonesia
- main.py tetap Python asli
""")

# ===============================
# ROOT MODE
# ===============================
def masuk_root():
    global LEVEL
    if LEVEL == "admin":
        LEVEL = "root"
        print("✓ Root mode aktif")
    else:
        print("Root hanya bisa dari admin")

def keluar_root():
    global LEVEL
    if LEVEL == "root":
        LEVEL = "admin"
        print("Keluar dari root mode")

# ===============================
# REPL
# ===============================
def repl():
    clear()
    auto_reload_plugins()

    while True:
        header()
        cmd = input("(+)> ").strip()

        if cmd in ("exit", "keluar"):
            break

        if cmd == "bantuan":
            bantuan()
            continue

        if cmd.startswith("jalankan "):
            file = cmd.split(" ", 1)[1]
            if os.path.exists(file):
                jalankan_blo(file)
            else:
                print("File tidak ditemukan")
            continue

        if cmd == "linux":
            menu_linux()
            continue

        if cmd == "plugin":
            plugin_menu()
            continue

        if cmd == "simpan":
            backup_data()
            continue

        if cmd == "admin":
            masuk_admin()
            continue

        if cmd == "keluar_admin":
            keluar_admin()
            continue

        if cmd == "root":
            masuk_root()
            continue

        if cmd == "keluar_root":
            keluar_root()
            continue

        # command linux biasa
        try:
            subprocess.run(cmd, shell=True)
        except:
            print("Command gagal")

# ===============================
# START
# ===============================
if __name__ == "__main__":
    repl()
