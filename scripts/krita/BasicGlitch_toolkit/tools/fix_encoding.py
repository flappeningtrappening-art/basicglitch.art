#!/usr/bin/env python3
# fix_encoding.py - Convert all Python files to UTF-8
import os
import sys

def convert_file_to_utf8(filepath):
    """Convert a file to UTF-8 encoding"""
    try:
        # Try to read with common encodings
        for encoding in ['utf-8', 'windows-1252', 'latin-1', 'cp1252']:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                # Successfully read, now write as UTF-8
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"? {os.path.basename(filepath)}: {encoding} ? UTF-8")
                return True
            except UnicodeDecodeError:
                continue
        
        print(f"? {os.path.basename(filepath)}: Could not determine encoding")
        return False
    except Exception as e:
        print(f"? {os.path.basename(filepath)}: Error - {e}")
        return False

def main():
    # Get the tools directory
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("?? FIXING ENCODING FOR ALL PYTHON FILES")
    print("=" * 50)
    
    converted = 0
    failed = 0
    
    for filename in os.listdir(tools_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(tools_dir, filename)
            if convert_file_to_utf8(filepath):
                converted += 1
            else:
                failed += 1
    
    print("=" * 50)
    print(f"RESULTS: {converted} converted, {failed} failed")
    
    if failed > 0:
        print("\n??  Some files failed. Try Option 2 below.")

if __name__ == "__main__":

    main()



def run():

    """Run the encoding fixer"""

    main()
