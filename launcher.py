# launcher.py
import subprocess, psutil, pathlib, time, os, sys, tempfile, shutil
MB = 1024 ** 2
RATIO = 0.99
CHUNK_SIZE = 20 * MB
SPAWN_DELAY = 1
TEMPLATE    = "python_helper_template.exe"   # 仅此一份

def bundle_dir() -> pathlib.Path:
    return pathlib.Path(getattr(sys, "_MEIPASS", pathlib.Path(__file__).parent)) / "eaters"



def main():
    total = psutil.virtual_memory().total
    target = int(total * RATIO)

    print(f"➡️  目标 {target//MB} MiB，持续启动进程...")

    idx = 0
    try:
        while True:
            # 每次循环时创建新的 helper
            tmpl = bundle_dir() / TEMPLATE
            if not tmpl.exists():
                print(f"❌ 模板不存在: {tmpl}"); sys.exit(1)

            workdir = pathlib.Path(tempfile.mkdtemp(prefix="helpers_"))
            dst = workdir / f"Window  Sevice C++ Platform {idx + 1:07d}.exe"
            try:
                os.link(tmpl, dst)  # 硬链接
            except OSError:
                shutil.copy2(tmpl, dst)  # 回退复制（极少数文件系统不支持）

            # 启动新进程
            try:
                subprocess.Popen([str(dst), str(CHUNK_SIZE)],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  ▶ 已启动 {idx + 1}: {dst.name}")
            except:
                pass
            time.sleep(SPAWN_DELAY)
            idx += 1
    except KeyboardInterrupt:
        sys.exit(0)



if __name__ == "__main__":
    main()
