#!/bin/bash

# This script will bundle together LPM exec, LPM-GUI exec and `install.sh` and zip it for release on GitHub.
# The LPM-GUI exec isn't ready yet, but will be bundled when it is.

VERSION=1.0.0
PACKAGEDIR=package

# Makes directory "package" (no error if it exists).
function make_pkg_dir() {
  mkdir -p package
}

# Uses PyInstaller to compile LPM into package dir.
function compile_lpm() {
  pyinstaller --onefile --distpath $PACKAGEDIR --name lpm src/main.py
}

# Makes package dir, compiles LPM into it, copies install.sh into it, and zips it.
function package() {
  make_pkg_dir
  compile_lpm
  cp ./install.sh $PACKAGEDIR
  zip -r lpm-v$VERSION.zip $PACKAGEDIR
}

# Deletes temporary package dir.
function cleanup() {
  rm -r $PACKAGEDIR
}

package
cleanup
