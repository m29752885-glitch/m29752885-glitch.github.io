# admin/plugins/admin_control.py
import os
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER

# Hanya jalankan kalau mode admin aktif
if not globals().get("ADMIN_MODE", False):
    print("Plugin Admin Control: Hanya bisa digunakan di mode ADMIN!")
else:
    print("=== Admin Control Plugin Aktif ===")
    folders = {
        "downloads": DOWNLOADS_FOLDER,
        "packages": PACKAGES_FOLDER,
        "admin": ADMIN_FOLDER,
        "backup": BACKUP_FOLDER
    }

    while True:
        print("\nMenu Admin Control:")
        print("1. Lihat folder")
        print("2. Buat folder baru")
        print("3. Pindah file")
        print("4. Hapus file/folder")
        print("5. Keluar plugin")

        pilihan = input("Pilih opsi: ").strip()

        if pilihan == "1":
            for nama, path in folders.items():
                print(f"\nFolder {nama}: {path}")
                if os.path.exists(path):
                    for f in os.listdir(path):
                        print(f"  - {f}")
                else:
                    print("  (tidak ada)")
        elif pilihan == "2":
            nama_folder = input("Nama folder baru: ").strip()
            path_folder = input("Lokasi folder (misal downloads): ").strip()
            target = folders.get(path_folder.lower(), None)
            if target:
                os.makedirs(os.path.join(target, nama_folder), exist_ok=True)
                print(f"Folder '{nama_folder}' dibuat di {target}")
            else:
                print("Lokasi tidak valid!")
        elif pilihan == "3":
            src = input("File yang mau dipindah: ").strip()
            dst = input("Tujuan folder: ").strip()
            src_path = None
            dst_path = None
            for p in folders.values():
                if os.path.exists(os.path.join(p, src)):
                    src_path = os.path.join(p, src)
                if os.path.exists(os.path.join(p, dst)):
                    dst_path = os.path.join(p, dst)
            if src_path and dst_path:
                os.rename(src_path, os.path.join(dst_path, src))
                print(f"{src} berhasil dipindah ke {dst}")
            else:
                print("File atau tujuan tidak ditemukan!")
        elif pilihan == "4":
            target = input("Masukkan file/folder yang mau dihapus: ").strip()
            found = False
            for p in folders.values():
                path_target = os.path.join(p, target)
                if os.path.exists(path_target):
                    if os.path.isfile(path_target):
                        os.remove(path_target)
                    else:
                        import shutil
                        shutil.rmtree(path_target)
                    print(f"{target} berhasil dihapus!")
                    found = True
                    break
            if not found:
                print("File/folder tidak ditemukan!")
        elif pilihan == "5":
            print("Keluar dari Admin Control Plugin")
            break
        else:
            print("Opsi tidak valid!")
