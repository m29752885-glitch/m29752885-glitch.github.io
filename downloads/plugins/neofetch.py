# plugins/neofetch_bahasa_lo.py
import os, platform, time
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER

def tampilkan_neofetch():
    print("===================================")
    print("      Bahasa-Lo REPL Neofetch      ")
    print("===================================")
    
    try:
        print(f"OS      : {platform.system()} {platform.release()}")
    except: print("OS      : Tidak tersedia")
    
    try:
        print(f"Python  : {platform.python_version()}")
    except: print("Python  : Tidak tersedia")
    
    try:
        import psutil
        print(f"CPU     : {psutil.cpu_count()} cores | {psutil.cpu_percent()}% usage")
        print(f"RAM     : {psutil.virtual_memory().percent}% used")
    except: print("CPU/RAM : Tidak tersedia")
    
    print(f"Downloads : {len(os.listdir(DOWNLOADS_FOLDER))} file")
    print(f"Packages  : {len(os.listdir(PACKAGES_FOLDER))} file")
    print("===================================")

tampilkan_neofetch()
