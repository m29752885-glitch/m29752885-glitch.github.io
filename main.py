# main.py
# ======================
# Ultimate Bahasa-lo REPL
# ======================

import os
import sys
import subprocess
from blo_interpreter import jalankan_blo
from blo_repl import repl_blo
from plugin_loader import auto_reload_all, activate_single_plugin

# ----------------------
# Folder dan level akses
# ----------------------
DOWNLOADS_FOLDER = "./downloads"
PACKAGES_FOLDER = "./packages"
ADMIN_FOLDER = "./admin"
BACKUP_FOLDER = "./backup"
PLUGINS_FOLDER = "./downloads/plugins"

os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
os.makedirs(PACKAGES_FOLDER, exist_ok=True)
os.makedirs(ADMIN_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

LEVEL = "user"
PROMPT = "(+)> "

# ----------------------
# Fungsi bantu
# ----------------------
def menu_bantuan():
    print("=== Menu Bantuan Bahasa-lo ===")
    print("Command dasar:")
    print("  jalankan <file.blo>    : Jalankan file .blo")
    print("  cd <folder>            : Pindah folder")
    print("  ls                     : Lihat isi folder")
    print("  nano <file>            : Edit file")
    print("  simpan                 : Backup folder penting")
    print("  plugin -i <plugin>     : Aktifkan plugin tertentu")
    print("  linux <command>        : Jalankan command Linux (root/admin)")
    print("  bantuan                : Tampilkan menu bantuan")
    print("  exit                   : Keluar REPL")
    print("Level akses:")
    print("  User : (+)>")
    print("  Root : [#]>")
    print("  Admin: {+}>")

def update_prompt():
    global PROMPT
    if LEVEL == "user":
        PROMPT = "(+)> "
    elif LEVEL == "root":
        PROMPT = "[#]> "
    elif LEVEL == "admin":
        PROMPT = "{+}> "

def masuk_root():
    global LEVEL
    if LEVEL == "user":
        LEVEL = "root"
    update_prompt()

def masuk_admin():
    global LEVEL
    password = input("Masukkan password admin: ")
    if password == "12345":
        global LEVEL
        LEVEL = "admin"
        update_prompt()
        print("✅ Akses admin diberikan")
    else:
        print("❌ Password salah")

def keluar_root():
    global LEVEL
    if LEVEL in ["root", "admin"]:
        LEVEL = "user"
        update_prompt()
        print("✅ Kembali ke level user")

# ----------------------
# File Explorer
# ----------------------
current_dir = os.getcwd()

def command_cd(args):
    global current_dir
    if len(args) == 0:
        print(current_dir)
        return
    path = args[0]
    try:
        os.chdir(path)
        current_dir = os.getcwd()
    except FileNotFoundError:
        print(f"❌ Folder {path} tidak ditemukan")

def command_ls(args):
    for item in os.listdir(current_dir):
        print(item)

def command_nano(args):
    if len(args) == 0:
        print("❌ Masukkan nama file")
        return
    path = args[0]
    try:
        subprocess.call(["nano", path])
    except Exception as e:
        print(f"❌ Gagal buka nano: {e}")

# ----------------------
# Backup
# ----------------------
def command_simpan():
    backup_name = os.path.join(BACKUP_FOLDER, "backup.zip")
    subprocess.call(["zip", "-r", backup_name, current_dir])
    print(f"✅ Backup tersimpan di {backup_name}")

# ----------------------
# Linux command
# ----------------------
def command_linux(args):
    if LEVEL not in ["root", "admin"]:
        print("❌ Akses Linux hanya untuk root/admin")
        return
    if len(args) == 0:
        print("❌ Masukkan command Linux")
        return
    try:
        subprocess.call(args)
    except Exception as e:
        print(f"❌ Error saat menjalankan Linux command: {e}")

# ----------------------
# Jalankan plugin tertentu
# ----------------------
auto_reload_all()

# ----------------------
# REPL utama
# ----------------------
def repl():
    print("=== Bahasa-lo REPL FINAL ===")
    print(f"Level: {LEVEL}")
    while True:
        try:
            baris = input(PROMPT)
            if baris.strip() == "":
                continue
            parts = baris.strip().split()
            cmd = parts[0]
            args = parts[1:]

            if cmd == "exit":
                print("Keluar dari REPL")
                break
            elif cmd == "bantuan":
                menu_bantuan()
            elif cmd == "jalankan":
                if len(args) == 0:
                    print("❌ Masukkan nama file .blo")
                    continue
                jalankan_blo(args[0])
            elif cmd == "cd":
                command_cd(args)
            elif cmd == "ls":
                command_ls(args)
            elif cmd == "nano":
                command_nano(args)
            elif cmd == "simpan":
                command_simpan()
            elif cmd == "linux":
                command_linux(args)
            elif cmd == "root":
                masuk_root()
            elif cmd == "admin":
                masuk_admin()
            elif cmd == "keluar_root":
                keluar_root()
            elif cmd == "plugin":
                if len(args) >= 2 and args[0] == "-i":
                    activate_single_plugin(args[1])
                else:
                    print("❌ Gunakan: plugin -i <nama_plugin>")
            else:
                print(f"❌ Command {cmd} tidak ditemukan")

        except KeyboardInterrupt:
            print("\nKeluar REPL")
            break

# ----------------------
# Main
# ----------------------
if __name__ == "__main__":
    repl()
