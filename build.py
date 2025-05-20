import os
import platform
import subprocess
import shutil
import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import pyinstaller
        print("PyInstaller is installed.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=6.3.0"])
        print("PyInstaller installed successfully.")

def clean_build_dirs():
    """Clean build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name} directory...")
            shutil.rmtree(dir_name)

def build_executable():
    """Build executable for the current platform"""
    system = platform.system().lower()
    
    # Base PyInstaller command using Python module
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=ClipAI",
        "--onefile",
        "--windowed",
        "--clean",
        "--add-data=images;images" if system == 'windows' else '--add-data=images:images',
        '--icon=images/ClipAI_icon.ico',
        'run.py'
    ]
    
    # Add platform-specific options
    if system == 'darwin':  # macOS
        cmd.extend(['--target-arch=universal2'])
    
    print("Running PyInstaller with command:", " ".join(cmd))
    
    try:
        # Run PyInstaller
        subprocess.run(cmd, check=True)
        
        # Create platform-specific output directory
        output_dir = f'dist/{system}'
        os.makedirs(output_dir, exist_ok=True)
        
        # Move executable to platform-specific directory
        executable = 'ClipAI.exe' if system == 'windows' else 'ClipAI'
        if os.path.exists(f'dist/{executable}'):
            shutil.move(f'dist/{executable}', f'{output_dir}/{executable}')
        else:
            raise FileNotFoundError(f"Executable not found at dist/{executable}")
        
        # Copy necessary files
        files_to_copy = ['prompts.json', 'config.json', 'README.md']
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, output_dir)
            else:
                print(f"Warning: {file} not found, skipping...")
        
        # Create images directory and copy images
        images_dir = f'{output_dir}/images'
        os.makedirs(images_dir, exist_ok=True)
        if os.path.exists('images'):
            for file in os.listdir('images'):
                shutil.copy2(f'images/{file}', images_dir)
        else:
            print("Warning: images directory not found!")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running PyInstaller: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def main():
    """Main build function"""
    try:
        print("Checking dependencies...")
        check_dependencies()
        
        print("Cleaning build directories...")
        clean_build_dirs()
        
        print("Building executable...")
        build_executable()
        
        print("Build completed successfully!")
        print(f"Executable can be found in: dist/{platform.system().lower()}/")
        
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 