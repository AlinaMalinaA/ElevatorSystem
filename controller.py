import elevator
import time


class Controller(object):
    def __init__(self, el_del: int):
        self.elevator = elevator.Elevator(el_del)
        self.flag_for_output = True
        print("Объект создан")

    def stop_the_elevator(self):
        self.elevator.stop()

    # устанавливаем этаж-цель
    # если актуальный этаж не является этажом-целью,
    # то закрыть двери и поехать
    def move(self, target_level: int):
        if self.flag_for_output:
            print("Начиаем с {} этажа".format(self.elevator.level))
        while self.elevator.isMoving:
            if self.elevator.level < int(target_level):
                self.elevator.move(1)
            elif self.elevator.level == int(target_level):
                self.stop_the_elevator()
                self.elevator.open_doors()
                if self.flag_for_output:
                    print("Приехали!")
                    # это заглушка,
                    # позже я добавлю настоящую загрузку людей
                    print("Здесь мы загружаем и выгружаем людей")
                    time.sleep(1)
                    print()
                    time.sleep(1)
                    print()
                    time.sleep(1)
                    print()

            else:
                self.elevator.move(-1)
            if self.flag_for_output:
                print("Мы сейчас на {} этаже ".format(self.elevator.level))

    def prepare_elevator(self, target_level: int):
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
        if int(self.elevator.target) < int(self.elevator.level):
            return self.elevator.target, self.elevator.level
        else:
            return int(self.elevator.level), int(self.elevator.target)

    def load_people(self, number_of_new_people: int):
        self.elevator.occupancy = self.elevator.occupancy + number_of_new_people
        print("В кабине {} людей ".format(self.elevator.occupancy))

    def how_much_people_inside(self):
        return self.elevator.occupancy

    # проверяет, нужно ли подобрать пассажира
    # если вызвавший этаж - не нашла цель, и мы уже едем,
    # то можно и подобрать
    # если стоим или едем прямо туда, то не подбирать
    def is_that_not_our_target(self, target_level: int):
        if target_level != self.elevator.target and self.elevator.isMoving:
            return True
        else:
            return False

    def is_elev_moving(self):
        return self.elevator.isMoving

    def where_do_we_go(self):
        return self.elevator.target

    def where_are_we_now(self):
        return self.elevator.level


