import time


class Elevator(object):
    def __init__(self, d):
        self.level = 1  # актуальный  этаж для лифта
        self.occupancy = 0  # количество людей внутри
        self.isMoving = False
        self.target = 0  # этаж-назначение
        self.delay = d  # время движения между этажами и время закрытия створок дверей (во избежание несчастных случаев)

    def open_doors(self):
        # let people to come in and exit
        pass

    def close_doors(self):
        # closing the doors ONLY AFTER waiting for 1 sec
        time.sleep(self.delay)

    def move(self, iterator):
        time.sleep(self.delay)
        self.level += iterator

    def stop(self):
        self.isMoving = False

    def go(self):
        self.isMoving = True
