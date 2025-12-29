# ----------------------------
# main.py - Ultimate Bahasa-Lo REPL Final
# ----------------------------

import os, sys, subprocess, pickle, time, re
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, LOADING_MSGS, progress_bar, PROGRESS_SPEED

# ----------------------------
# Setup global
# ----------------------------
variabel = {}
macros = {}
alias_perintah = {"Echo":"tulis"}
alias_keyword = {"jika":"if","apabila":"elif","Maka":":"}
prompt_str = "(+)> "
current_folder = "."
plugins_folder = os.path.join(DOWNLOADS_FOLDER, "plugins")
os.makedirs(plugins_folder, exist_ok=True)
session_file = ".session"
log_file = "repl.log"

# ----------------------------
# Load session sebelumnya
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
        expr = re.sub(r'\b'+var+r'\b', str(variabel[var]), expr)
    try:
        return eval(expr)
    except:
        return expr.strip('"')

# ----------------------------
# File manager Linux vibes
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
# Proses baris REPL
# ----------------------------
def proses_baris(b):
    b = b.strip()
    if b == "" or b.startswith("#"):
        return None

    global prompt_str, current_folder

    # Admin mode
    if b.lower() == "admin":
        password = input("Masukkan password admin: ").strip()
        if password == "12345":
            print("=== Mode Admin Aktif ===")
            while True:
                print("\nMenu Admin:")
                print("1. Tambah repo / kelola repo")
                print("2. Kelola file system")
                print("3. Keluar admin")
                choice = input("Pilih opsi: ").strip()
                if choice=="1":
                    print("Tambah repo / mirror dapat dilakukan disini (future feature).")
                elif choice=="2":
                    print(f"Folder admin: {ADMIN_FOLDER}")
                elif choice=="3":
                    print("Keluar admin")
                    break
                else:
                    print("Pilihan salah!")
        else:
            print("Password salah!")
        return None

    # Proot-distro
    if b.lower() == "linux":
        result = subprocess.getoutput("proot-distro list")
        lines = result.splitlines()
        distro_status = {}
        print("Distro tersedia:")
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
            if not distro_status.get(distro, False):
                print(f"Install {distro}...")
                subprocess.run(f"proot-distro install {distro}", shell=True)
            print(f"Login ke {distro} ...")
            subprocess.run(f"proot-distro login {distro}", shell=True, cwd=PACKAGES_FOLDER)
        return None

    # Plugin system
    if b.startswith("plugin"):
        if b.strip() == "plugin -m":
            plugins = [f for f in os.listdir(plugins_folder) if f.endswith(".py")]
            if not plugins:
                print("Belum ada plugin.")
            else:
                print("Plugin tersedia:")
                for i, p in enumerate(plugins, 1):
                    print(f"{i}. {p}")
                choice = input("Pilih plugin (nomor): ").strip()
                if choice.isdigit() and 1<=int(choice)<=len(plugins):
                    path = os.path.join(plugins_folder, plugins[int(choice)-1])
                    try:
                        exec(open(path).read(), globals())
                        print("Plugin aktif!")
                    except Exception as e:
                        print("Gagal aktifkan plugin:", e)
            return None
        elif b.strip() == "plugin":
            print("Menu Plugin:")
            print("1. Buat file plugin sendiri")
            print("2. Upload dari GitHub")
            choice = input("Pilih opsi: ").strip()
            if choice=="1":
                filename = input("Nama file plugin (.py): ").strip()
                path = os.path.join(plugins_folder, filename)
                with open(path,"w") as f:
                    f.write("# Plugin baru\n")
                print(f"Plugin {filename} dibuat di folder {plugins_folder}")
            elif choice=="2":
                url = input("Masukkan URL plugin (.py): ").strip()
                out_file = os.path.join(plugins_folder, url.split("/")[-1])
                subprocess.run(f"wget -O {out_file} {url}", shell=True)
                print(f"Plugin tersimpan di {out_file}")
            return None

    # Macro
    if b in macros:
        subprocess.run(macros[b], shell=True)
        return None

    # Aliasing command
    for a in alias_perintah:
        if b.startswith(a+" "):
            b = b.replace(a, alias_perintah[a], 1)
    for k in alias_keyword:
        b = re.sub(r'\b'+k+r'\b', alias_keyword[k], b)

    # Assignment
    if "=" in b and not b.startswith("if") and not b.startswith("elif"):
        key,val = b.split("=",1)
        variabel[key.strip()] = evaluasi_ekspresi(val.strip())
        return None

    # tulis
    if b.startswith("tulis "):
        isi = b[6:].strip()
        out = evaluasi_ekspresi(isi)
        print(out)
        log(b,out)
        return None

    # jalankan file .blo
    if b.startswith("jalankan "):
        f = os.path.join(current_folder, b[9:].strip())
        if os.path.exists(f):
            with open(f) as file:
                exec(file.read(), globals(), variabel)
        else:
            print(f"File {f} tidak ditemukan!")
        return None

    # CD command
    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder == "/":
            current_folder = "."
        else:
            target = os.path.join(current_folder, folder)
            if os.path.isdir(target):
                current_folder = os.path.abspath(target)
            else:
                print(f"Folder '{folder}' tidak ditemukan!")
        return None

    if b.strip() == "keluar_folder":
        current_folder = "."
        return None

    # File explorer
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return None
    if b.startswith("cat "):
        file = os.path.join(current_folder, b[4:].strip())
        if os.path.exists(file):
            out = subprocess.getoutput(f"head -n 10 {file}")
            print(out)
            log(b,out)
        else:
            print(f"File '{file}' tidak ditemukan!")
        return None

    # pindah file
    if b.startswith("pindah "):
        parts = b.split()
        if len(parts)<3:
            print("Format: pindah <nama_file> <folder_tujuan>")
            return None
        src = os.path.join(current_folder, parts[1])
        dst_folder = parts[2]
        os.makedirs(dst_folder, exist_ok=True)
        dst = os.path.join(dst_folder, parts[1])
        try:
            os.rename(src,dst)
            print(f"{parts[1]} dipindah ke {dst_folder}/")
        except Exception as e:
            print("Gagal memindah file:", e)
        return None

    # root mode
    if b.strip() == "root -a":
        prompt_str = "[Root]> "
        print("Prompt REPL sekarang menjadi [Root]>")
        return None

    # Bantuan
    if b.lower() == "bantuan":
        print("\n=== MENU BANTUAN ===")
        print("Command umum:")
        print("  tulis <isi>          -> tampilkan teks")
        print("  <variabel> = <nilai> -> assignment variabel")
        print("  jika / apabila / Maka -> kondisi")
        print("  jalankan <file.blo>  -> jalankan file .blo")
        print("\nFile Explorer:")
        print("  ls [folder]           -> list isi folder")
        print("  cd <folder>           -> pindah folder")
        print("  keluar_folder         -> kembali ke root folder")
        print("  cat <file>            -> lihat isi file (10 baris pertama)")
        print("  pindah <file> <folder> -> pindahkan file")
        print("\nPlugin System:")
        print("  plugin                -> menu plugin")
        print("  plugin -m             -> aktifkan plugin")
        print("\nRoot Mode:")
        print("  root -a               -> ubah prompt menjadi [Root]>")
        print("\nAdmin Mode:")
        print("  admin                 -> masuk mode admin (password diperlukan)")
        print("\nKeluar REPL:")
        print("  keluar / exit         -> keluar REPL dan simpan session\n")
        return None

    # Semua command lain
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
        log(b)
    except:
        print("Terjadi kesalahan menjalankan:", b)
    return None

# ----------------------------
# REPL
# ----------------------------
def repl():
    print("\n=== Ultimate Bahasa-Lo REPL Final ===")
    print("Ketik 'bantuan' untuk melihat command, 'keluar' untuk keluar.")
    global current_folder, prompt_str
    kode_multi=""
    while True:
        if current_folder == ".":
            prompt = "[Root]> " if prompt_str.startswith("[Root]") else "(+)> "
        else:
            prompt = f"[Root]/{os.path.basename(current_folder)}> " if prompt_str.startswith("[Root]") else f"(+) / {os.path.basename(current_folder)}> "
        baris = input(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            print("Session tersimpan. Bye!")
            break
        kode = proses_baris(baris)
        if kode:
            kode_multi += kode+"\n"
        if kode_multi and not baris.strip().endswith(":"):
            try:
                exec(kode_multi, globals(), variabel)
            except Exception as e:
                print("Error:", e)
            kode_multi = ""

if __name__=="__main__":
    repl()
