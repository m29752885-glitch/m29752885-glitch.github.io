# main.py – Ultimate Bahasa-Lo REPL Final Remastered
import os, sys, subprocess, pickle, time
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED

# ----------------------------
# Global
# ----------------------------
variabel = {}
macros = {}
alias_perintah = {"Echo":"tulis"}
alias_keyword = {"jika":"if","apabila":"elif","Maka":":"}
log_file = "repl.log"
session_file = ".session"
PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER,"plugins")
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

# ----------------------------
# Level akses
# ----------------------------
LEVEL = "User"  # User, Root, Admin
prompt_str = "(+)> "
current_folder = "."

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
# Log function
# ----------------------------
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
        mtime_str = time.strftime("%b %d %H:%M", time.localtime(stat.st_mtime))
        if os.path.isdir(path):
            print(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size>=1024 else f"{size}B"
            print(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Plugin loader
# ----------------------------
def load_plugins(auto_reload=True):
    plugins = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
    for plugin in plugins:
        try:
            exec(open(os.path.join(PLUGINS_FOLDER,plugin)).read(), globals())
            if auto_reload:
                print(f"Plugin {plugin} auto-reload aktif!")
        except Exception as e:
            print("Gagal load plugin:", plugin, e)

# ----------------------------
# Proses perintah
# ----------------------------
def proses_baris(b):
    global current_folder, prompt_str, LEVEL
    b = b.strip()
    if b=="" or b.startswith("#"):
        return None

    # Admin mode
    if b.lower()=="admin":
        password = input("Masukkan password admin: ").strip()
        if password=="12345":
            LEVEL="Admin"
            prompt_str="[Admin]> "
            print("Admin mode aktif! Pilih menu:")
            print("1. Kelola repo")
            print("2. Kelola file system")
            choice = input("Pilih opsi: ").strip()
            if choice=="1":
                print("Fitur repo admin (tambah/edit repo) disini")
            elif choice=="2":
                print("Fitur kontrol penuh file system disini")
        else:
            print("Password salah!")
        return None

    # Root mode
    if b.lower()=="root":
        LEVEL="Root"
        prompt_str="[Root]> "
        print("Root mode aktif!")
        return None

    # Proot-distro Linux
    if b.lower()=="linux":
        result = subprocess.getoutput("proot-distro list")
        print("Distro tersedia:")
        for line in result.splitlines():
            print(line)
        distro = input("Pilih distro: ").strip()
        if distro:
            subprocess.run(f"proot-distro login {distro}", shell=True, cwd=PACKAGES_FOLDER)
        return None

    # Plugin commands
    if b.startswith("plugin"):
        if b.strip()=="plugin -m":
            plugins = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
            if not plugins: print("Belum ada plugin."); return None
            print("Plugin tersedia:")
            for i,p in enumerate(plugins,1):
                print(f"{i}. {p}")
            choice = input("Pilih plugin untuk aktifkan (nomor): ").strip()
            if choice.isdigit() and 1<=int(choice)<=len(plugins):
                plugin_path = os.path.join(PLUGINS_FOLDER, plugins[int(choice)-1])
                exec(open(plugin_path).read(), globals())
                print("Plugin aktif!")
            return None
        elif b.strip()=="plugin":
            print("Menu Plugin:")
            print("1. Buat file plugin")
            print("2. Upload dari GitHub")
            choice = input("Pilih opsi: ").strip()
            if choice=="1":
                filename=input("Nama file plugin (.py): ").strip()
                path=os.path.join(PLUGINS_FOLDER,filename)
                with open(path,"w") as f: f.write("# Plugin baru\n")
                print(f"Plugin {filename} berhasil dibuat")
            elif choice=="2":
                url=input("URL GitHub plugin (.py): ").strip()
                out_file=os.path.join(PLUGINS_FOLDER,url.split("/")[-1])
                subprocess.run(f"wget -O {out_file} {url}", shell=True)
            return None

    # Jalankan file .blo
    if b.startswith("jalankan "):
        file_name=b[8:].strip()
        path=os.path.join(current_folder,file_name)
        if os.path.exists(path):
            exec(open(path).read(), globals())
        else:
            print(f"File {file_name} tidak ditemukan!")
        return None

    # File commands
    if b.startswith("cd "):
        folder=b[3:].strip()
        if folder=="/":
            current_folder="."
        else:
            target=os.path.join(current_folder, folder)
            if os.path.exists(target) and os.path.isdir(target):
                current_folder=os.path.abspath(target)
            else:
                print(f"Folder {folder} tidak ditemukan!")
        return None
    if b.strip()=="keluar_folder":
        current_folder="."
        return None
    if b.startswith("ls"):
        folder=b[3:].strip() or current_folder
        list_files(folder)
        return None
    if b.startswith("cat "):
        file_path=os.path.join(current_folder,b[4:].strip())
        if os.path.exists(file_path):
            print(subprocess.getoutput(f"head -n 10 {file_path}"))
        else:
            print(f"File {file_path} tidak ditemukan!")
        return None

    # Backup
    if b.strip()=="simpan":
        timestamp=time.strftime("%Y%m%d-%H%M%S")
        target=os.path.join(BACKUP_FOLDER,f"backup_{timestamp}")
        os.makedirs(target, exist_ok=True)
        for folder in [DOWNLOADS_FOLDER, PACKAGES_FOLDER, PLUGINS_FOLDER]:
            if os.path.exists(folder):
                subprocess.run(f"cp -r {folder} {target}/", shell=True)
        print(f"Backup selesai di {target}")
        return None

    # Bantuan
    if b.lower()=="bantuan":
        print("Perintah utama REPL:")
        print("admin, root, linux, plugin, plugin -m, jalankan <file.blo>")
        print("cd <folder>, ls, cat <file>, pindah <file> <folder>")
        print("simpan, keluar_folder")
        print("Level akses:", LEVEL)
        return None

    # Assignment / tulis
    if "=" in b:
        key,val=b.split("=",1)
        variabel[key.strip()]=evaluasi_ekspresi(val.strip())
        return None
    if b.startswith("tulis "):
        isi=b[6:].strip()
        print(evaluasi_ekspresi(isi))
        return None

    # Linux shell fallback
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
    except:
        print("Terjadi kesalahan menjalankan:",b)
    return None

# ----------------------------
# REPL
# ----------------------------
def repl():
    global prompt_str
    load_plugins(auto_reload=True)
    print("\n=== Ultimate Bahasa Lo REPL ===")
    print("Ketik 'keluar' untuk keluar.")
    while True:
        prompt = prompt_str if current_folder=="." else f"{prompt_str} {os.path.basename(current_folder)}>"
        try:
            baris=input(prompt)
        except EOFError:
            print("\nKeluar")
            break
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            print("Session tersimpan. Bye!")
            break
        proses_baris(baris)

if __name__=="__main__":
    repl()
