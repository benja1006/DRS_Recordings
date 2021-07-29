# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\benja\\Documents\\GitHub\\DRS\\src\\main\\python\\main.py'],
             pathex=['C:\\Users\\benja\\Documents\\GitHub\\DRS\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=['openpyxl'],
             hookspath=['c:\\users\\benja\\downloads\\drs-20210726t192607z-001\\drs\\venv\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['C:\\Users\\benja\\Documents\\GitHub\\DRS\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='DRS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True , version='C:\\Users\\benja\\Documents\\GitHub\\DRS\\target\\PyInstaller\\version_info.py', icon='C:\\Users\\benja\\Documents\\GitHub\\DRS\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='DRS')
