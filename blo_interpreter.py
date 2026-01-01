# blo_interpreter.py
# Interpreter Bahasa-lo (.blo)

import re

# ==========================
# Kamus Bahasa Indonesia → Python
# ==========================
KAMUS = {
    # I/O
    r'\btulis\b': 'print',
    r'\bmasukan\b': 'input',

    # Tipe data
    r'\bbulat\b': 'int',
    r'\bpecahan\b': 'float',
    r'\bteks\b': 'str',
    r'\bdaftar\b': 'list',
    r'\bkamus\b': 'dict',
    r'\btipe\b': 'type',
    r'\bpanjang\b': 'len',

    # Logika
    r'\bjika\b': 'if',
    r'\bapabila\b': 'elif',
    r'\blainnya\b': 'else',
    r'\bdan\b': 'and',
    r'\batau\b': 'or',
    r'\btidak\b': 'not',

    # Loop
    r'\buntuk\b': 'for',
    r'\bselama\b': 'while',
    r'\bhentikan\b': 'break',
    r'\blanjutkan\b': 'continue',

    # Fungsi
    r'\bfungsi\b': 'def',
    r'\bkembalikan\b': 'return',

    # Import
    r'\bimpor\b': 'import',
    r'\bdari\b': 'from',
    r'\bsebagai\b': 'as',

    # Error handling
    r'\bcoba\b': 'try',
    r'\bkecuali\b': 'except',
    r'\bakhirnya\b': 'finally',

    # Nilai khusus
    r'\bBenar\b': 'True',
    r'\bSalah\b': 'False',
    r'\bKosong\b': 'None',
}

# ==========================
# Translate kode .blo → Python
# ==========================
def translate_blo(kode_blo: str) -> str:
    kode_python = kode_blo

    # ganti keyword
    for pola, pengganti in KAMUS.items():
        kode_python = re.sub(pola, pengganti, kode_python)

    # otomatis tambahin () ke print jika lupa
    kode_python = re.sub(
        r'print\s+"([^"]+)"',
        r'print("\1")',
        kode_python
    )

    return kode_python


# ==========================
# Jalankan file .blo
# ==========================
def jalankan_blo(path: str, debug=False):
    with open(path, "r") as f:
        kode_blo = f.read()

    kode_python = translate_blo(kode_blo)

    if debug:
        print("=== HASIL TRANSLATE ===")
        print(kode_python)
        print("=======================")

    try:
        exec(kode_python, {})
    except Exception as e:
        print("❌ Error saat menjalankan .blo")
        print(e)
      
