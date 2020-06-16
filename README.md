# OpenWRT as a graphical interface for the Snake Game

### Linux in Embedded Systems

**Julian Szachowicz**

## Introduction

### Project Requirements

The project requirements are simplified below:

  1. Project must be created in OpenWRT
  2. Project must utilize gpio
  3. Project must utilize sound card
  4. This is a recreation of previous project made in buildroot (see [buildroot-snake](https://github.com/julzerinos/buildroot-snake/))

The project uses qemu-arm and buildroot to create and support an image of OpenWRT. Once setup with below instructions, the snake game will be playable within the OpenWRT image.

## Project Tools

The above are fulfilled with the following toolset:

  * Buildroot 2020.02
    * Configuration based on following [distribution](https://github.com/wzab/BR_Internet_Radio/tree/gpio/QemuVexpressA9) (from branch gpio-simple-usb)
  * Python 3.8.2
    * mpd/mpc
    * gpiod
    * curses
  * Snake logic
    * Sourced from [Snake](https://github.com/GeorgeZhukov/python-snake/blob/master/snake.py)
  * Sounds
    * Sourced from [Soundhelix](https://www.soundhelix.com/audio-examples)


## Project Distribution and Installation

The project is availble at [this]() repository.


### Initial Setup

To setup the project the following steps should be taken:

  1. Initialize the buildroot image with the following commands

```sh
git clone https://github.com/wzab/BR_Internet_Radio
cd BR_Internet_Radio
git checkout gpio_simple_USB
cd QemuVirt64
./build.sh
```

  2. In the meanwhile, setup OpenWRT with the following

```sh
wget https://downloads.openwrt.org/releases/19.07.2/targets/armvirt/64/openwrt-19.07.2-armvirt-64-Image
wget https://downloads.openwrt.org/releases/19.07.2/targets/armvirt/64/openwrt-19.07.2-armvirt-64-root.ext4.gz
wget https://downloads.openwrt.org/releases/19.07.2/targets/armvirt/64/openwrt-sdk-19.07.2-armvirt-64_gcc-7.5.0_musl.Linux-x86_64.tar.xz

gzip -c -d openwrt-19.07.2-armvirt-64-root.ext4.gz > root.ext4
truncate -s \>512M root.ext4
/sbin/resize2fs root.ext4

tar -xJf openwrt-sdk-19.07.2-armvirt-64_gcc-7.5.0_musl.Linux-x86_64.tar.xz

wget http://koral.ise.pw.edu.pl/~wzab/LINES/L8_examples.tar.bz2
tar -xjf L8_examples.tar.bz2

cd openwrt-sdk-19.07.2-armvirt-64_gcc-7.5.0_musl.Linux-x86_64

src-link mini /absolute/path/to/W8

export LANG=C
scripts/feeds update mini
scripts/feeds install -a -p mini
make menuconfig
# (In the menuconfig make sure that drv-mpc8xxx is selected as a package. Save configuration at the end.)
make package/drv-mpc8xxx/compile

cd bin/targets/armvirt/64/packages
python3 -m http.server &
```

  3. At this point, the buildroot image should be complete. Your project tree structure should look like this:

```sh
opnwrt-snake
| buildroot-2020.02
| GUI
| (...)
| openwrt-sdk-19 (...)
```

  4. If the steps have been completed correctly, the image may be accessed with `./runme2`.

  5. Once the image starts, finalize the installation with the `openwrt_setup` script by either copying it or cloning it from the repository with

```sh
git clone --single-branch --branch just-setup https://github.com/julzerinos/openwrt-snake.git
```

## Project Overview

After the above setup, the snake game may be played from the console line using `python3 snake.py` and may be steered with the gpio connected buttons (line 12, 13, 14 and 15).

`gui3.py` should be used as the gpio remote control (appropriate pip requirements are found in `requirements.txt`).
