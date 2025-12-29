#!/usr/bin/env python3
# main.py - Bahasa-lo REPL FINAL

import os, sys, subprocess, pickle, time

# ----------------------------
# IMPORT CONFIG
# ----------------------------
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED, PROGRESS_SYMBOL, PROGRESS_LENGTH

# ----------------------------
# GLOBAL
# ----------------------------
VARIABEL = {}
MACROS = {}
SESSION_FILE = ".session"
PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER, "plugins")
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

# ----------------------------
# PROMPT LEVEL
# ----------------------------
PROMPT_USER = "(+)> "
PROMPT_ROOT = "[Root]> "
PROMPT_ADMIN = "[Admin]> "
level = "user"  # user/root/admin
current_folder = "."

# ----------------------------
# LOAD SESSION
# ----------------------------
if os.path.exists(SESSION_FILE):
    try:
        with open(SESSION_FILE,"rb") as f:
            data = pickle.load(f)
            VARIABEL.update(data.get("variabel",{}))
            MACROS.update(data.get("macros",{}))
        print("Session sebelumnya dimuat.")
    except:
        print("Gagal load session, lanjut.")

# ----------------------------
# AUTO RELOAD PLUGINS
# ----------------------------
def load_plugins():
    for file in os.listdir(PLUGINS_FOLDER):
        if file.endswith(".py"):
            try:
                exec(open(os.path.join(PLUGINS_FOLDER,file)).read(), globals())
            except Exception as e:
                print("Plugin gagal dimuat:", file, e)
load_plugins()

# ----------------------------
# FILE EXPLORER
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        print(f"Folder '{folder}' tidak ada!")
        return
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        if os.path.isdir(path):
            print(f"drwxr-xr-x {entry}")
        else:
            size = os.stat(path).st_size
            print(f"-rw-r--r-- {size} {entry}")

# ----------------------------
# BLO INTERPRETER
# ----------------------------
def jalankan_blo(file):
    path = os.path.join(current_folder,file)
    if not os.path.exists(path):
        print(f"File {file} tidak ditemukan!")
        return
    with open(path,"r") as f:
        kode = f.read()
    for line in kode.splitlines():
        proses_baris(line)

# ----------------------------
# PROSES BARIS COMMAND
# ----------------------------
def proses_baris(b):
    global current_folder, level
    b = b.strip()
    if b=="" or b.startswith("#"):
        return
    # ADMIN
    if b.lower()=="admin":
        pw = input("Password admin: ")
        if pw=="12345":
            level="admin"
            print("Mode admin aktif!")
        else:
            print("Password salah!")
        return
    # ROOT
    if b.lower()=="masuk_root":
        level="root"
        print("Mode root aktif!")
        return
    if b.lower()=="keluar_root":
        level="user"
        print("Kembali ke mode user")
        return
    # BANTUAN
    if b.lower()=="bantuan":
        print("""
=== MENU BANTUAN ===

File Explorer:
  ls               : menampilkan daftar file/folder
  cd <folder>      : pindah folder
  pwd              : tampilkan folder saat ini

Linux:
  linux            : daftar distro proot-distro
  linux login <distro> : login ke distro tertentu

BLO interpreter:
  jalankan <file.blo> : jalankan script .blo

Plugin:
  plugin            : tampilkan plugin yang tersedia
  plugin -m         : reload plugin

Akses mode:
  masuk_root        : ubah mode ke root
  keluar_root       : kembali user
  admin             : masuk mode admin (password: 12345)
  keluar            : keluar REPL

Catatan:
  - User biasa hanya bisa akses ./downloads
  - Root bisa jalankan perintah sistem
  - Admin bisa mengelola seluruh filesystem & plugin
""")
        return
    # FILE COMMAND
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return
    if b.startswith("cd "):
        target = b[3:].strip()
        if target=="..":
            current_folder=os.path.dirname(current_folder)
        else:
            new_path=os.path.join(current_folder,target)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                current_folder=os.path.abspath(new_path)
            else:
                print("Folder tidak ditemukan!")
        return
    if b=="pwd":
        print(current_folder)
        return
    # BLO
    if b.startswith("jalankan "):
        jalankan_blo(b[9:].strip())
        return
    # PLUGIN
    if b.startswith("plugin"):
        if b.strip()=="plugin -m":
            load_plugins()
            print("Plugin dimuat ulang!")
            return
        else:
            files = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
            if not files:
                print("Belum ada plugin")
            else:
                for i,f in enumerate(files,1):
                    print(f"{i}. {f}")
            return
    # LINUX
    if b.startswith("linux"):
        try:
            result = subprocess.getoutput("proot-distro list")
            print(result)
            distro = input("Pilih distro untuk login: ").strip()
            if distro:
                subprocess.run(f"proot-distro login {distro}", shell=True, cwd=PACKAGES_FOLDER)
        except Exception as e:
            print("Linux error:", e)
        return
    # USER / ROOT COMMAND
    if level in ["root","admin"]:
        try:
            subprocess.run(b, shell=True, cwd=current_folder)
        except:
            print("Perintah error!")
    else:
        print("Perintah hanya untuk root/admin!")

# ----------------------------
# REPL
# ----------------------------
def repl():
    global current_folder, level
    print("=== Ultimate Bahasa Lo REPL FINAL ===")
    while True:
        prompt = PROMPT_ADMIN if level=="admin" else PROMPT_ROOT if level=="root" else PROMPT_USER
        baris = input(f"{prompt} ")
        if baris.lower() in ["keluar","exit"]:
            with open(SESSION_FILE,"wb") as f:
                pickle.dump({"variabel":VARIABEL,"macros":MACROS},f)
            print("Session tersimpan. Bye!")
            break
        proses_baris(baris)

if __name__=="__main__":
    repl()
