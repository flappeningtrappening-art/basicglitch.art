#!/usr/bin/env python3
# copy_tools.py - Copy tools to Krita's user script folder
import os
import shutil
import sys

def main():
    # Source: Your current tools folder
    source_dir = r"C:\Program Files\Krita (x64)\share\krita\pykrita\BasicGlitch_toolkit\tools"
    
    # Destination: Krita's user script folder
    dest_dir = r"C:\Users\basic.glitch\AppData\Roaming\krita\pykrita\scripts"
    
    print("📁 COPYING TOOLS TO KRITA USER FOLDER")
    print("=" * 50)
    print(f"Source: {source_dir}")
    print(f"Destination: {dest_dir}")
    print("=" * 50)
    
    # Create destination if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Copy all .py files
    copied = 0
    skipped = 0
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.py'):
            source_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(dest_dir, filename)
            
            # Check if file already exists and is newer
            if os.path.exists(dest_path):
                source_mtime = os.path.getmtime(source_path)
                dest_mtime = os.path.getmtime(dest_path)
                
                if source_mtime <= dest_mtime:
                    print(f"⏭️  {filename}: Already up-to-date")
                    skipped += 1
                    continue
            
            # Copy the file
            try:
                shutil.copy2(source_path, dest_path)
                print(f"✅ {filename}: Copied")
                copied += 1
            except Exception as e:
                print(f"❌ {filename}: Failed - {e}")
    
    print("=" * 50)
    print(f"RESULTS: {copied} copied, {skipped} skipped")
    
    if copied > 0:
        print("\n🔄 RESTART KRITA to see tools in Tools→Scripts menu")
    else:
        print("\n✅ All files already in correct location")
        
        # Test if they appear
        print("\n🔍 Testing menu appearance...")
        test_menu()

def test_menu():
    """Test if tools would appear in menu"""
    dest_dir = r"C:\Users\basic.glitch\AppData\Roaming\krita\pykrita\scripts"
    
    if not os.path.exists(dest_dir):
        print("❌ Destination folder doesn't exist!")
        return
    
    py_files = [f for f in os.listdir(dest_dir) if f.endswith('.py')]
    
    print(f"Found {len(py_files)} Python files in user scripts folder")
    
    # Check which have run() function
    print("\nChecking for run() functions:")
    
    # Add to path temporarily
    if dest_dir not in sys.path:
        sys.path.append(dest_dir)
    
    for filename in py_files[:5]:  # Check first 5
        module_name = filename[:-3]  # Remove .py
        try:
            module = __import__(module_name)
            if hasattr(module, 'run'):
                print(f"  ✅ {filename}: Has run()")
            else:
                print(f"  ⚠️  {filename}: NO run() function")
        except Exception as e:
            print(f"  ❌ {filename}: Can't import - {e}")

if __name__ == "__main__":

    main()



def run():

    """Run the copy tools script"""

    main()
