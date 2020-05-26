#!/usr/bin/python3

# Sources:
# https://lazka.github.io/pgi-docs
# https://python-gtk-3-tutorial.readthedocs.io/en/latest/button_widgets.html
# https://developer.gnome.org/gtk3/stable/
# Threads: https://wiki.gnome.org/Projects/PyGObject/Threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

import threading
# Communication part
import struct
pipc_magick = 0x6910
import posix_ipc as pipc
mq_to_qemu = pipc.MessageQueue("/to_qemu",flags=pipc.O_CREAT, read=False, write=True)
mq_from_qemu = pipc.MessageQueue("/from_qemu",flags=pipc.O_CREAT, read=True, write=False)

#Global variables (will be filled when bulding the GUI)
class glb:
    pass

import random
import time


def send_change(nof_pin, state):
    s=struct.pack(">HBB",pipc_magick,nof_pin,state)
    mq_to_qemu.send(s)

def recv_change(msg):
    mg, pin, state = struct.unpack(">HBB",msg)
    print("mg=",mg," pin=",pin," state=",state)
    if mg != pipc_magick:
        raise Exception("Wrong magick number in GPIO IPC message")
    if state == 0:
        s = 0
    else:
        s = 1
    GLib.idle_add(MyControls[pin].change_state,s)

def receiver():
    while True:
        msg = mq_from_qemu.receive()
        recv_change(msg[0])

class MyButton(Gtk.Button):
    dir = 0 #Input
    def __init__(self,number,name):
        super().__init__(label=name)
        self.number = number
        self.state = 1
    def change_state(self,state):
        pass

MyControls = {}

def Reconnect(button):
    # First send state of all inputs
    for i in MyControls:
        ctrl = MyControls[i]
        if ctrl.dir == 0:
           send_change(ctrl.number,1-ctrl.state)
           send_change(ctrl.number,ctrl.state)
    # Then request sending all outputs
    send_change(255,0)

class SwitchBoardWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Switch Demo")
        self.set_border_width(10)
        mainvbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        self.add(mainvbox)

        hbox = Gtk.Box(spacing=6)
        hbox = Gtk.Box(spacing=6)
        button = MyButton(0, 'up')
        button.connect("button-press-event", self.on_button_clicked,0)
        button.connect("button-release-event", self.on_button_clicked,1)
        MyControls[0] = button
        hbox.pack_start(button,True,True,0)
        button = MyButton(1, 'right')
        button.connect("button-press-event", self.on_button_clicked,0)
        button.connect("button-release-event", self.on_button_clicked,1)
        MyControls[1] = button
        hbox.pack_start(button,True,True,0)
        button = MyButton(2, 'down')
        button.connect("button-press-event", self.on_button_clicked,0)
        button.connect("button-release-event", self.on_button_clicked,1)
        MyControls[2] = button
        hbox.pack_start(button,True,True,0)
        button = MyButton(3, 'left')
        button.connect("button-press-event", self.on_button_clicked,0)
        button.connect("button-release-event", self.on_button_clicked,1)
        MyControls[3] = button
        hbox.pack_start(button,True,True,0)
        mainvbox.pack_start(hbox,True,True,0)

        mainvbox.pack_start(hbox,True,True,0)
        #Add the configuration controlls
        hbox = Gtk.Box(spacing=6)
        #Add the reconnect button
        button = Gtk.Button(label="Reconnect")
        button.connect("clicked", Reconnect)
        hbox.pack_start(button,True,True,0)

    def on_button_clicked(self, button,gparam, state):
        print("pressed!")
        send_change(button.number,state)
        self.state = state
        print("Button #"+str(button.number)+" was turned", state)
        return True


win = SwitchBoardWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()

thread = threading.Thread(target=receiver)
thread.daemon = True
thread.start()

Gtk.main()
