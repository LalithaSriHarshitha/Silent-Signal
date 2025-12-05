"""Update .env file for local development"""
import os

# Read .env.example
with open('.env.example', 'r') as f:
    content = f.read()

# Replace values
content = content.replace(
    'SECRET_KEY=your-secret-key-change-this-in-production',
    'SECRET_KEY=9439ee72357a1a145f33975a5b8e59dd4f4d480835067079708fe7a1878c3b2e'
)
content = content.replace(
    'DATABASE_URL=postgresql://silentsignal:password@localhost:5432/silentsignal_db',
    'DATABASE_URL=sqlite:///./silentsignal.db'
)
content = content.replace(
    'REDIS_URL=redis://localhost:6379/0',
    'REDIS_URL='
)

# Write to .env
with open('.env', 'w') as f:
    f.write(content)

print(".env file updated successfully!")
print("- Using SQLite database")
print("- Redis disabled")
print("- Secret key generated")
