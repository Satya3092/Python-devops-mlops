"""
Day 018 — String Slicing
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Slicing basics
# ======================================================================
word = "automation"
print(word[0:4])     # auto
print(word[4:])      # mation
print(word[:4])      # auto
print(word[-4:])     # tion
print(word[::2])     # every second character
print(word[::-1])    # reversed
print(word[2:100])   # out of range is fine

# ======================================================================
# Example 2 — Parsing a fixed-format log line
# ======================================================================
log_line = "2026-11-20 10:15:32 ERROR Database connection timeout"

date = log_line[0:10]
time = log_line[11:19]
year = log_line[:4]
month = log_line[5:7]
hour = log_line[11:13]
rest = log_line[20:]

print("Date:", date)
print("Time:", time)
print("Year:", year, "| Month:", month, "| Hour:", hour)
print("Message part:", rest)

# Docker image reference: get the tag after the colon
image = "nginx:1.27-alpine"
colon_position = image.index(":")      # position of ':' (method from Day 19)
print("Image name:", image[:colon_position])
print("Image tag:", image[colon_position + 1:])
