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

    # устанавливаем этаж-цель
    # если актуальный этаж не является этажом-целью,
    # то закрыть двери и поехать
    def move(self, target_level):
        self.target = target_level
        if self.level != self.target:
            self.close_doors()
            self.isMoving = True
            print("Мы сейчас на {} этаже ".format(self.level))
        while self.isMoving:
            if self.level < target_level:
                time.sleep(self.delay)
                self.level += 1
            elif self.level == target_level:
                self.isMoving = False
                print("Приехали!")
                self.open_doors()
            else:
                time.sleep(self.delay)
                self.level -= 1
            print("Мы сейчас на {} этаже ".format(self.level))

    # команда для прерывания, если пришел вызов с какого-нибудь этажа в процессе движения
    # пока не используется
    def stop(self):
        self.isMoving = False
