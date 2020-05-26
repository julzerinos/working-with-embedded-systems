# Buildroot as a graphical interface for the Snake Game

## Introduction

### Project Requirements

The project requirements are simplified below:

  1. Project must be created in buildroot
  2. Buildroot must utilize gpio
  3. Buildroot must utilize sound card

The selected creative initiative to fulfill these requirements is the recreation of the cult classic hit _Snake_. In this case, the game is displayed in the buildroot terminal (before login), controlled via gpio and plays audio via the host-connected soundcard.

### Project Tools

The above are fulfilled with the following toolset:

  * Buildroot 2020.02
    * Configuration based on following [distribution](https://github.com/wzab/BR_Internet_Radio/tree/gpio/QemuVexpressA9) (from branch gpio-simple)
  * Python 3.8.2
    * pygame
    * gpiod
    * curses
  * Snake logic
    * Sourced from [Snake](https://github.com/GeorgeZhukov/python-snake/blob/master/snake.py)
  * Sounds
    * [He man - What's Going On](https://www.youtube.com/watch?v=32FB-gYr49Y)
    * Other sounds - [Freesound](freesound.com)

## Project Distribution and Installation

### Initial Setup

The project has to be setup before use (download, install and apply configuration to buildroot). This is done by running `build.sh`.

This will download, install, apply patches and apply configuration to the buildroot install.

The user should also prepare a virtualenv for Python to run the local GUI through which the user will control the snake. The required packages are listed in `pipreq.txt` and can be applied with `pip install -r pipreq.txt`.


## Project Overview

If the project is setup correctly, the user may access the buildroot image via the `runme` script. The image will boot and the snake game will begin playing immediately after startup (without going through log in). At any moment, the user should (in the host machine) open the GUI with `python GUI/gui3.py` or `run_before`.

The game is composed of:
 * curses interface for snake gameplay.
 * pygame playing sounds (background music, level-up, movement and death).
 * upon death, the user is granted the permission to login to the system.

 ### Project Recreation Steps

  1. Copy the repository (QemuVexpressA9) from the following [repository](https://github.com/wzab/BR_Internet_Radio/tree/gpio) (branch: gpio-simple)
  2. Create virtualenv to use GUI
  3. Setup Snake game on Buildroot
  4. Setup to use sounds
  5. Setup flow of game/system
