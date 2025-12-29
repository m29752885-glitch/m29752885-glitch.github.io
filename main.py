# main.py - Ultimate Bahasa Lo REPL Final
import os, sys, subprocess, time, pickle
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED

# ----------------------------
# Variabel global
# ----------------------------
variabel = {}
macros = {}
prompt_str = "(+)> "
current_folder = "."
plugins_folder = os.path.join(DOWNLOADS_FOLDER, "plugins")
os.makedirs(plugins_folder, exist_ok=True)

# ----------------------------
# Load session
# ----------------------------
session_file = ".session"
if os.path.exists(session_file):
    try:
        with open(session_file,"rb") as f:
            data = pickle.load(f)
            variabel.update(data.get("variabel",{}))
            macros.update(data.get("macros",{}))
        print("Session sebelumnya berhasil dimuat.")
    except:
        print("Gagal memuat session, lanjutkan...")

# ----------------------------
# Log command
# ----------------------------
log_file = "repl.log"
def log(cmd, output=""):
    with open(log_file,"a") as f:
        f.write(f"CMD> {cmd}\n{output}\n")

# ----------------------------
# Evaluasi ekspresi
# ----------------------------
def evaluasi_ekspresi(expr):
    for var in variabel:
        expr = expr.replace(var,str(variabel[var]))
    try:
        return eval(expr)
    except:
        return expr.strip('"')

# ----------------------------
# File Explorer Linux vibes
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
# Proses setiap baris perintah
# ----------------------------
def proses_baris(b):
    b = b.strip()
    global current_folder, prompt_str

    if b=="" or b.startswith("#"):
        return None

    # ----------------------------
    # Admin mode
    # ----------------------------
    if b.lower()=="admin":
        password = input("Masukkan password admin: ").strip()
        if password=="12345":
            print("Mode Admin aktif!")
            while True:
                print("\nMenu Admin:")
                print("1. Tambah repo")
                print("2. Kelola file system")
                print("3. Keluar Admin")
                choice = input("Pilih opsi: ").strip()
                if choice=="3":
                    break
        else:
            print("Password salah!")
        return None

    # ----------------------------
    # Root mode
    # ----------------------------
    if b.lower()=="root -a":
        prompt_str = "[Root]> "
        print("Prompt sekarang menjadi [Root]>")
        return None

    # ----------------------------
    # Proot-distro Linux
    # ----------------------------
    if b.lower()=="linux":
        result = subprocess.getoutput("proot-distro list")
        lines = result.splitlines()
        print("Distro tersedia:")
        distro_status = {}
        for line in lines:
            line = line.strip()
            if line.startswith("*"):
                name = line[1:].strip()
                print(f"{name} (diinstal)")
                distro_status[name]=True
            elif line:
                print(line)
                distro_status[line]=False
        distro = input("Pilih distro: ").strip()
        if distro:
            if not distro_status.get(distro,False):
                print(f"Menginstall {distro} ...")
                subprocess.run(f"proot-distro install {distro}", shell=True)
            print(f"Login ke {distro} ...")
            subprocess.run(f"proot-distro login {distro}", shell=True)
        return None

    # ----------------------------
    # Plugin system
    # ----------------------------
    if b.startswith("plugin"):
        if b.strip()=="plugin -m":
            plugins = [f for f in os.listdir(plugins_folder) if f.endswith(".py")]
            if not plugins:
                print("Belum ada plugin.")
            else:
                print("Plugin tersedia:")
                for i,p in enumerate(plugins,1):
                    print(f"{i}. {p}")
                choice = input("Pilih plugin (nomor) untuk aktifkan: ").strip()
                if choice.isdigit() and 1<=int(choice)<=len(plugins):
                    plugin_path = os.path.join(plugins_folder,plugins[int(choice)-1])
                    try:
                        exec(open(plugin_path).read(), globals())
                        print(f"Plugin {plugins[int(choice)-1]} aktif!")
                    except Exception as e:
                        print("Gagal aktifkan plugin:", e)
            return None
        elif b.strip()=="plugin":
            print("Menu Plugin:")
            print("1. Buat plugin baru")
            print("2. Upload dari GitHub")
            choice = input("Pilih opsi: ").strip()
            if choice=="1":
                filename = input("Nama file plugin (.py): ").strip()
                path = os.path.join(plugins_folder, filename)
                with open(path,"w") as f:
                    f.write("# Plugin baru\n")
                print(f"Plugin {filename} berhasil dibuat.")
            elif choice=="2":
                url = input("Masukkan URL GitHub plugin (.py): ").strip()
                out_file = os.path.join(plugins_folder,url.split("/")[-1])
                subprocess.run(f"wget -O {out_file} {url}", shell=True)
                print(f"Plugin tersimpan di {out_file}")
            return None

    # ----------------------------
    # Backup command
    # ----------------------------
    if b.strip()=="simpan":
        import shutil
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        target = os.path.join(BACKUP_FOLDER,f"backup_{timestamp}")
        os.makedirs(target,exist_ok=True)
        for folder in [DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER]:
            if os.path.exists(folder):
                shutil.copytree(folder,os.path.join(target,os.path.basename(folder)),dirs_exist_ok=True)
        print(f"Backup selesai! Tersimpan di {target}")
        return None

    # ----------------------------
    # File Explorer commands
    # ----------------------------
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return None
    if b.startswith("cat "):
        file = os.path.join(current_folder,b[4:].strip())
        if os.path.exists(file):
            out = subprocess.getoutput(f"head -n 10 {file}")
            print(out)
            log(b,out)
        else:
            print(f"File '{file}' tidak ditemukan!")
        return None
    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder=="/":
            current_folder = "."
        else:
            target_path = os.path.join(current_folder,folder)
            if os.path.exists(target_path) and os.path.isdir(target_path):
                current_folder = os.path.abspath(target_path)
            else:
                print(f"Folder '{folder}' tidak ditemukan!")
        return None
    if b.strip()=="keluar_folder":
        current_folder = "."
        return None
    if b.startswith("pindah "):
        parts = b.split()
        if len(parts)<3:
            print("Format: pindah <nama_file> <folder_tujuan>")
            return None
        file_name = parts[1]
        tujuan = parts[2]
        src_path = os.path.join(DOWNLOADS_FOLDER,file_name)
        if not os.path.exists(src_path):
            print(f"File {file_name} tidak ditemukan di downloads/")
            return None
        os.makedirs(tujuan,exist_ok=True)
        dst_path = os.path.join(tujuan,file_name)
        try:
            os.rename(src_path,dst_path)
            print(f"{file_name} berhasil dipindah ke {tujuan}/")
        except Exception as e:
            print("Gagal memindahkan file:", e)
        return None

    # ----------------------------
    # Interpreter .blo
    # ----------------------------
    if b.startswith("jalankan "):
        file = b[8:].strip()
        path = os.path.join(current_folder,file)
        if os.path.exists(path):
            try:
                exec(open(path).read(), globals())
            except Exception as e:
                print("Error menjalankan file .blo:",e)
        else:
            print(f"File '{file}' tidak ditemukan!")
        return None

    # ----------------------------
    # Semua perintah Linux lain
    # ----------------------------
    try:
        subprocess.run(b,shell=True,cwd=current_folder)
        log(b)
    except:
        print("Terjadi kesalahan menjalankan:",b)
    return None

# ----------------------------
# REPL utama
# ----------------------------
def repl():
    print("\n=== Ultimate Bahasa Lo REPL Final ===")
    print("Ketik 'keluar' untuk keluar.")
    global current_folder, prompt_str
    while True:
        if current_folder==".":
            prompt = "[Root]> " if prompt_str.startswith("[Root]") else "(+)> "
        else:
            prompt = f"[Root]/{os.path.basename(current_folder)}> " if prompt_str.startswith("[Root]") else f"(+) / {os.path.basename(current_folder)}> "
        baris = input(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            print("Session tersimpan. Bye!")
            break
        proses_baris(baris)

if __name__=="__main__":
    repl()
