# Ultimate Bahasa-Lo REPL FINAL v6
import re, subprocess, time, sys, os, pickle

# ----------------------------
# Progress bar sederhana
# ----------------------------
def progress_bar(task_name, duration=1):
    print(f"{task_name}...", end="")
    sys.stdout.flush()
    for i in range(20):
        print("█", end="")
        sys.stdout.flush()
        time.sleep(duration/20)
    print(" Done!")

# ----------------------------
# Install package penting
# ----------------------------
required_packages = ["rsync","apt-mirror","git","wget","curl","proot-distro"]
for pkg in required_packages:
    try:
        print(f"\nMemeriksa package '{pkg}'...")
        subprocess.run(f"apt install -y {pkg}", shell=True)
        progress_bar(f"Installing {pkg}", 0.5)
    except:
        print(f"Gagal install {pkg}, lanjut saja")

# ----------------------------
# Setup global
# ----------------------------
variabel = {}
alias_perintah = {"Echo":"tulis"}
alias_keyword = {"jika":"if","apabila":"elif","Maka":":"}
macros = {}
log_file = "repl.log"
session_file = ".session"
downloads_folder = "./downloads"
plugins_folder = os.path.join(downloads_folder, "plugins")
repo_folder = "./repo"
repo_list_file = os.path.join(repo_folder,"repo.list")
os.makedirs(downloads_folder, exist_ok=True)
os.makedirs(plugins_folder, exist_ok=True)
os.makedirs(repo_folder, exist_ok=True)
prompt_str = "(+)> "
current_folder = "."  # folder aktif

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
        expr = re.sub(r'\b'+var+r'\b', str(variabel[var]), expr)
    try:
        return eval(expr)
    except:
        return expr.strip('"')

# ----------------------------
# File manager versi Linux vibes clean
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
# Check mirror ala Termux
# ----------------------------
def check_mirror(url):
    try:
        result = subprocess.run(f"curl -Is {url}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except:
        return False

# ----------------------------
# Proses perintah utama
# ----------------------------
def proses_baris(b):
    b = b.strip()
    if b == "" or b.startswith("#"):
        return None

    global prompt_str, current_folder

    # =============================
    # Admin menu
    # =============================
    if b.lower() == "admin":
        password = input("Masukkan password admin: ").strip()
        if password != "rahasia123":
            print("Password salah!")
            return None

        while True:
            print("\n=== Admin Menu ===")
            print("1. Repo GitHub manual")
            print("2. Repo Linux")
            print("3. Tambah repo lokal (/repo/repo.list)")
            print("4. Edit mirror (/repo/repo.list)")
            print("q. Keluar admin")
            choice = input("Pilih opsi: ").strip().lower()
            if choice=="q":
                break

            # Tambah repo lokal manual
            if choice == "3":
                url = input("Masukkan URL repo: ").strip()
                with open(repo_list_file,"a") as f:
                    f.write(url+"\n")
                print(f"Repo {url} berhasil ditambahkan ke repo.list")

            # Edit mirror
            elif choice=="4":
                with open(repo_list_file,"r") as f:
                    repos = [line.strip() for line in f if line.strip()]
                while True:
                    print("\nDaftar mirror:")
                    for i,r in enumerate(repos,1):
                        print(f"{i}. {r}")
                    print("a = tambah, e = edit, d = hapus, q = keluar")
                    aksi = input("Pilihan: ").strip().lower()
                    if aksi=="q":
                        break
                    elif aksi=="a":
                        url = input("Masukkan URL mirror baru: ").strip()
                        repos.append(url)
                    elif aksi=="e":
                        idx = int(input("Pilih nomor mirror untuk edit: ").strip())-1
                        if 0<=idx<len(repos):
                            url = input("Masukkan URL baru: ").strip()
                            repos[idx]=url
                    elif aksi=="d":
                        idx = int(input("Pilih nomor mirror untuk hapus: ").strip())-1
                        if 0<=idx<len(repos):
                            repos.pop(idx)
                # Simpan
                with open(repo_list_file,"w") as f:
                    for r in repos:
                        f.write(r+"\n")
                print("Mirror list berhasil diperbarui!")

            # Pilihan lain bisa ditambah
            else:
                print("Pilihan admin tidak valid!")
        return None

    # =============================
    # Proot-distro
    # =============================
    if b.lower() == "linux":
        result = subprocess.getoutput("proot-distro list")
        lines = result.splitlines()
        print("Distro tersedia:")
        distro_status = {}
        for line in lines:
            line = line.strip()
            if line.startswith("*"):
                name = line[1:].strip()
                print(f"{name} (installed)")
                distro_status[name] = True
            elif line:
                print(line)
                distro_status[line] = False

        distro = input("Pilih distro: ").strip()
        if distro:
            if not distro_status.get(distro, False):
                print(f"Distro {distro} belum terinstall. Menginstall sekarang...")
                subprocess.run(f"proot-distro install {distro}", shell=True)
                print(f"{distro} selesai diinstall!")
            print(f"Login ke {distro} ...")
            subprocess.run(f"proot-distro login {distro}", shell=True)
        return None

    # =============================
    # Plugin system
    # =============================
    if b.startswith("plugin"):
        if b.strip() == "plugin -m":
            plugins = [f for f in os.listdir(plugins_folder) if f.endswith(".py")]
            if not plugins:
                print("Belum ada plugin.")
            else:
                print("Plugin tersedia:")
                for i,p in enumerate(plugins,1):
                    print(f"{i}. {p}")
                choice = input("Pilih plugin untuk aktifkan (nomor): ").strip()
                if choice.isdigit() and 1<=int(choice)<=len(plugins):
                    plugin_path = os.path.join(plugins_folder, plugins[int(choice)-1])
                    try:
                        exec(open(plugin_path).read(), globals())
                        print("Plugin aktif!")
                    except Exception as e:
                        print("Gagal aktifkan plugin:", e)
            return None
        elif b.strip() == "plugin":
            print("Menu Plugin:")
            print("1. Buat file sendiri")
            print("2. Upload dari GitHub")
            choice = input("Pilih opsi: ").strip()
            if choice=="1":
                filename = input("Nama file plugin (.py): ").strip()
                path = os.path.join(plugins_folder, filename)
                with open(path,"w") as f:
                    f.write("# Plugin baru\n")
                print(f"Plugin {filename} berhasil dibuat di {plugins_folder}")
            elif choice=="2":
                url = input("Masukkan URL GitHub plugin (.py): ").strip()
                out_file = os.path.join(plugins_folder, url.split("/")[-1])
                subprocess.run(f"wget -O {out_file} {url}", shell=True)
                print(f"Plugin tersimpan di {out_file}")
            return None

    # =============================
    # PIT system
    # =============================
    if b.startswith("pit "):
        args = b.split()
        if len(args)<3:
            print("Gunakan: pit search/show/install <package>")
            return None
        cmd = args[1]
        pkg = args[2]

        # Load repo list
        if not os.path.exists(repo_list_file):
            print("repo.list kosong!")
            return None
        with open(repo_list_file,"r") as f:
            repos = [line.strip() for line in f if line.strip()]

        # Check mirrors
        mirror_status={}
        print("Testing available mirror:")
        for r in repos:
            status = "ok" if check_mirror(r) else "bad"
            mirror_status[r]=status
            print(f"{r} : {status}")
        ok_repos = [r for r,s in mirror_status.items() if s=="ok"]
        if not ok_repos:
            print("Tidak ada mirror yang tersedia!")
            return None

        # PIT SEARCH
        if cmd=="search":
            hasil = [r for r in ok_repos if pkg.lower() in r.lower()]
            if hasil:
                print("Hasil pencarian:")
                for h in hasil: print(" -",h)
            else:
                print("Tidak ditemukan package yang cocok.")
            return None

        # PIT SHOW
        elif cmd=="show":
            found=False
            for r in ok_repos:
                if r.split("/")[-1].replace(".git","")==pkg:
                    print(f"Info package {pkg}: {r}")
                    found=True
                    break
            if not found:
                print(f"Package '{pkg}' tidak ditemukan")
            return None

        # PIT INSTALL
        elif cmd=="install":
            found=False
            for r in ok_repos:
                if r.split("/")[-1].replace(".git","")==pkg:
                    found=True
                    out_dir = os.path.join(downloads_folder,pkg)
                    print(f"Cloning {r} ke {out_dir} ...")
                    subprocess.run(f"git clone {r} {out_dir}", shell=True)
                    break
            if not found:
                print(f"Package '{pkg}' tidak ditemukan")
            return None
        else:
            print("Command pit tidak valid")
            return None

    # =============================
    # Command Linux biasa
    # =============================
    if b.startswith("apt "):
        subprocess.run(b, shell=True)
        return None

    # =============================
    # Assignment / tulis / cd / ls / cat / pindah / backup / root
    # =============================
    # ... (pertahankan semua fungsi sebelumnya dari versi final v5)
    # Misal tulis, cd, ls, cat, pindah, simpan, root -a

    return None

# ----------------------------
# REPL
# ----------------------------
def repl():
    print("\n=== Ultimate Bahasa Lo REPL FINAL v6 ===")
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
