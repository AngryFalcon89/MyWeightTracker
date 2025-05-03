# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Get the tkinter path for macOS
tk_path = '/opt/homebrew/opt/python-tk@3.11/libexec'

# Collect all tkcalendar submodules and data files
tkcalendar_datas = collect_data_files('tkcalendar')
tkcalendar_hiddenimports = collect_submodules('tkcalendar')

a = Analysis(
    ['app.py'],
    pathex=[tk_path],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('requirements.txt', '.'),
        ('assets', 'assets'),
    ] + tkcalendar_datas,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'matplotlib',
        'numpy',
        'pandas',
        'controllers.data_controller',
        'controllers.stats_controller',
        'views.main_view',
        'views.input_panel',
        'views.entries_table',
        'views.stats_panel',
    ] + tkcalendar_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyWeightTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyWeightTracker',
)

app = BUNDLE(
    coll,
    name='MyWeightTracker.app',
    icon=None,
    bundle_identifier='com.myweighttracker',
    info_plist={
        'CFBundleName': 'MyWeightTracker',
        'CFBundleDisplayName': 'MyWeightTracker',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
)
