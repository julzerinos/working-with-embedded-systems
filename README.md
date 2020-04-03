## Steps to recreate

 1. create virtual environment to install gui python pip packages
 2. install required packages
 3. create c file in directory overlay subdirectory (eg. root)
 4. create Makefile

```sh
Makefile
```

 5. create build file to cross-compile binary for buildroot usage

```sh
build
```

 6. modified runme (or steps: open gui -> rebuild BR -> run BR)
 7. use binary application within BR

 8. play around with libgpiod commands
