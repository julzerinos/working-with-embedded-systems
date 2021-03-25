# An assortment of embedded Linux system projects
  
## Introduction  
  
This is a collection of five projects involving the creation of embedded Linux systems in [Buildroot](https://buildroot.org/) (4) and [OpenWRT](https://openwrt.org/) (1).

Each project is stored on a separate branch with respective READMEs containing descriptions, goals and setup instructions. Please check below for a short list of the projects.

## Projects

1. [buildroot-introdcution](https://github.com/julzerinos/buildroot-dual-boot/tree/buildroot-introduction) - an introductory buildroot project which involves basic operations such as network connection, host name change, datetime synchronization and including files in the embedded system's directory.
2. [buildroot-dual-boot](https://github.com/julzerinos/buildroot-dual-boot/tree/buildroot-dual-boot) - setup of two parallel embedded systems which are wrapped in a boot loader for selecting the appropriate system at startup.
3. [buildroot-gpio](https://github.com/julzerinos/buildroot-dual-boot/tree/buildroot-gpio) - this project involves the interaction of an embedded Linux system connecting and interacting with an external controller consisting of LED diodes and buttons (simulated by python).
4. [buildroot-snake](https://github.com/julzerinos/buildroot-dual-boot/tree/buildroot-snake) - takes the above project a step further by recreating everybody's favorite classic - Snake - in the embedded system output window. The twist? The snake is controlled by the external controller.
5. [openwrt-snake](https://github.com/julzerinos/buildroot-dual-boot/tree/openwrt-snake) - the same as the above, but recreated in OpenWRT.
