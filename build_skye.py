"""
Helper script to build SkyeEngine into a single shared library
for usage with PySkye

os environment variables are passed to cmake
"""

import os
import subprocess
import shutil

print("""
==================== PySkye ====================
This script will build the SkyeEngine library for use with PySkye.
See LICENSE for license information.

SkyeEngine is developed by zTags, check their repo for license and more info:
https://www.github.com/zTags/SkyeEngine
PySkye is developed by WoffleTbh, you can take a look at the repo:
https://www.github.com/WoffleTbh/PySkye
================================================
""")

def check_dep(dep):
    print(f"[INFO] Checking for {dep}...", end="")
    try:
        subprocess.run([dep, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("failed")
        exit(1)
    print("ok")

def check_deps():
    print("[INFO] Checking dependencies")
    try:
        check_dep("cmake")
        check_dep("make")
        check_dep("clang++")
        check_dep("clang")
        check_dep("git")
    except subprocess.CalledProcessError:
        print("Please install cmake, make, clang++, clang, and git")
        exit(1)

def runverbose(cmd):
    print("[CMD] " + " ".join(cmd))
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
    if proc.returncode != 0:
        print(proc.stderr.decode("utf-8"))
        exit(1)

def ensure_dirs():
    if not os.path.exists("skye"):
        print("[INFO] 'skye' directory doesn't exist, meaning the C wrappers have been removed. Please reinstall")
        exit(1)
    if os.path.exists("skye/SkyeEngine") and not os.environ.get("NO_INSTALL"):
        print("[INFO] Removing old SkyeEngine source")
        shutil.rmtree("skye/SkyeEngine")

def install_all():
    print("[INFO] Installing SkyeEngine and dependencies")
    runverbose(["git", "clone", "https://github.com/zTags/SkyeEngine", "skye/SkyeEngine"])
    print("[INFO] Entering skye/SkyeEngine directory")
    os.chdir("skye/SkyeEngine")
    runverbose(["git", "submodule", "update", "--init"])
    print("[INFO] Exiting skye directory")
    os.chdir("../..")

def build_skye():
    print("[INFO] Building SkyeEngine")
    print("[INFO] Entering skye/SkyeEngine directory")
    os.chdir("skye/SkyeEngine")
    if os.path.exists("build"):
        print("[INFO] Removing old build directory")
        shutil.rmtree("build")
    print("[INFO] Creating build directory & entering it")
    os.mkdir("build")
    os.chdir("build")
    print("[INFO] Setting ENV variables")
    print("[CMD] CFLAGS=-fPIC")
    print("[CMD] CXXFLAGS=-fPIC")
    if not os.environ.get("CC"):
        os.environ["CC"] = "clang"
        print("[CMD] CC=clang")
    if not os.environ.get("CXX"):
        os.environ["CXX"] = "clang++"
        print("[CMD] CXX=clang++")
    os.environ["CFLAGS"] = "-fPIC"
    os.environ["CXXFLAGS"] = "-fPIC"
    runverbose(["cmake", ".."])
    runverbose(["make", "-j"])
    CC = os.environ["CC"]
    CXX = os.environ["CXX"]
    runverbose([CXX, "-c", "-fPIC", "../../pyskye/shell.cpp", "../../pyskye/SUSMap.cpp", "-I../include/", "-std=c++17"])
    runverbose([CXX, "-shared", "-Wl,-soname,libskye.so", "-o", "../../libskye.so", "SUSMap.o", "shell.o", "engine/SUS/libskye_sus.a", "engine/shell/libskye_shell.a"])
    print("[INFO] Exiting build directory")
    os.chdir("../../..")

def clean():
    if not os.environ.get("NO_INSTALL"):
        print("[INFO] Cleaning up")
        shutil.rmtree("skye/SkyeEngine")

def remove_binaries():
    if os.path.exists("libskye.so"):
        print("[INFO] Removing binaries")
        os.remove("skye/libskye.so")

def main():
    remove_binaries()
    check_deps()
    ensure_dirs()
    if not os.environ.get("NO_INSTALL"):
        install_all()
    build_skye()
    clean()

if __name__ == "__main__":
    main()
    print("[INFO] Done")
    exit(0)

