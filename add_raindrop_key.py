"""Add Raindrop AI API key to .env file"""

# Read the current .env file
with open('.env', 'r') as f:
    lines = f.readlines()

# Update the RAINDROP_API_KEY line
updated_lines = []
for line in lines:
    if line.startswith('RAINDROP_API_KEY='):
        updated_lines.append('RAINDROP_API_KEY=lm_apikey_000afe58c3de4adfab37ef7b6de3fe8654f2e54acada43ae\n')
        print('✅ Updated RAINDROP_API_KEY')
    else:
        updated_lines.append(line)

# Write back to .env file
with open('.env', 'w') as f:
    f.writelines(updated_lines)

print('✅ Successfully saved to .env file!')
print('\nNext steps:')
print('1. Restart your server (Ctrl+C then run START_SERVER_HERE.bat)')
print('2. Your Raindrop AI key is now active!')
