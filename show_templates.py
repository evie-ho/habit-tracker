# show_templates.py
import os
p = os.path.abspath('templates')
print("templates folder:", p)
print("files:", sorted(os.listdir('templates')) if os.path.exists('templates') else [])
