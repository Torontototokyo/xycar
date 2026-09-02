# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/work_card/insert.py'],
    pathex=[],
    binaries=[],
    datas=[('src/work_card/*.py', 'work_card')],
    hiddenimports=[
        'sqlalchemy',
        'pymysql',
        'pandas'],
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
