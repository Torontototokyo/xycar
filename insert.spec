# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/work_card/insert.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'sqlalchemy',
        'pymysql',
        'pandas',
        'pandas._libs.tslibs.timedeltas',   # 解决常见 _TSObject 错误[citation:3][citation:8]
        'pandas._libs.tslibs.np_datetime',  # 解决 C 扩展相关错误[citation:7]
        'pandas._libs.tslibs.nattype',      # 另一个常见的 C 扩展依赖[citation:7]
        'pandas._libs.skiplist'             # 部分 pandas 版本需要[citation:7]
        ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='update_db',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
