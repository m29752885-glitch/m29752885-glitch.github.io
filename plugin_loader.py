# plugin_loader.py
# ======================
# Load dan manage plugin Bahasa-lo
# ======================

import os
import importlib.util

PLUGINS_FOLDER = "./downloads/plugins"
loaded_plugins = {}  # plugin aktif

# ======================
# Auto reload plugin tertentu
# ======================
def auto_reload_all():
    global loaded_plugins
    plugin_list = ["Explorer_fix", "Optimasi", "crash_handle, Manual, download_manager"]
    for plugin in plugin_list:
        path = os.path.join(PLUGINS_FOLDER, plugin + ".py")
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location(plugin, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            loaded_plugins[plugin] = mod
        else:
            print(f"⚠️ Plugin {plugin} tidak ditemukan")

# ======================
# Aktifkan plugin manual
# ======================
def activate_single_plugin(plugin_name):
    global loaded_plugins
    path = os.path.join(PLUGINS_FOLDER, plugin_name + ".py")

    if not os.path.exists(path):
        print(f"❌ Plugin {plugin_name} tidak ditemukan")
        return

    spec = importlib.util.spec_from_file_location(plugin_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    loaded_plugins[plugin_name] = mod
    print(f"✅ Plugin {plugin_name} diaktifkan")

    # ==========================
    # AUTO CALL SEMUA FUNCTION
    # ==========================
    for nama in dir(mod):
        attr = getattr(mod, nama)

        if (
            callable(attr)
            and not nama.startswith("_")      # skip private
            and nama not in ["os", "sys"]     # safety
        ):
            try:
                attr()
            except TypeError:
                # fungsi butuh argumen → skip
                pass
            except Exception as e:
                print(f"❌ Error di plugin {plugin_name}.{nama}()")
                print(e)
# ======================
# List plugin
# ======================
def list_plugins():
    if not os.path.exists(PLUGINS_FOLDER):
        print("❌ Folder plugin tidak ditemukan")
        return

    files = os.listdir(PLUGINS_FOLDER)
    plugins = [f[:-3] for f in files if f.endswith(".py")]

    if not plugins:
        print("⚠️ Tidak ada plugin")
        return

    print("=== Daftar Plugin ===")
    for p in plugins:
        status = "AKTIF" if p in loaded_plugins else "NONAKTIF"
        print(f"- {p} [{status}]")
  
