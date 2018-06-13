#!/usr/bin/env python3
import controller
import paramsLoader
import os
import threading


NUMBER_OF_LEVELS = paramsLoader.what_number_of_levels()
ELEVATOR_CAPACITY = paramsLoader.what_capacity_of_elevator()
ELEVATOR_DELAY = paramsLoader.what_delay_between_levels()


controller = controller.Controller(ELEVATOR_DELAY)


# проверяет, является ли число целым
def is_int(k):
    try:
        int(k)
        return True
    except (TypeError, ValueError):
        return False


def loading_people():
    while True:
        print("В кабине {} людей ".format(controller.how_much_people_inside()))
        print("Сколько людей вошло или вышло? Больше {} войти не может.".format(ELEVATOR_CAPACITY))
        inp = input('Напишите положительное число для входящих людей и отрицательное для выходящих: ')
        if is_int(inp):
            number = int(inp)
            if 0 <= controller.how_much_people_inside() + number <= ELEVATOR_CAPACITY:
                controller.load_people(number)
                break
            else:
                print("Некорректное количество людей")
        else:
            print("Некорректный ввод. Введите целое число")


def moving(target):
    # os.system('clear')
    print('Едем на {} этаж'.format(target))
    controller.prepare_elevator(target)
    print("Время ожидания ", time_for_waiting())
    controller.move(target)
    loading_people()


def check_if_possible_to_pick_up(target_level):
    print("Проверяем, можно ли подобрать пассажира по пути")
    # здесь проверка, находится ли этаж, с которого пришел вызов
    # по пути следования лифта, то есть между актульными этажом и этажом-целью
    # если лифт едет наверх, то все просто
    # но если лифт едет вниз, надо проверять,
    # находится ли этаж между целью (меньшее число) и актуальным этажом (большее число)
    # и так как в функции range() правая точка не включается, приходится делать +1
    # так как вызов мог прийти с актуального этажа, и значит есть смысл остановиться
    a, b = controller.give_the_range_of_levels_that_left()
    if target_level in range(a, b):
        print("Нам по пути")
        controller.stop_and_pick_up(target_level)
        loading_people()
    else:
        print("Нам не по пути, иди в очередь")
        controller.add_to_queue(target_level)


# если лифт вызвали
# то подготовить лифт
# и проверить, можно ли подсадить вызвавшего пассажира
# если свободен - сразу ехать на вызов
def calling(target_level):
    controller.prepare_elevator(target_level)
    if controller.is_that_our_target(target_level):
        check_if_possible_to_pick_up(target_level)
    else:
        moving(target_level)


def ask_for_level():
    inputted_level = input("Введите этаж: ")
    if is_int(inputted_level) and 0 < int(inputted_level) <= NUMBER_OF_LEVELS:
        return int(inputted_level)
    else:
        print("Неверный номер этажа")


def received_call_from():
    target_level = ask_for_level()
    calling(target_level)


def asked_to_move_to():
    while controller.if_elevator_empty():
        print("Лифт пустой, не может ехать")
        loading_people()
    target_level = ask_for_level()
    moving(target_level)


def waiting_for_input():
    if len(controller.levels_queue) > 0:
        calling(controller.get_max_level_from_queue())
    while True:
        call = input("Введите 'f' для вызова лифта, 't' для назначения или 'выход' для выхода : ")
        if call == 'выход':
            break
        if call == 'f':
            received_call_from()
        elif call == 't':
            asked_to_move_to()
        else:
            print("Некорректный ввод команды")


# поток ждет своего часа
# t3 = threading.Thread(target=waiting_for_input)

def time_for_waiting():
    a, b = controller.give_the_range_of_levels_that_left()
    return ELEVATOR_DELAY*(b-a)


waiting_for_input()