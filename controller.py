import elevator
import time


class Controller(object):
    def __init__(self, el_del):
        self.elevator = elevator.Elevator(el_del)
        self.levels_queue = []
        print("Объект создан")



    # метод для подсаживания пассажиров по пути
    # запоминает цель лифта и отправляет ее в очередь
    # подменяет цель лифта на промежуточный этаж, с которого пришел вызов
    def stop_and_pick_up(self, target_level):
        print("Надо остановиться")
        elevator.isMoving = False
        temp = elevator.target
        elevator.move(target_level)
        self.add_to_queue(temp)

    # не забыть добавить проверку на повтор значений в очереди
    def add_to_queue(self, target_level):
        self.levels_queue.append(target_level)
        print("В очереди: "+self.levels_queue)

    # не только находит максимальный этаж, но и сразу удаляет его из очереди
    def get_max_level_from_queue(self):
        max_level = max(self.levels_queue)
        self.levels_queue.remove(max_level)
        return max_level


    # устанавливаем этаж-цель
    # если актуальный этаж не является этажом-целью,
    # то закрыть двери и поехать
    def move(self, target_level):

        while self.elevator.isMoving:
            if self.elevator.level < target_level:
                self.elevator.move(1)
            elif self.elevator.level == target_level:
                self.elevator.stop()
                print("Приехали!")
                self.elevator.open_doors()
            else:
                self.elevator.move(-1)
            print("Мы сейчас на {} этаже ".format(self.elevator.level))

    def prepare_elevator(self, target_level):
        self.elevator.target = target_level
        if self.elevator.level != self.elevator.target:
            self.elevator.close_doors()
            self.elevator.go()

    def if_elevator_empty(self):
        if self.elevator.occupancy == 0:
            return True
        else:
            return False

    def give_the_range_of_levels_that_left(self):
        if self.elevator.target < self.elevator.level:
            return self.elevator.target, self.elevator.level+1
        else:
            return self.elevator.level, self.elevator.target

    def load_people(self, number_of_new_people):
        elevator.occupancy = elevator.occupancy + number_of_new_people
        print("В кабине {} людей ".format(elevator.occupancy))

    def how_much_people_inside(self):
        return self.elevator.occupancy

    def is_that_our_target(self, target_level):
        if target_level != self.elevator.target and self.elevator.isMoving:
            return True
        else:
            return False