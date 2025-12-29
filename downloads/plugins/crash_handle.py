# Plugin: Crash Handle
# Fungsinya: Menangkap error kecil di REPL agar tidak crash

def crash_wrapper(func):
    """Wrapper untuk menangkap exception"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n[!] Interupsi oleh user")
        except Exception as e:
            print(f"[!] Terjadi error: {e}")
    return wrapper

# Patch REPL eval/execution
if "repl" in globals():
    import types
    if isinstance(repl, types.FunctionType):
        asli_repl = repl
        repl = crash_wrapper(asli_repl)

print("[Plugin Crash Handle] Aktif: Error kecil tidak akan crash REPL")
