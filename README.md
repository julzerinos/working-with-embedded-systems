# Buildroot dual admin/server ecosystem example

## Introduction

### Project Requirements

The requirements are as follows:

 1. Prepare the "administrative" Linux system similar to the „rescue” system
used in our normal lab. This system should be:
  1. working in initramfs;
  2. equipped with the tools necessary to manage the SD card (partition it,
format it, copy the new version of the system via a network, etc.).
 2. Prepare a "utility" Linux operating system using the ext4 filesystem
located in the 2nd partition as its root file system. This system should
provide a file server controlled via WWW interface (suggested solution is
Python with certain web application framework – flask, Tornado etc..
However, you may chose another environment as well).
  1. The server should serve files located in certain directory (displaying
the list of files and allowing selection of file to download).
  2. The server should also allow the authenticated users to upload new
files to that directory.
 3. Prepare a script for the bootloader, which allows to select which system
(the „administrative” or the „utility”) should be booted.
  1. Unfortunately, the current emulation of the GUI-connected GPIO does not
correctly send the initial state of the inputs. Therefore the user must
have certain time to press the „reconnect” button in the GUI as soon as
the U-Boot starts.
  2. Due to certain problems with current emulation of GPIO, the first
change of the state of the LED is ignored. Please clear all GPIOs
connected to the LEDs you are going to use, so the next operations will
work correctly.
  3. After two seconds the LED 24 should signal, that the buttons will be
checked.
  4. After the next second, the buttons should be read to select the system.
If the chosen button IS NOT pressed, the „utility” system should beloaded. If the chosen button IS pressed, the „administrative” system
should be loaded.
  5. After selection of the system, the LED 24 should be switched off. The
LED 25 should be switched ON if the „utility” system was selected. The
LED 26 should be switched ON if the „administrative” system was
selected.

### Project Tools

The project utilizes the following tools:

* Buildroot 2020.02
* Initframs with Uboot
* Configuration based on following [distribution](https://github.com/wzab/BR_Internet_Radio/tree/gpio/QemuVexpressA9) (from branch gpio-uboot)
* Python 3.8.2
* Virtualenv

## Project Distribution and Installation

### Initial setup

In the case of using the repository (and not directly downloading the buildroot package) the project may be setup using the `prepare_systems.sh` script. There are many variables to this setup so user may be required to adjust ad hoc.

The script will:

Setup the utility system by:

1. Downloading and building buildroot 2020.02
2. Apply patches to the configuration
3. Applying configuration
4. Copying required files to Admin system folder

Setup the Admin system by:

1. Preparing the Uboot configuration using the copied Utility files
2. Downloading and building buildroot 2020.02
3. Apply patches to the configuration
4. Applying configuration
5. Preparing the virtualenv for gui usage

To access on of the image configuration one may use (in the buildroot directory)

``` sh
$ make menuconfig
```

To access the linux images one must use the prepared script:

``` sh
$ ./runme
```

The runme completes the following:
1. Opens the GUI
2. Opens the image
3. Upon closing the image, closes the GUI

**Once the Image starts loading it is vital to "reconnect" the gui. Missing this step will cause the dual boot to always boot to the Admin system.**

During booting, the user has 10 second to reconnect the GUI and switch the 0 switch to 0 or 1 for Utility or Admin respectively. After 10 seconds the appropriate system will be booted. This method was selected to allow the user to reconnect the GUI in time and then accounts for gpio bouncing (not using the button) and time for the connectors to update for the switch to be read.

Access credentials for both systems: `root` with no password.

## Project Overview

### Utility System

The utility system boots a simple HTTP file server on localhost port 8810. This port is forwarded to the host via port 8888 and may be accessed on the host system with `localhost:8888`. Please note that the server has not been tested and updating files may potentially alter the Utility system.

The file server is authentication-protected with the credentials `admin/password`.

### Admin Systems

The admin system may influence the partitions of the utility system.

### Bootloader

The bootloader uses a script simultaneously with it's innate delay settings to allow the user to communicate via the gpio demo switch to select (or not select) the appropriate system to boot into.

### Project setup

The following steps were taken to setup the project.

1. Copy the repository (QemuVexpressA9) from the following [repository](https://github.com/wzab/BR_Internet_Radio/tree/gpio)
2. Create virtual environment to use GUI
3. Prepare file server on Utility system
4. Prepare admin system
5. Create boot system for both images
6. Integrate GUI with bootloader
7. Setup Admin system capabilities
