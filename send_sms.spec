# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/work_card/send_sms.py'],
    pathex=[],
    binaries=[],
    datas=[('src/work_card/*.py', 'work_card','.env')],
    hiddenimports=[
        'sqlalchemy',
        'pymysql',
        'pandas'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='send_sms',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
