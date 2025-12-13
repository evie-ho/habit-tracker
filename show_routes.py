# show_routes.py
from importlib import import_module
app = import_module('app').app
print("Routes (endpoint -> rule):")
for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
    print(f"{rule.endpoint:30} -> {rule}")
