# Introductory Project to Buildroot

## Linux in Embedded Systems

### Julian Szachowicz

## Introduction

### Project Requirements

The requirements are as follows:

 1. Vex9 should automatically connect to the network, using DHCP to obtain the network parameters.
Disconnection of the cable should shut down the network connection.
Connection of the cable should reconnect the network.
 2. The system host name should be set to: "firstname_lastname" of the user.
 3. When the Internet connection is established, the system clock should be
synchronized with an NTP server (preferably using the "NTP server pool")
 4. Add the shell script that after the start of the system tries to download fron certain URL update.tar.gz file and unpacks it overwriting the filesystem

### Project tools

For the project, the following tools (and versions) were used:

 * Buildroot 2019.11.1
 * Python 3.7

## Project Distribution and Installation

The project is available under the repository at [this](https://github.com/julzerinos/buildroot-introduction) repository.

### Initial setup

To prepare the environment `build.sh` may be executed.

This script will:

 1. Download buildroot 2019.11.1
 2. Unpack it
 3. Move required configuration files
 4. Build the configuration menu and the linux image

To access the configuration one may use

```sh
$ make menuconfig
```

To access the linux image one may use

```sh
$ make && ./runme
```

## Project Overview

The following steps were taken to create the image.

### Initial setup

Firstly two options were setup in menuconfig.

 1. External Toolchain (under Toolchain/External Toolchain) to Y
 2. CCache location has been changed to "../.buildroot-ccache"

To find below settings the suggested method is using "/" for the search function.

### Network connection

The netplug deamon has been activated to allow network communication.

### Host name

In menuconfig under System Configuration/System Hostname the image host name may be changed.

### Datetime synchronization

To activate datetime synchronization (without adjusting timezone), the NTPD deamon should be activated allowing NTP server pool usage.

### Shell script

This requirement is slightly more complex.

An overlaying directory must be set for buildroot to use during building. This directory is applied before/during/after initializing the image filesystem. This allows the creation of scripts to control steps of the filesystem initialization. Within the overlaying directory (named "overdir" is the project environment) BusyBox will search for initialization scripts under etc/init.d/. These must start with the string S## where ## is a number representing the priority (or order) of initialization. For the use of this project, "S99..." is perfect, because this will execute the script at the very end of image initialization.

It is important that the script has no extension and has `chmod 755` applied to it.

The script will try to download a file from the localhost server called "filesystem.tar.gz". It will unpack the directory and copy (with force overwrite) the "update" filesystem over files in the image. This `server` (with an example file) may be opened with `python3 -m http.server` in the server directory. 
