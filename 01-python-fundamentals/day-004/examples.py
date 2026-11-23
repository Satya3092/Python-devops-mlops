"""
Day 004 — Python Literals
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Numbers in different bases
# ======================================================================
million = 1_000_000
binary_value = 0b1010
file_mode = 0o755
max_byte = 0xFF
big_float = 2.5e3

print("million:", million)
print("0b1010 =", binary_value)
print("0o755 =", file_mode)
print("0xFF  =", max_byte)
print("2.5e3 =", big_float)
print("755 in octal back to text:", oct(file_mode))

# ======================================================================
# Example 2 — Building a config file with string literals
# ======================================================================
# Multi-line string - perfect for a config template
nginx_config = """server {
    listen 80;
    server_name example.com;
}"""
print(nginx_config)

# Escape sequences
print("Name:\tweb-01\nStatus:\tUP")
print("He said \"deploy now\"")

# Raw string keeps backslashes (Windows path)
windows_path = r"C:\new\tools\terraform.exe"
print(windows_path)
