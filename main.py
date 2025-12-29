# main.py - Bahasa-lo FINAL
import os, sys
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED
from blo_interpreter import jalankan_blo
from pathlib import Path

# -----------------------------
# Global
# -----------------------------
USER_LEVEL = "user"
CURRENT_FOLDER = os.getcwd()
PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER, "plugins")
AKTIF_PLUGINS = ["Explorer_fix.py","Optimasi.py","crash_handle.py"]  # auto reload beberapa plugin

os.makedirs(PLUGINS_FOLDER, exist_ok=True)

# -----------------------------
# REPL
# -----------------------------
def repl():
    global CURRENT_FOLDER, USER_LEVEL
    tulis("=== Bahasa-lo REPL FINAL ===")
    tulis(f"Level: {USER_LEVEL}")
    while True:
        if USER_LEVEL == "user":
            prompt = "(+)>" 
        elif USER_LEVEL == "root":
            prompt = "[#]>"
        else:
            prompt = "{+}>"

        command = input(prompt).strip()

        # Keluar
        if command in ["exit", "keluar", "quit"]:
            tulis("Keluar dari REPL...")
            break

        # Bantuan
        if command == "bantuan":
            tulis("=== Bantuan Bahasa-lo ===")
            tulis("cd [folder] : masuk folder")
            tulis("ls : daftar file folder sekarang")
            tulis("touch [nama] : buat file di folder sekarang")
            tulis("mkdir [nama] : buat folder")
            tulis("jalankan [file.blo] : jalankan file .blo")
            tulis("linux : masuk proot-distro (root/admin)")
            tulis("admin : masuk mode admin (password 12345)")
            tulis("simpan : backup folder downloads/packages/admin")
            continue

        # Admin
        if command.startswith("admin"):
            if USER_LEVEL != "admin":
                pw = input("Password Admin: ")
                if pw == "12345":
                    USER_LEVEL = "admin"
                    tulis("Login Admin berhasil")
                else:
                    tulis("Password salah")
            continue

        # Linux command
        if command == "linux":
            if USER_LEVEL in ["root", "admin"]:
                tulis("Masuk ke proot-distro (root mode). Ketik 'exit' untuk keluar.")
                while True:
                    subcmd = input("[linux]# ").strip()
                    if subcmd in ["exit", "keluar"]:
                        tulis("Keluar dari Linux")
                        break
            else:
                tulis("Akses ditolak: hanya root/admin yang bisa menggunakan 'linux'")
            continue

        # File Explorer
        parts = command.split()
        base = parts[0]
        args = parts[1:]

        if base == "cd":
            if args:
                target = os.path.join(CURRENT_FOLDER, args[0])
                if os.path.isdir(target):
                    CURRENT_FOLDER = target
                    os.chdir(CURRENT_FOLDER)
                else:
                    tulis(f"Folder tidak ditemukan: {args[0]}")
            else:
                tulis(CURRENT_FOLDER)
            continue

        if base == "ls":
            tulis("\n".join(os.listdir(CURRENT_FOLDER)))
            continue

        if base == "mkdir":
            if args:
                os.makedirs(os.path.join(CURRENT_FOLDER, args[0]), exist_ok=True)
            continue

        if base == "touch":
            if args:
                path = os.path.join(CURRENT_FOLDER, args[0])
                Path(path).touch(exist_ok=True)
            continue

        # Backup
        if base == "simpan":
            tulis("Membuat backup...")
            for folder in [DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER]:
                tulis(f"Backup folder: {folder}")
            continue

        # Jalankan .blo
        if base == "jalankan":
            if args:
                path = os.path.join(CURRENT_FOLDER, args[0])
                if os.path.isfile(path):
                    jalankan_blo(path)
                else:
                    tulis(f"File tidak ditemukan: {args[0]}")
            continue

        # Default
        tulis(f"Perintah tidak dikenal: {command}")

# -----------------------------
# Fungsi tulis
# -----------------------------
def tulis(teks):
    print(teks)

# -----------------------------
# Start
# -----------------------------
if __name__ == "__main__":
    repl()
