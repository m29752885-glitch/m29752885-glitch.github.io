# agent_adaptive.py
# AI Adaptive Bahasa-lo (.blo) - Function based, tetap pakai nama AgentAdaptive

import os
from info import INFO
from blo_interpreter import jalankan_blo

def AgentAdaptive(debug=False):
    known_files = set()
    known_plugins = set()

    print("=== Agent Adaptive Bahasa-lo ===")
    print("Ketik 'keluar' untuk berhenti, 'scan' untuk cek file .blo baru, 'jalankan nama.blo' untuk run file .blo")

    while True:
        try:
            cmd = input("agent> ").strip()

            if cmd.lower() == "keluar":
                print("🛑 Keluar dari Agent Adaptive")
                break

            elif cmd.lower() == "scan":
                folder = "./downloads"
                os.makedirs(folder, exist_ok=True)
                files = os.listdir(folder)
                new_files = [f for f in files if f.endswith(".blo") and f not in known_files]
                for nf in new_files:
                    print(f"📌 File .blo baru terdeteksi: {nf}")
                    known_files.add(nf)
                if not new_files:
                    print("✅ Tidak ada file .blo baru")

            elif cmd.startswith("jalankan "):
                path_file = cmd.split(" ", 1)[1]
                if os.path.exists(path_file):
                    print(f"🚀 Menjalankan {path_file} ...")
                    try:
                        jalankan_blo(path_file, debug=debug)
                    except Exception as e:
                        print(f"❌ Error saat menjalankan {path_file}: {e}")
                else:
                    print(f"❌ File {path_file} tidak ditemukan")

            else:
                related_topics = [k for k in INFO if cmd.lower() in k.lower()]
                if related_topics:
                    print("🤖 Agent meninjau topik terkait...")
                    for topic in related_topics:
                        print(f"💡 {topic}: {INFO[topic]}")
                elif cmd in INFO:
                    print(f"💡 Tips untuk '{cmd}': {INFO[cmd]}")
                else:
                    print(f"⚠️ Command atau topik '{cmd}' belum ada di info.py")

        except KeyboardInterrupt:
            print("\n🛑 Agent dihentikan")
            break
