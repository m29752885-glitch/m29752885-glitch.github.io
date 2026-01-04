import requests
import os

GITHUB_USER = "biasa132"
GITHUB_REPO = "Bahasa-lo"
LOCAL_VERSION_FILE = "./version.txt"

def get_latest_release():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            return data["tag_name"], data["body"]
    except Exception as e:
        print(f"⚠ Gagal cek update: {e}")
    return None, None

def read_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return None

def write_local_version(version):
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(version)

def check_update():
    latest_version, changelog = get_latest_release()
    if not latest_version:
        return

    local_version = read_local_version()
    if local_version != latest_version:
        print(f"⚡ Ada update baru Bahasa-lo! {latest_version}")
        print("📝 Changelog:")
        print(changelog)
        # update version.txt supaya selanjutnya gak muncul lagi
        write_local_version(latest_version)
    else:
        print("✅ Bahasa-lo sudah versi terbaru!")

if __name__ == "__main__":
    check_update()
