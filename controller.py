import elevator
import time


class Controller(object):
    def __init__(self, el):
        self.elevator = el
        self.queue = []
        print("Объект создан")

    # метод для подсаживания пассажиров по пути
    # запоминает цель лифта и отправляет ее в очередь
    # подменяет цель лифта на промежуточный этаж, с которого пришел вызов
    def stop_and_open_doors(self, target_level):
        print("Надо остановиться")
        elevator.isMoving = False
        temp = elevator.target
        elevator.move(target_level)
        self.add_to_queue(temp)

    def add_to_queue(self, target_level):
        self.queue.append(target_level)
        print("В очереди: "+self.queue)
