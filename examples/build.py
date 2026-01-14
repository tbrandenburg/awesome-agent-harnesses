#!/usr/bin/env python3

"""Build script for HelloWorld project."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    """Main build function."""
    print("🔨 Starting HelloWorld build process...")

    # Create build directory
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    # Create dist directory for distribution
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    print("📁 Created build directories")

    # Test the Python script
    print("🧪 Testing HelloWorld.py...")
    try:
        result = subprocess.run(
            [sys.executable, "HelloWorld.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"✅ Test passed: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Test failed: {e}")
        return 1

    # Copy source files to build directory
    shutil.copy2("HelloWorld.py", build_dir)
    print("📋 Copied source files to build directory")

    # Create executable version
    executable_path = dist_dir / "helloworld"
    with open(executable_path, "w") as f:
        f.write("#!/usr/bin/env python3\n")
        with open("HelloWorld.py") as source:
            # Skip the shebang line from original
            lines = source.readlines()
            if lines and lines[0].startswith("#!"):
                lines = lines[1:]
            f.writelines(lines)

    # Make executable
    os.chmod(executable_path, 0o755)
    print("🚀 Created executable version")

    # Create build info
    build_info = build_dir / "build_info.txt"
    with open(build_info, "w") as f:
        f.write("HelloWorld Build Information\n")
        f.write("===========================\n\n")
        f.write(
            f"Build Date: {subprocess.run(['date'], capture_output=True, text=True).stdout}"
        )
        f.write(f"Python Version: {sys.version}\n")
        f.write(f"Build Host: {os.uname().nodename}\n")
        f.write("\nBuild Contents:\n")
        f.write("- HelloWorld.py (source)\n")
        f.write("- dist/helloworld (executable)\n")

    print("📄 Generated build information")

    print("\n✅ Build completed successfully!")
    print(f"📦 Build artifacts available in: {build_dir.absolute()}")
    print(f"🎯 Distribution files in: {dist_dir.absolute()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
