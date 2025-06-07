#!/bin/bash
git clone --recurse-submodules https://github.com/openwall/john.git
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev zlib1g-dev
sudo apt install -y hashcat
cd john/src
./configure
make -s clean && make -sj8
