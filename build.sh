#!/bin/bash
set -e
wget https://buildroot.org/downloads/buildroot-2019.11.1.tar.bz2
tar -xjf buildroot-2019.11.1.tar.bz2
cp .config buildroot-2019.11.1/
cp runme buildroot-2019.11.1/
cd buildroot-2019.11.1
make
