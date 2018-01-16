#!/usr/bin/python
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from time import sleep

fps = 60
spf = 1/fps

class World(object):
    def __init__(self, text):
        self.cells = [self.read_line(line) for line in text.split('\n')]
        self.players = 'asd'
        self.selected = None

    def read_line(self, line):
        return [char for char in line]

    def render(self, screen):
        screen.clear()
        for y, line in enumerate(self.cells):
            for x, char in enumerate(line):
                screen.print_at(char, x, y)
        screen.refresh()

    def handle_event(self, ev):
        if isinstance(ev, KeyboardEvent):
            if ev.key_code == ord('q'):
                exit(0)
            elif chr(ev.key_code) in self.players:
                self.select(chr(ev.key_code))
            elif chr(ev.key_code) in 'hjkl':
                self.move(chr(ev.key_code))

    def get(self, x, y):
        return self.cells[y][x]

    def set(self, x, y, val):
        self.cells[y][x] = val

    def find(self, chars):
        for y, line in enumerate(self.cells):
            for x, char in enumerate(line):
                if char in chars:
                    yield (x, y, char)

    def find_one(self, chars):
        for x, y, char in self.find(chars):
            return (x, y, char)

    def select(self, selection):
        self.selected = None
        for x, y, char in self.find(self.players + self.players.upper()):
            if char == selection:
                self.set(x, y, char.upper())
                self.selected = char.lower()
            else:
                self.set(x, y, char.lower())

    def move(self, direction):
        if self.selected is None:
            return
        x, y, char = self.find_one(self.selected + self.selected.upper())
        if direction == 'h':
            xn, yn = x-1, y
        elif direction == 'j':
            xn, yn = x, y+1
        elif direction == 'k':
            xn, yn = x, y-1
        else:
            xn, yn = x+1, y
        if self.get(xn, yn) == ' ':
            self.set(x,y, ' ')
            self.set(xn,yn, char)

world = World('''
    ####################
    #          #       ###
    # d   a s  #   1     #
    #          #         #
    #          ####      #
    #                    #
    #                    #
    ######################
''')

def demo(screen):
    world.render(screen)
    while True:
        event = None
        while event is None:
            sleep(spf)
            event = screen.get_event()
        world.handle_event(event)
        world.render(screen)

Screen.wrapper(demo)
