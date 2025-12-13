# test_import.py
import importlib, traceback

print("=== Starting import test ===")
try:
    import models
    print("Imported models OK")
except Exception:
    print("Import raised an exception:")
    traceback.print_exc()

# Try reloading to capture any further errors
print("\n=== Attempt reload ===")
try:
    importlib.reload(models)
    print("Reload OK")
except Exception:
    traceback.print_exc()

print("\n=== Module info (if available) ===")
try:
    print("models.__file__ =", models.__file__)
    print("Has User =", hasattr(models, "User"))
    print("Public names =", [n for n in dir(models) if not n.startswith('_')])
except Exception as e:
    print("Could not read module attributes:", e)
