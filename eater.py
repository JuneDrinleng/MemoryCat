# eater.py
"""
按命令行参数分配指定字节后常驻。
用法: eater.exe 104857600   # 分 100 MiB
"""
import os, sys, time

size = int(sys.argv[1]) if len(sys.argv) > 1 else 100 * 1024**2
chunk = b'0' * size
print(f"[PID {os.getpid()}] allocated {size/1024**2:.0f} MiB, sleeping…")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    pass
