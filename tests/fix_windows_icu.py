"""Keep Windows' native ICU when a build host's unrelated ICU DLL shadows it."""
import os
import sys
from pathlib import Path
import pefile

def exports(path):
    binary=pefile.PE(str(path),fast_load=True)
    binary.parse_data_directories(directories=[0])
    names={s.name for s in binary.DIRECTORY_ENTRY_EXPORT.symbols if s.name}
    binary.close()
    return names

def main():
    if os.name!='nt':return
    root=Path(sys.argv[1]).resolve()/'PublicWebAdDetector'/'_internal'
    qt=root/'PySide6'/'Qt6Core.dll';packaged=root/'icuuc.dll'
    if not qt.is_file() or not packaged.is_file():return
    binary=pefile.PE(str(qt),fast_load=True)
    binary.parse_data_directories(directories=[1])
    required={s.name for entry in binary.DIRECTORY_ENTRY_IMPORT if entry.dll.lower()==b'icuuc.dll' for s in entry.imports if s.name}
    if not required or required<=exports(packaged):return
    system=Path(os.environ['SystemRoot'])/'System32'/'icuuc.dll'
    if not system.is_file() or not required<=exports(system):
        raise RuntimeError('Qt ICU dependencies cannot be satisfied by packaged or Windows ICU')
    if packaged.resolve().parent!=root.resolve():raise RuntimeError('Unexpected ICU target')
    packaged.unlink()
    print('Excluded incompatible build-host ICU; Qt uses verified Windows native ICU.')

if __name__=='__main__':main()
