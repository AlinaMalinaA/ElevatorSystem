#!/usr/bin/env python3
import controller
import elevator
import load_params
import os


NUMBER_OF_LEVELS = load_params.what_number_of_levels()
ELEVATOR_CAPACITY = load_params.what_capacity_of_elevator()
ELEVATOR_DELAY = load_params.what_delay_between_levels()

elevator = elevator.Elevator(ELEVATOR_DELAY)
controller = controller.Controller(elevator)


def is_int(k):
    try:
        int(k)
        return True
    except (TypeError, ValueError):
        return False


def loading_people():
    while True:
        print("В кабине {} людей ".format(elevator.occupancy))
        print("Сколько людей вошло или вышло? Больше {} войти не может.".format(ELEVATOR_CAPACITY))
        inp = input('Напишите положительное число для входящих людей и отрицательное для выходящих: ')
        if is_int(inp):
            number = int(inp)
            if 0 <= elevator.occupancy+number <= ELEVATOR_CAPACITY:
                elevator.occupancy = elevator.occupancy + number
                print("В кабине {} людей ".format(elevator.occupancy))
                break
            else:
                print("Некорректное количество людей")
        else:
            print("Некорректный ввод. Введите целое число")


def moving(target):
    os.system('clear')
    print('Едем на {} этаж'.format(target))
    elevator.move(target)
    print("все")
    loading_people()


def check_if_possible_to_pick_up(target_level):
    print("Проверяем, можно ли подобрать пассажира по пути")
    if elevator.isMoving:
        if target_level in range(elevator.level, elevator.target) \
                or target_level in range(elevator.target, elevator.level):
            print("Нам по пути")
            elevator.stop()
            loading_people()
        else:
            print("Нам не по пути, иди в очередь")
            controller.add_to_queue(target_level)
    else:
        print("Сразу едь на вызов")
        elevator.move(target_level)


def calling(target_level):
    if elevator.isMoving:
        check_if_possible_to_pick_up(target_level)
    else:
        moving(target_level)


while True:
    # os.system('clear')
    call = input("Введите 'f' для вызова лифта, 't' для назначения или 'выход' для выхода : ")
    if "выход" in call:
        break
    inputed_level = input("введите этаж: ")
    if "выход" in inputed_level:
        break

    if is_int(inputed_level) and int(inputed_level) > 0:
        level = int(inputed_level)
        if level > NUMBER_OF_LEVELS:
            print("Неверный номер этажа")
        else:
            if "f" in call:
                print("Произошел вызов с {} этажа".format(level))
                calling(level)
            elif "t" in call:
                while elevator.occupancy == 0:
                    print("Лифт пустой, не может ехать")
                    loading_people()
                moving(level)

            else:
                print("Некорректный ввод " + call)
    else:
        print("Некорректный ввод "+inputed_level)
