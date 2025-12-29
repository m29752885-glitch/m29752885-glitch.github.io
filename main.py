#!/data/data/com.termux/files/usr/bin/env python3
# main.py – Ultimate Bahasa Lo REPL Final

import os, sys, subprocess, time, pickle
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED

# ----------------------------
# Global setup
# ----------------------------
variabel = {}
macros = {}
prompt_str = "(+)> "
current_folder = "."
session_file = ".session"
PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER,"plugins")
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

# ----------------------------
# Load session
# ----------------------------
if os.path.exists(session_file):
    try:
        with open(session_file,"rb") as f:
            data = pickle.load(f)
            variabel.update(data.get("variabel",{}))
            macros.update(data.get("macros",{}))
        print("Session sebelumnya berhasil dimuat.")
    except:
        print("Gagal load session, lanjut.")

# ----------------------------
# Auto reload plugins
# ----------------------------
for file in os.listdir(PLUGINS_FOLDER):
    if file.endswith(".py"):
        try:
            exec(open(os.path.join(PLUGINS_FOLDER,file)).read(), globals())
        except Exception as e:
            print(f"Gagal load plugin {file}: {e}")

# ----------------------------
# File manager Linux vibes
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        print(f"Folder '{folder}' tidak ada!")
        return
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        stat = os.stat(path)
        size = stat.st_size
        mtime = time.localtime(stat.st_mtime)
        mtime_str = time.strftime("%b %d %H:%M", mtime)
        if os.path.isdir(path):
            print(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size>=1024 else f"{size}B"
            print(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Command interpreter
# ----------------------------
def proses_baris(b):
    global prompt_str, current_folder

    b = b.strip()
    if not b or b.startswith("#"):
        return None

    # Admin mode
    if b.lower() == "admin":
        password = input("Masukkan password admin: ").strip()
        if password == "12345":
            print("Admin mode aktif! Pilih menu tweak:")
            print("1. Repo admin cloud\n2. File system")
            choice = input("Pilih opsi: ").strip()
            if choice=="1":
                url = input("Masukkan URL repo baru: ").strip()
                out_dir = os.path.join(ADMIN_FOLDER,url.split("/")[-1].replace(".git",""))
                print(f"Clone/update {url} ke {out_dir} ...")
                subprocess.run(f"git clone {url} {out_dir}", shell=True)
            elif choice=="2":
                print("Bisa mengedit semua folder & file system utama")
            return None
        else:
            print("Password salah!")
            return None

    # Plugin menu
    if b.startswith("plugin"):
        if b.strip() == "plugin -m":
            plugins = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
            if not plugins:
                print("Belum ada plugin.")
            else:
                print("Plugin tersedia:")
                for i,p in enumerate(plugins,1):
                    print(f"{i}. {p}")
                choice = input("Pilih plugin untuk aktifkan (nomor): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(plugins):
                    path = os.path.join(PLUGINS_FOLDER,plugins[int(choice)-1])
                    try: exec(open(path).read(), globals()); print("Plugin aktif!")
                    except Exception as e: print("Gagal aktifkan plugin:", e)
            return None
        elif b.strip() == "plugin":
            print("Menu Plugin:")
            print("1. Buat plugin baru")
            print("2. Upload dari GitHub")
            return None

    # Interpreter .blo
    if b.startswith("jalankan "):
        file_blo = os.path.join(current_folder, b[9:].strip())
        if os.path.exists(file_blo):
            try:
                with open(file_blo) as f: exec(f.read(), globals())
            except Exception as e:
                print(f"Gagal jalankan {file_blo}: {e}")
        else:
            print(f"{file_blo} tidak ditemukan")
        return None

    # File manager
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return None
    if b.startswith("cat "):
        file = os.path.join(current_folder, b[4:].strip())
        if os.path.exists(file):
            print(subprocess.getoutput(f"head -n 10 {file}"))
        else: print(f"File '{file}' tidak ditemukan")
        return None
    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder == "/": current_folder = "."
        else:
            target_path = os.path.join(current_folder, folder)
            if os.path.exists(target_path) and os.path.isdir(target_path):
                current_folder = os.path.abspath(target_path)
            else: print(f"Folder '{folder}' tidak ditemukan!")
        return None
    if b.strip() == "keluar_folder": current_folder = "."

    # Linux / proot-distro
    if b.lower() == "linux":
        try:
            result = subprocess.getoutput("proot-distro list")
            lines = result.splitlines()
            print("Distro tersedia:")
            distro_status = {}
            for line in lines:
                line = line.strip()
                if line.startswith("*"):
                    name = line[1:].strip()
                    print(f"{name} (diinstal)")
                    distro_status[name] = True
                elif line:
                    print(line)
                    distro_status[line] = False
            distro = input("Pilih distro: ").strip()
            if distro:
                if not distro_status.get(distro,False):
                    print(f"Menginstall {distro} ...")
                    progress_bar("Install distro",2)
                    subprocess.run(f"proot-distro install {distro}", shell=True)
                    print(f"{distro} selesai!")
                subprocess.run(f"proot-distro login {distro}", shell=True, cwd=PACKAGES_FOLDER)
        except Exception as e: print(f"Gagal menjalankan Linux: {e}")
        return None

    # Jalankan command lain Linux
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
    except: print(f"Gagal jalankan: {b}")
    return None

# ----------------------------
# Bantuan
# ----------------------------
def bantuan():
    print("""
Fitur tersedia:
- File Explorer: ls, cat, cd <folder>, keluar_folder
- Plugin: plugin, plugin -m (auto reload di start)
- Admin: admin (password 12345)
- Interpreter: jalankan <file>.blo
- Linux: linux (proot-distro install & login)
- Folder penting: downloads, packages, admin, backup
- Akses level: user / root / admin
""")

# ----------------------------
# REPL
# ----------------------------
def repl():
    global prompt_str, current_folder
    print("\n=== Ultimate Bahasa Lo REPL Final ===")
    print("Ketik 'keluar' untuk keluar, 'bantuan' untuk info fitur.")
    while True:
        prompt = "[Admin]> " if prompt_str.startswith("[Admin]") else ("[Root]> " if prompt_str.startswith("[Root]") else "(+)> ")
        baris = input(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            print("Session tersimpan. Bye!")
            break
        if baris.lower() == "bantuan":
            bantuan()
            continue
        proses_baris(baris)

if __name__=="__main__":
    repl()
