# fix_json.py
import io

# Read as UTF-16 (Windows default when using > redirection in PowerShell)
with io.open("data.json", "r", encoding="utf-16") as f:
    content = f.read()

# Write back clean UTF-8 without BOM
with io.open("data_clean.json", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Converted from UTF-16 to clean UTF-8 (data_clean.json)")
