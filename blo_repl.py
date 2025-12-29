# blo_repl.py
# REPL untuk Bahasa-lo (.blo)

from blo_interpreter import translate_blo
import sys

# ==========================
# Globals untuk REPL
# ==========================
KONTEKS = {}

# ==========================
# REPL .blo
# ==========================
def repl_blo(debug=False):
    buffer = []
    print("=== Bahasa-lo REPL (.blo) ===")
    print("Ketik 'exit' untuk keluar, 'run filename.blo' untuk jalankan file .blo")
    
    while True:
        try:
            baris = input(">>> ")
            
            # exit
            if baris.strip().lower() == "exit":
                print("Keluar dari REPL .blo")
                break

            # jalankan file .blo
            if baris.strip().startswith("run "):
                path_file = baris.strip()[4:]
                try:
                    with open(path_file, "r") as f:
                        kode_file = f.read()
                    kode_python = translate_blo(kode_file)
                    if debug:
                        print("=== HASIL TRANSLATE ===")
                        print(kode_python)
                        print("=======================")
                    exec(kode_python, KONTEKS)
                except FileNotFoundError:
                    print(f"❌ File {path_file} tidak ditemukan")
                continue

            # simpan baris ke buffer
            buffer.append(baris)

            # jika baris kosong, eksekusi buffer
            if baris.strip() == "":
                kode = "\n".join(buffer)
                kode_python = translate_blo(kode)
                if debug:
                    print("=== HASIL TRANSLATE ===")
                    print(kode_python)
                    print("=======================")
                try:
                    exec(kode_python, KONTEKS)
                except Exception as e:
                    print("❌ Error saat menjalankan kode .blo")
                    print(e)
                buffer = []

        except KeyboardInterrupt:
            print("\nKeluar dari REPL .blo")
            break

# ==========================
# Jalankan langsung REPL
# ==========================
if __name__ == "__main__":
    repl_blo(debug=False)
