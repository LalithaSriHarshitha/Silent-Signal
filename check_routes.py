"""Check what routes are registered"""
from backend.main import app

print("=" * 60)
print("REGISTERED ROUTES")
print("=" * 60)

for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        methods = ', '.join(route.methods)
        print(f"{methods:10} {route.path}")

print("=" * 60)
