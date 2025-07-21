# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

ROOT = os.getcwd()
TEMPLATE_EXE = os.path.join(ROOT, "templates", "python_helper_template.exe")

# 只打进这一个模板 exe
binaries = [(TEMPLATE_EXE, "eaters")]

# 需要的隐藏导入（psutil + 自己的词表）
hiddenimports = collect_submodules("psutil") 

block_cipher = None
a = Analysis(
    ["launcher.py"],
    pathex=[ROOT],
    binaries=binaries,
    datas=[],                 # ⚠️ 这里已无 wordfreq 数据
    hiddenimports=hiddenimports,
    strip=False,
    upx=False,                # 调通后再考虑 True
    cipher=block_cipher,
)

# ★ 一定带 a.zipped_data
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ★ 一定带 a.zipfiles，并指定图标
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="python service",
    console=False,
    icon="favicon.ico",       # ← 你的 ico 图标
    strip=False,
    upx=False,
)
