# launcher.py
import subprocess, psutil, pathlib, time, os, sys, tempfile, shutil
MB = 1024 ** 2
RATIO = 0.99
CHUNK_SIZE = 20 * MB
SPAWN_DELAY = 0.5
TEMPLATE    = "python_helper_template.exe"   # 仅此一份

def bundle_dir() -> pathlib.Path:
    return pathlib.Path(getattr(sys, "_MEIPASS", pathlib.Path(__file__).parent)) / "eaters"

def make_helper_links(need: int) -> list[pathlib.Path]:
    tmpl = bundle_dir() / TEMPLATE
    if not tmpl.exists():
        print(f"❌ 模板不存在: {tmpl}"); sys.exit(1)

    workdir = pathlib.Path(tempfile.mkdtemp(prefix="helpers_"))
    helpers = []
    for i in range(1, need + 1):
        dst = workdir / f"Window Systenn Sevice For Helping Pythen {i:07d}.exe"
        try:
            os.link(tmpl, dst)        # ★ 硬链接
        except OSError:
            shutil.copy2(tmpl, dst)   # 回退复制（极少数文件系统不支持）
        helpers.append(dst)
    return helpers

def main():
    total = psutil.virtual_memory().total
    target = int(total * RATIO)
    need   = (target + CHUNK_SIZE - 1) // CHUNK_SIZE

    helpers = make_helper_links(need)
    print(f"➡️  目标 {target//MB} MiB，需要 {need} 个进程")

    for idx, exe in enumerate(helpers, 1):
        subprocess.Popen([str(exe), str(CHUNK_SIZE)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  ▶ 已启动 {idx}/{need}: {exe.name}")
        time.sleep(SPAWN_DELAY)

    print("✅ 全部 helper 运行中，Ctrl-C 退出启动器")
    try:
        while True: time.sleep(60)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
