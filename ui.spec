# -*- mode: python ; coding: utf-8 -*-
import os


block_cipher = None

wkdir = os.path.abspath('.')


#a = Analysis(['E:/Documents/Python/CR2_Preprocessor/ui.py'],
a = Analysis([os.path.join(wkdir, 'ui.py')],
             pathex=[wkdir],
             binaries=[],
             datas=[(os.path.join(wkdir, 'exiftool.exe'), '.'),
                    (os.path.join(wkdir, 'dcraw.exe'), '.'),
                    (os.path.join(wkdir, 'cr2hdr.exe'), '.'),
                    ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
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
          name='CR2_Preprocessor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='CR2_Preprocessor')
