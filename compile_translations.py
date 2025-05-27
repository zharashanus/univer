#!/usr/bin/env python3
import os
import polib

def compile_po_files():
    """Компилирует .po файлы в .mo файлы."""
    locale_dirs = [
        'locale/en/LC_MESSAGES',
        'locale/ru/LC_MESSAGES', 
        'locale/kk/LC_MESSAGES'
    ]
    
    print("Starting compilation of translation files...")
    
    for locale_dir in locale_dirs:
        po_file = os.path.join(locale_dir, 'django.po')
        mo_file = os.path.join(locale_dir, 'django.mo')
        
        print(f"Checking {po_file}")
        
        if os.path.exists(po_file):
            try:
                print(f"Loading {po_file}")
                po = polib.pofile(po_file)
                print(f"Saving as {mo_file}")
                po.save_as_mofile(mo_file)
                print(f"✓ Compiled {po_file} -> {mo_file}")
            except Exception as e:
                print(f"✗ Error compiling {po_file}: {e}")
        else:
            print(f"✗ File {po_file} does not exist")
    
    print("Compilation finished!")

if __name__ == '__main__':
    compile_po_files() 