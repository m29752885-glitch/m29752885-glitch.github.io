#!/usr/bin/env python3
# main.py - Ultimate Bahasa Lo REPL Final

import os, sys, subprocess, time, pickle, json

# ----------------------------
# Config import
# ----------------------------
from config.pkg_config import (
    DOWNLOADS_FOLDER,
    PACKAGES_FOLDER,
    ADMIN_FOLDER,
    BACKUP_FOLDER,
    progress_bar,
    LOADING_MSGS,
    PROGRESS_SPEED
)

PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER, "plugins")
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

# ----------------------------
# Global
# ----------------------------
variabel = {}
macros = {}
session_file = ".session"
prompt_str = "(+)> "
current_folder = "."

# ----------------------------
# Load session sebelumnya
# ----------------------------
if os.path.exists(session_file):
    try:
        with open(session_file,"rb") as f:
            data = pickle.load(f)
            variabel.update(data.get("variabel", {}))
            macros.update(data.get("macros", {}))
        print("Session sebelumnya berhasil dimuat.")
    except:
        print("Gagal load session, lanjut.")

# ----------------------------
# Auto reload plugin
# ----------------------------
for file in os.listdir(PLUGINS_FOLDER):
    if file.endswith(".py"):
        try:
            exec(open(os.path.join(PLUGINS_FOLDER, file)).read(), globals())
        except Exception as e:
            print(f"Gagal load plugin {file}: {e}")

# ----------------------------
# Logging
# ----------------------------
def log(cmd, output=""):
    with open("repl.log","a") as f:
        f.write(f"CMD> {cmd}\n{output}\n")

# ----------------------------
# File manager
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        print(f"Folder '{folder}' tidak ada!")
        return
    entries = os.listdir(folder)
    for entry in entries:
        path = os.path.join(folder, entry)
        stat = os.stat(path)
        size = stat.st_size
        mtime = time.localtime(stat.st_mtime)
        mtime_str = time.strftime("%b %d %H:%M", mtime)
        if os.path.isdir(path):
            print(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size >= 1024 else f"{size}B"
            print(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Proses perintah
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
            print("Mode Admin aktif! Prompt [Admin]>")
            prompt_str = "[Admin]> "
            while True:
                cmd = input(prompt_str).strip()
                if cmd.lower() in ["keluar", "exit"]:
                    prompt_str = "(+)> "
                    break
                elif cmd.startswith("tulis "):
                    isi = cmd[6:]
                    print(isi)
                elif cmd.startswith("ls"):
                    folder = cmd[3:].strip() or current_folder
                    list_files(folder)
                elif cmd.startswith("cd "):
                    folder = cmd[3:].strip()
                    if folder == "/":
                        current_folder = "."
                    else:
                        target = os.path.join(current_folder, folder)
                        if os.path.isdir(target):
                            current_folder = os.path.abspath(target)
                        else:
                            print("Folder tidak ditemukan!")
                else:
                    try:
                        subprocess.run(cmd, shell=True, cwd=current_folder)
                    except:
                        print(f"Gagal menjalankan: {cmd}")
        else:
            print("Password salah!")
        return None

    # Plugin system
    if b.startswith("plugin"):
        if b.strip() == "plugin -m":
            plugins = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
            if not plugins:
                print("Belum ada plugin.")
            else:
                print("Plugin tersedia:")
                for i, p in enumerate(plugins,1):
                    print(f"{i}. {p}")
                choice = input("Pilih plugin (nomor): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(plugins):
                    path = os.path.join(PLUGINS_FOLDER, plugins[int(choice)-1])
                    try:
                        exec(open(path).read(), globals())
                        print("Plugin aktif!")
                    except Exception as e:
                        print(f"Gagal aktifkan plugin: {e}")
        elif b.strip() == "plugin":
            print("Menu Plugin:")
            print("1. Buat file plugin")
            print("2. Upload plugin dari GitHub")
            pilihan = input("Pilih: ").strip()
            if pilihan=="1":
                fn = input("Nama plugin (.py): ").strip()
                path = os.path.join(PLUGINS_FOLDER, fn)
                with open(path,"w") as f:
                    f.write("# Plugin baru\n")
                print(f"{fn} dibuat di {PLUGINS_FOLDER}")
            elif pilihan=="2":
                url = input("URL GitHub plugin: ").strip()
                out_file = os.path.join(PLUGINS_FOLDER, url.split("/")[-1])
                subprocess.run(f"wget -O {out_file} {url}", shell=True)
                print(f"Plugin tersimpan di {out_file}")
        return None

    # File explorer
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return None

    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder == "/":
            current_folder = "."
        else:
            target = os.path.join(current_folder, folder)
            if os.path.isdir(target):
                current_folder = os.path.abspath(target)
            else:
                print("Folder tidak ditemukan!")
        return None

    if b.strip() == "keluar_folder":
        current_folder = "."
        return None

    # Jalankan file .blo
    if b.startswith("jalankan "):
        fn = b[8:].strip()
        path = os.path.join(current_folder, fn)
        if os.path.exists(path):
            try:
                with open(path) as f:
                    kode = f.read()
                    exec(kode, globals())
            except Exception as e:
                print(f"Gagal jalankan {fn}: {e}")
        else:
            print(f"File {fn} tidak ditemukan!")
        return None

    # Bantuan
    if b.lower() == "bantuan":
        print("\n=== Menu Bantuan ===")
        print("Admin: admin")
        print("File explorer: ls, cd <folder>, cd .., cd /, keluar_folder")
        print("Plugin: plugin, plugin -m")
        print("Jalankan file .blo: jalankan <file>.blo")
        print("Keluar REPL: keluar, exit\n")
        return None

    # Default: jalankan di shell
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
        log(b)
    except:
        print(f"Gagal menjalankan: {b}")
    return None

# ----------------------------
# REPL
# ----------------------------
def repl():
    global prompt_str, current_folder
    print("\n=== Ultimate Bahasa Lo REPL ===")
    print("Ketik 'keluar' untuk keluar.")
    while True:
        prompt = prompt_str if current_folder=="." else f"{prompt_str.rstrip('>')}/{os.path.basename(current_folder)}> "
        baris = input(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            print("Session tersimpan. Bye!")
            break
        proses_baris(baris)

if __name__=="__main__":
    repl()
