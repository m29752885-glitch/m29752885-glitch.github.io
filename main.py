# main.py - Bahasa-lo FINAL

import os
import sys
import subprocess
from blo_repl import repl_blo
from plugin_loader import auto_reload_all, activate_single_plugin, loaded_plugins
from pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED

# -----------------------------
# Akses level
# -----------------------------
LEVEL = "user"  # user, root, admin
PROMPT_DICT = {"user": "(+) > ", "root": "[#] > ", "admin": "{+} > "}

# -----------------------------
# Folder plugins
# -----------------------------
PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER, "plugins")

# Pastikan folder plugins ada
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

# -----------------------------
# Auto reload plugin tertentu
# -----------------------------
auto_reload_all()

# -----------------------------
# Fungsi bantu
# -----------------------------
def tampil_bantuan():
    print("""
=== BANTUAN BAHASA-LO ===
Command REPL:
- jalankan filename.blo : Jalankan file .blo
- plugin -i nama_plugin  : Aktifkan satu plugin manual
- linux : Masuk ke proot-distro (hanya root/admin)
- cd nama_folder : Pindah folder
- ls : List folder saat ini
- buat file/folder : create nama_file / create nama_folder
- hapus file/folder : delete nama_file / delete nama_folder
- edit nama_file : Edit file menggunakan nano
- backup : Simpan backup folder utama
- help : Tampilkan bantuan
- exit : Keluar dari REPL
""")

def masuk_linux():
    if LEVEL not in ["root", "admin"]:
        print("❌ Hanya root/admin yang bisa masuk Linux")
        return
    try:
        # List distro proot-distro
        subprocess.run(["proot-distro", "list"])
        distro = input("Pilih distro yang diinstall: ").strip()
        # Login distro
        subprocess.run(["proot-distro", "login", distro])
    except Exception as e:
        print(f"❌ Error saat masuk Linux: {e}")

def buat_file(folder, nama, is_folder=False):
    path = os.path.join(folder, nama)
    try:
        if is_folder:
            os.makedirs(path, exist_ok=True)
        else:
            open(path, "a").close()
        print(f"✅ {'Folder' if is_folder else 'File'} {nama} dibuat di {folder}")
    except Exception as e:
        print(f"❌ Gagal buat {'folder' if is_folder else 'file'}: {e}")

def hapus_file(folder, nama):
    path = os.path.join(folder, nama)
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
        print(f"✅ {nama} dihapus")
    except Exception as e:
        print(f"❌ Gagal hapus {nama}: {e}")

def edit_file(folder, nama):
    path = os.path.join(folder, nama)
    if os.path.exists(path):
        subprocess.run(["nano", path])
    else:
        print(f"❌ File {nama} tidak ditemukan di {folder}")

def backup_folder():
    import shutil
    dst = os.path.join(BACKUP_FOLDER, "backup_main")
    try:
        shutil.copytree(".", dst, dirs_exist_ok=True)
        print(f"✅ Backup selesai di {dst}")
    except Exception as e:
        print(f"❌ Backup gagal: {e}")

# -----------------------------
# REPL Utama
# -----------------------------
def repl():
    global LEVEL
    cwd = os.getcwd()
    while True:
        prompt = PROMPT_DICT.get(LEVEL, "(+) > ")
        baris = input(prompt).strip()

        # === Keluar ===
        if baris == "exit":
            print("Keluar dari REPL")
            break

        # === Bantuan ===
        if baris == "help":
            tampil_bantuan()
            continue

        # === Masuk Linux ===
        if baris == "linux":
            masuk_linux()
            continue

        # === Jalankan file .blo ===
        if baris.startswith("jalankan "):
            path_file = baris[9:].strip()
            full_path = os.path.join(cwd, path_file)
            if os.path.exists(full_path):
                try:
                    from blo_interpreter import jalankan_blo
                    jalankan_blo(full_path)
                except Exception as e:
                    print(f"❌ Error jalankan .blo: {e}")
            else:
                print(f"❌ File {path_file} tidak ditemukan")
            continue

        # === Aktifkan plugin manual ===
        if baris.startswith("plugin -i "):
            plugin_name = baris[10:].strip()
            activate_single_plugin(plugin_name)
            continue

        # === CD ===
        if baris.startswith("cd "):
            folder = baris[3:].strip()
            target = os.path.join(cwd, folder)
            if os.path.isdir(target):
                cwd = os.path.abspath(target)
                os.chdir(cwd)
            else:
                print(f"❌ Folder {folder} tidak ditemukan")
            continue

        # === LS ===
        if baris == "ls":
            for f in os.listdir(cwd):
                print(f)
            continue

        # === Buat file/folder ===
        if baris.startswith("create "):
            nama = baris[7:].strip()
            if nama.endswith("/"):
                buat_file(cwd, nama.rstrip("/"), is_folder=True)
            else:
                buat_file(cwd, nama, is_folder=False)
            continue

        # === Hapus file/folder ===
        if baris.startswith("delete "):
            nama = baris[7:].strip()
            hapus_file(cwd, nama)
            continue

        # === Edit file ===
        if baris.startswith("edit "):
            nama = baris[5:].strip()
            edit_file(cwd, nama)
            continue

        # === Backup ===
        if baris == "backup":
            backup_folder()
            continue

        # === Perintah shell biasa (nano, git, wget, dll) ===
        try:
            subprocess.run(baris, shell=True)
        except Exception as e:
            print(f"❌ Error perintah: {e}")

# -----------------------------
# Jalankan REPL
# -----------------------------
if __name__ == "__main__":
    print("=== Bahasa-lo REPL FINAL ===")
    print(f"Level: {LEVEL}")
    repl()
