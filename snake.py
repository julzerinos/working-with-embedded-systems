# Sources
# Snake https://github.com/GeorgeZhukov/python-snake/blob/master/snake.py

import sys
from random import randint

import signal

import curses

import time
from time import sleep
from datetime import timedelta

import mpd

import gpiod


class Field:
    def __init__(self, size):
        self.size = size
        self.icons = {
            0: ' . ',
            1: ' * ',
            2: ' @ ',
            3: ' $ ',
        }
        self.snake_coords = []
        self._generate_field()
        self.add_entity()

    def add_entity(self):

        while(True):
            i = randint(0, self.size-1)
            j = randint(0, self.size-1)
            entity = [i, j]

            if entity not in self.snake_coords:
                self.field[i][j] = 3
                break

    def _generate_field(self):
        self.field = [[0 for j in range(self.size)] for i in range(self.size)]

    def _clear_field(self):
        self.field = [
            [j if j != 1 and j != 2 else 0 for j in i] for i in self.field
        ]

    def render(self, screen):
        size = self.size
        self._clear_field()

        # Render snake on the field
        for i, j in self.snake_coords:
            self.field[i][j] = 1

        # Mark head
        head = self.snake_coords[-1]
        self.field[head[0]][head[1]] = 2

        for i in range(size):
            row = ''
            for j in range(size):
                row += self.icons[self.field[i][j]]

            screen.addstr(i, 0, row)

    def get_entity_pos(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 3:
                    return [i, j]

        return [-1, -1]

    def is_snake_eat_entity(self):
        entity = self.get_entity_pos()
        head = self.snake_coords[-1]
        return entity == head


class Snake:
    def __init__(self, name):
        self.name = name
        self.direction = curses.KEY_RIGHT

        # Init basic coords
        self.coords = [[0, 0], [0, 1], [0, 2], [0, 3]]

    def set_direction(self, ch):

        # Check if wrong direction
        if ch == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT:
            return
        if ch == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT:
            return
        if ch == curses.KEY_UP and self.direction == curses.KEY_DOWN:
            return
        if ch == curses.KEY_DOWN and self.direction == curses.KEY_UP:
            return

        self.direction = ch

    def level_up(self):
        # mixer.Channel(2).play(SOUNDS['point'])

        # get last point direction
        a = self.coords[0]
        b = self.coords[1]

        tail = a[:]

        if a[0] < b[0]:
            tail[0] -= 1
        elif a[1] < b[1]:
            tail[1] -= 1
        elif a[0] > b[0]:
            tail[0] += 1
        elif a[1] > b[1]:
            tail[1] += 1

        tail = self._check_limit(tail)
        self.coords.insert(0, tail)

    def is_alive(self):
        head = self.coords[-1]
        snake_body = self.coords[:-1]
        return head not in snake_body

    def _check_limit(self, point):
        # Check field limit
        if point[0] > self.field.size-1:
            point[0] = 0
        elif point[0] < 0:
            point[0] = self.field.size-1
        elif point[1] < 0:
            point[1] = self.field.size-1
        elif point[1] > self.field.size-1:
            point[1] = 0

        return point

    def move(self):
        # Determine head coords
        head = self.coords[-1][:]

        # Calc new head coords
        if self.direction == curses.KEY_UP:
            head[0] -= 1
        elif self.direction == curses.KEY_DOWN:
            head[0] += 1
        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1
        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1

        # Check field limit
        head = self._check_limit(head)

        del(self.coords[0])
        self.coords.append(head)
        self.field.snake_coords = self.coords

        if not self.is_alive():

            time.sleep(1)

            print("You have died.")

            mpd_client.stop()
            sys.exit()

        # check if snake eat an entity
        if self.field.is_snake_eat_entity():
            self.level_up()
            self.field.add_entity()

    def set_field(self, field):
        self.field = field


def sig_hand(sig, frame):
    mpd_client.stop()
    sys.exit(0)


def main(screen):
    chip = gpiod.chip('9008000.gpio')
    dir_buttons = chip.get_lines([12, 13, 14, 15])
    line_map = {
        str(dir_buttons.get(0).offset): curses.KEY_UP,
        str(dir_buttons.get(1).offset): curses.KEY_RIGHT,
        str(dir_buttons.get(2).offset): curses.KEY_DOWN,
        str(dir_buttons.get(3).offset): curses.KEY_LEFT
    }

    config = gpiod.line_request()
    config.consumer = 'snake'
    config.request_type = gpiod.line_request.EVENT_FALLING_EDGE

    dir_buttons.request(config)

    # Configure screen
    screen.timeout(0)

    # Init snake & field
    field = Field(20)
    snake = Snake("Joe")
    snake.set_field(field)

    while(True):

        loop_bulk = dir_buttons.event_wait(timedelta(seconds=1))

        if loop_bulk:

            src = str(loop_bulk[0].event_read().source.offset)

            if line_map.get(src) is not None:
                snake.set_direction(line_map[src])

        # Move snake
        snake.move()

        # Render field
        screen.clear()
        field.render(screen)
        screen.refresh()


SOUNDS = None
ENTRY = r"""
               ______
          _.-""      ""-._
       .-'                `-.
     .'      __.----.__      `.
    /     .-"          "-.     \
   /    .'                `.    \
  J    /                    \    L
  F   J                      L   J
 J    F                      J    L
 |   J                        L   |
 |   |                        |   |
 |   J                        F   |
 J    L                      J    F
  L   J   .-''''-.           F   J
  J    \ /        \   __    /    F
   \    (|)(|)_   .-'".'  .'    /
    \    \   /_>-'  .<_.-'     /
     `.   `-'     .'         .'
       `--.|___.-'`._    _.-'
           ^         ''''

           SNAKE
           GAME

           LOADING
"""

mpd_client = None

if __name__ == '__main__':

    print(ENTRY)

    signal.signal(signal.SIGINT, sig_hand)

    mpd_client = mpd.MPDClient()
    mpd_client.connect('localhost', 6600)
    mpd_client.add('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')
    mpd_client.play()

    curses.wrapper(main)
