import sys
sys.path.insert(0, '.')

try:
    from app import app
    print("✓ Successfully imported app.py")
    print(f"✓ App name: {app.name}")
    
    print("\n✓ Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  - {rule.endpoint}: {rule.rule}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()