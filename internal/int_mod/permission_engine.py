# permission_engine.py
# =========================
# Permission Engine Bahasa-lo
# Backend only (SILENT)
# =========================

import os

# =========================
# RULE SET
# =========================
PERMISSIONS = {
    "user": {
        "read": ["./downloads"],
        "write": ["./downloads"],
        "exec": []
    },
    "root": {
        "read": ["./downloads"],
        "write": [],
        "exec": ["linux"]
    },
    "admin": {
        "read": ["./"],
        "write": ["./"],
        "exec": ["linux", "plugin", "system"]
    }
}

# =========================
# INIT
# =========================
def init(ctx):
    ctx["cek_izin"] = cek_izin
    ctx["izin_baca"] = izin_baca
    ctx["izin_tulis"] = izin_tulis
    ctx["izin_exec"] = izin_exec

# =========================
# CORE CHECK
# =========================
def cek_izin(level, aksi, target):
    if level not in PERMISSIONS:
        return False

    rules = PERMISSIONS[level].get(aksi, [])
    for path in rules:
        if target.startswith(path) or path == "./":
            return True
    return False

# =========================
# HELPERS
# =========================
def izin_baca(level, path):
    return cek_izin(level, "read", path)

def izin_tulis(level, path):
    return cek_izin(level, "write", path)

def izin_exec(level, cmd):
    return cek_izin(level, "exec", cmd)
  
