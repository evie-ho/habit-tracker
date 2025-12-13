# show_app_file.py
import importlib
m = importlib.import_module('app')
print("app module file:", m.__file__)
