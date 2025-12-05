"""Test if WorkOS configuration is loaded correctly"""
from backend.config import settings

print("=" * 60)
print("WORKOS CONFIGURATION TEST")
print("=" * 60)

print(f"\nWORKOS_API_KEY: {settings.WORKOS_API_KEY[:20]}..." if settings.WORKOS_API_KEY else "WORKOS_API_KEY: (empty)")
print(f"WORKOS_CLIENT_ID: {settings.WORKOS_CLIENT_ID}")
print(f"WORKOS_REDIRECT_URI: {settings.WORKOS_REDIRECT_URI}")
print(f"WORKOS_COOKIE_PASSWORD: {settings.WORKOS_COOKIE_PASSWORD[:20]}..." if settings.WORKOS_COOKIE_PASSWORD else "WORKOS_COOKIE_PASSWORD: (empty)")

print("\n" + "=" * 60)

if settings.WORKOS_API_KEY and settings.WORKOS_CLIENT_ID:
    print("✅ WorkOS credentials are configured!")
    print("\nTrying to initialize WorkOS client...")
    try:
        from workos import WorkOSClient
        client = WorkOSClient(
            api_key=settings.WORKOS_API_KEY,
            client_id=settings.WORKOS_CLIENT_ID
        )
        print("✅ WorkOS client initialized successfully!")
    except Exception as e:
        print(f"❌ WorkOS client initialization failed: {e}")
else:
    print("❌ WorkOS credentials are NOT configured!")
    if not settings.WORKOS_API_KEY:
        print("   - WORKOS_API_KEY is missing")
    if not settings.WORKOS_CLIENT_ID:
        print("   - WORKOS_CLIENT_ID is missing")

print("=" * 60)
