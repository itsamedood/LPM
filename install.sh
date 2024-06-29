#!/bin/bash

# Displays `$1` as an error message and exits with code 1.
function raise() {
  printf "\033[0;31merror\033[0;0;0m: $1\n"; exit 1
}

# Checks to see if LPM is already installed.
function check_for_lpm() {
  if ! [ "$(ls ~/.lpm)" = "" ]; then raise "LPM exists already!"; fi
}

# Do this later :)
function install_lpm_windows() {
  # Steps:
  # 1) mkdir `C:\Users\<user>\.lpm`
  # 2) touch `C:\Users\<user>\.lpm\.key` (where the key for AES is stored)
  # 3) touch `C:\Users\<user>\.lpm\lpm.bin` (where shit is stored)
  # 4) Add path to LPM exec to PATH env var.

  echo "will do eventually ¯\_(ツ)_/¯"
  # printf "\033[0;32mSuccessfully installed LPM!\033[0;0;0m\n"
}

# Installs LPM on Linux & MacOS.
function install_lpm_unix() {
  echo "* Sudo will be needed to move LPM executable to /usr/bin."

  mkdir -p ~/.lpm
  touch ~/.lpm/.key
  touch ~/.lpm/lpm.bin
  sudo mv $PWD/lpm /usr/bin

  printf "\033[0;32mSuccessfully installed LPM!\033[0;0;0m\n"
}

# Determines which install function to run given OS.
function install_lpm() {
  os="$(uname -s | tr A-Z a-z)"

  if [ "$os" = "darwin" ] || [ "$os" = "linux" ]
  then install_lpm_unix
  else install_lpm_windows
  fi
}

check_for_lpm
install_lpm
lpm # Run `lpm` to create a key since `.key` will be empty.
