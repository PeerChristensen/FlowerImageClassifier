import os

directory = os.listdir("data")

for folder in directory:
    
    dir = os.listdir(f"data/{folder}")
    n = len(dir)
    if n == 0:
        os.rmdir(f"data/{folder}")