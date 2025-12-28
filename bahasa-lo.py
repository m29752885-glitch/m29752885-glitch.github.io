# bahasalo.py - Mini REPL Interpreter Bahasa Lo (Progress Install)
import re
import subprocess
import sys

variabel = {}
alias_perintah = {"Echo": "tulis"}
alias_keyword = {"jika": "if", "apabila": "elif", "Maka": ":"}

def evaluasi_ekspresi(ekspresi):
    for var in variabel:
        ekspresi = re.sub(r'\b' + var + r'\b', str(variabel[var]), ekspresi)
    try:
        return eval(ekspresi)
    except Exception:
        return ekspresi.strip('"')

def proses_baris(b):
    b = b.strip()
    if b == "" or b.startswith("#"):
        return None

    # Ganti alias perintah
    for a in alias_perintah:
        if b.startswith(a + " "):
            b = b.replace(a, alias_perintah[a], 1)

    # Ganti alias keyword
    for k in alias_keyword:
        b = re.sub(r'\b' + k + r'\b', alias_keyword[k], b)

    # Variabel assignment
    if "=" in b and not b.startswith("if") and not b.startswith("elif"):
        key, val = b.split("=", 1)
        key = key.strip()
        val = evaluasi_ekspresi(val.strip())
        variabel[key] = val
        return None

    # tulis perintah (ganti print)
    if b.startswith("tulis "):
        isi = b[6:].strip()
        print(evaluasi_ekspresi(isi))
        return None

    # apt install via system dengan progress sederhana
    if b.startswith("apt install "):
        paket = b[12:].strip()
        print(f"Menjalankan: apt install {paket}")
        try:
            # Panggil apt dengan -y
            process = subprocess.Popen(
                ["apt", "install", "-y", paket],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            # Baca output real-time
            for line in process.stdout:
                line = line.strip()
                if line:
                    # Progress sederhana: tampilkan line yang muncul
                    sys.stdout.write(f"\r{line[:70]}")  # batasi panjang line
                    sys.stdout.flush()
            print()  # pindah baris setelah selesai
        except Exception as e:
            print("Error menjalankan apt:", e)
        return None

    return b

def repl():
    print("Selamat datang di Mini Bahasa Lo (REPL Aman + Progress Install)")
    print("Ketik 'keluar' untuk keluar.")
    kode_multi = ""
    while True:
        prompt = "(+)> " if kode_multi == "" else "....> "
        baris = input(prompt)
        if baris.lower() in ["keluar", "exit"]:
            print("Bye!")
            break

        kode = proses_baris(baris)
        if kode:
            kode_multi += kode + "\n"

        if kode_multi and not baris.strip().endswith(":"):
            try:
                exec(kode_multi, globals(), variabel)
            except Exception as e:
                print("Error:", e)
            kode_multi = ""

if __name__ == "__main__":
    repl()
