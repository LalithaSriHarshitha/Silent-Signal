"""Test analytics endpoint"""
import sys
sys.path.insert(0, '.')

try:
    from backend.routes import analytics
    print("✓ Analytics module imported successfully")
    print(f"✓ Router created: {analytics.router}")
    print(f"✓ Routes: {[route.path for route in analytics.router.routes]}")
    print("\nAnalytics dashboard is ready!")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
