"""Generate a secure cookie password for WorkOS"""
import secrets

password = secrets.token_hex(32)
print("=" * 60)
print("NEW COOKIE PASSWORD GENERATED")
print("=" * 60)
print(password)
print("=" * 60)
print("\nCopy this and paste it in your .env file:")
print(f"WORKOS_COOKIE_PASSWORD={password}")
