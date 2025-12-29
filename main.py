# main.py - Ultimate Bahasa-Lo REPL Final
import os, sys, subprocess, time, pickle, json
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED

# ----------------------------
# Level akses & prompt
# ----------------------------
level = "user"  # default
PROMPT = {"user":"(+)>" , "root":"[Root]>", "admin":"[ADMIN] />"}

# ----------------------------
# Variabel global
# ----------------------------
variabel = {}
macros = {}
plugins = []
current_folder = "."
PLUGIN_FOLDER = "./plugins"
os.makedirs(PLUGIN_FOLDER, exist_ok=True)

# ----------------------------
# Load session
# ----------------------------
SESSION_FILE = ".session"
if os.path.exists(SESSION_FILE):
    try:
        with open(SESSION_FILE,"rb") as f:
            data = pickle.load(f)
            variabel.update(data.get("variabel",{}))
            macros.update(data.get("macros",{}))
        print("Session sebelumnya berhasil dimuat.")
    except:
        print("Gagal load session, lanjut.")

# ----------------------------
# Load plugin auto-reload
# ----------------------------
def load_plugins():
    global plugins
    plugins = []
    for file in os.listdir(PLUGIN_FOLDER):
        if file.endswith(".py"):
            path = os.path.join(PLUGIN_FOLDER, file)
            try:
                exec(open(path).read(), globals())
                plugins.append(file)
            except Exception as e:
                print(f"Gagal load plugin {file}: {e}")

load_plugins()

# ----------------------------
# Helper fungsi Python -> Bahasa Indonesia
# ----------------------------
tulis = print
masukan = input
bulat = int
pecahan = float
panjang = len
daftar = list
kamus = dict
Benar = True
Salah = False
Kosong = None

# ----------------------------
# File explorer Linux vibe
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        tulis(f"Folder '{folder}' tidak ada!")
        return
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        stat = os.stat(path)
        size = stat.st_size
        mtime = time.localtime(stat.st_mtime)
        mtime_str = time.strftime("%b %d %H:%M", mtime)
        if os.path.isdir(path):
            tulis(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size>=1024 else f"{size}B"
            tulis(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Admin menu
# ----------------------------
def admin_menu():
    global level
    tulis("=== Admin Menu ===")
    tulis("1. Kelola filesystem")
    tulis("2. Reload plugin")
    tulis("3. Backup sistem")
    tulis("4. Restore sistem")
    tulis("5. Keluar menu admin")
    pilihan = masukan("Pilih opsi: ").strip()
    if pilihan=="1":
        tulis("Filesystem management mode (akses penuh)")
    elif pilihan=="2":
        load_plugins()
        tulis("Plugins reload selesai!")
    elif pilihan=="3":
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        target = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")
        os.makedirs(target, exist_ok=True)
        for folder in [DOWNLOADS_FOLDER, PACKAGES_FOLDER, PLUGIN_FOLDER, ADMIN_FOLDER]:
            subprocess.run(f"rsync -a {folder} {target}/", shell=True)
        if os.path.exists(SESSION_FILE):
            subprocess.run(f"cp {SESSION_FILE} {target}/", shell=True)
        tulis(f"Backup selesai: {target}")
    elif pilihan=="4":
        tulis("Restore sistem manual via backup folder")
    elif pilihan=="5":
        return
    else:
        tulis("Pilihan tidak valid")

# ----------------------------
# Jalankan file .blo
# ----------------------------
def jalankan_file(nama):
    path = os.path.join(current_folder, nama)
    if not os.path.exists(path):
        tulis(f"File '{nama}' tidak ditemukan!")
        return
    try:
        with open(path) as f:
            kode = f.read()
            exec(kode, globals(), variabel)
    except Exception as e:
        tulis("Error eksekusi:", e)

# ----------------------------
# REPL
# ----------------------------
def repl():
    global current_folder, level
    tulis("\n=== Ultimate Bahasa Lo REPL ===")
    tulis("Ketik 'keluar' untuk keluar, 'bantuan' untuk list command.")
    while True:
        prompt = PROMPT[level] + " "
        baris = masukan(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(SESSION_FILE,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros}, f)
            tulis("Session tersimpan. Bye!")
            break
        if baris.strip()=="":
            continue

        # Bantuan
        if baris.lower() == "bantuan":
            tulis("=== Menu Bantuan Bahasa-Lo ===")
            tulis("Command dasar: ls, cd <folder>, cd .., cat <file>, jalankan <file.blo>")
            tulis("Level akses: user, root, admin")
            tulis("Masuk admin: admin")
            tulis("Plugin: auto load & reload (admin)")
            tulis("File management: downloads/, packages/, plugins/")
            continue

        # Admin mode
        if baris.lower() == "admin":
            pwd = masukan("Password admin: ").strip()
            if pwd=="12345":
                level="admin"
                tulis("Admin mode aktif!")
                admin_menu()
                level="user"
            else:
                tulis("Password salah!")
            continue

        # File explorer
        if baris.startswith("ls"):
            folder = baris[3:].strip() or current_folder
            list_files(folder)
            continue
        if baris.startswith("cd "):
            target = baris[3:].strip()
            if target=="..":
                current_folder = os.path.dirname(current_folder) or "."
            else:
                new_path = os.path.join(current_folder, target)
                if os.path.exists(new_path) and os.path.isdir(new_path):
                    current_folder = os.path.abspath(new_path)
                else:
                    tulis(f"Folder '{target}' tidak ditemukan!")
            continue
        if baris.startswith("cat "):
            file = os.path.join(current_folder, baris[4:].strip())
            if os.path.exists(file):
                tulis(open(file).read())
            else:
                tulis(f"File '{file}' tidak ditemukan!")
            continue

        # Jalankan .blo
        if baris.startswith("jalankan "):
            nama = baris[9:].strip()
            jalankan_file(nama)
            continue

        # Eksekusi normal
        try:
            exec(baris, globals(), variabel)
        except Exception as e:
            tulis("Error:", e)

if __name__=="__main__":
    repl()
