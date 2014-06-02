#!/usr/bin/env python
# coding: utf-8
from sys import exit
import copy
import time

class Point(object):

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __repr__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __str__(self):
        return self.__repr__()

    @property
    def xy(self):
        return (self._x, self._y)

    @xy.setter
    def xy(self, xy):
        self._x = xy[0]
        self._y = xy[1]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    def getNeighbors(self):
        out = []
        out.append(Point(self.x-1, self.y-1))
        out.append(Point(self.x+1, self.y+1))
        out.append(Point(self.x-1, self.y+1))
        out.append(Point(self.x+1, self.y-1))
        out.append(Point(self.x, self.y-1))
        out.append(Point(self.x, self.y+1))
        out.append(Point(self.x+1, self.y))
        out.append(Point(self.x-1, self.y))

        return out

class Man(Point):

    def __init__(self, x, y, alive=False, t=False):
        Point.__init__(self, x, y)
        self._alive = alive
        self.table = t

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, a):
        self._alive = a

    def getNeighborsAlive(self):
        neighbors = self.getNeighbors()
        alive = 0;
        for i in neighbors:
            try:
                if self.table.getMan(i.x, i.y):
                    alive += 1
            except IndexError as k:
                "Tentou acessar uma posição que não existe cai aqui"
                pass

        return alive

    def __str__(self):
        return "Man: %s , XY %s " % ("alive" if self._alive else "dead",Point.__str__(self))

    def __nonzero__(self):
        return self.alive


class Table(object):

    def __init__(self, w, h):
        self.table = [[Man(i, j) for i in xrange(h)] for j in xrange(w)]
        self.lines_size = w
        self.col_size = h
        self.generation = 0;
        self.alives = 0
        self.deads = 0

    def __repr__(self):
        out = ""
        for i in self.table:
            for j in i:
                out += self.getPrintMan(j)
            out += "\n"
        out += "\n(Generation: %d, Alives: %d, Deads: %d)" % (self.generation, self.alives, self.deads)
        return  out

    def __str__(self):
        out = ""
        for i in self.table:
            for j in i:
                out += self.getPrintMan(j)
            out += "\n"
        out += "\n(Generation: %d, Alives: %d, Deads: %d)" % (self.generation, self.alives, self.deads)
        return  out

    def setTable(self, table):
        if not type(table) == list:
            raise Exception("table passed is not valid")

        self.table = []

        for i, line in enumerate(table):
            self.table.append([])
            for j, col in enumerate(line):
                m = Man(i, j, bool(table[i][j]),t=self)
                self.table[i].append(m)

        self.lines_size = len(table)
        self.col_size = len(table[0])

    def getMan(self, l, c):
        return self.table[l][c]

    def printMan(self, m):
        cor = 32 if m.alive else 31
        print '\033[%sm%d\033[0;0m ' % (cor, m.getNeighborsAlive()),

    def getPrintMan(self, m):
        cor = 32 if m.alive else 31
        el = "█" if m.alive else "█"
        return '\033[%sm%s\033[0;0m' % (cor, el)

    def iterTable(self):
        self.alives = 0
        self.deads = 0
        new_table = []
        for l, line in enumerate(self.table):
            new_line = []
            for c, col in enumerate(line):
                m = self.getMan(l, c)
                nb_alives = m.getNeighborsAlive()

                if nb_alives == 3:
                    mn = Man(m.x, m.y, True, self)
                elif nb_alives < 2 or nb_alives > 3:
                    mn = Man(m.x, m.y, False, self)
                elif nb_alives == 2:
                    mn = copy.copy(m)

                if mn:
                    self.alives += 1
                else:
                    self.deads += 1

                new_line.append(mn)
            new_table.append(new_line)
        self.table = new_table
        self.generation += 1

table = [
[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

t = Table(10,10)
t.setTable(table)
while 1:
    print "\n"*30
    print t
    t.iterTable()
    time.sleep(0.3)
