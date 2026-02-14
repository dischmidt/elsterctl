import ctypes
import os
from pathlib import Path

lib_path = os.environ["ELSTER_ERIC_LIB"]
print("STEP:load", flush=True)
lib = ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
print("OK:load", flush=True)

plugin_path = str(Path(lib_path).resolve().parent / "plugins2").encode("utf-8")

init = lib.EricInitialisiere
init.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
init.restype = ctypes.c_int

print("STEP:init", flush=True)
rc = init(plugin_path, None)
print(f"OK:init rc={rc}", flush=True)

if rc == 0:
    end = lib.EricBeende
    end.argtypes = []
    end.restype = ctypes.c_int
    print("STEP:end", flush=True)
    rc2 = end()
    print(f"OK:end rc={rc2}", flush=True)
