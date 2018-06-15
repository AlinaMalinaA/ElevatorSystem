#!/usr/bin/env python3
import controller
import paramsLoader
import os
import math
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


def print_condition():
    # os.system('clear')
    print("Где лифт сейчас?", controller.where_are_we_now())
    print("Сколько людей внутри?", controller.how_much_people_inside())
    calculate_time_for_waiting()


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
    calculate_time_for_waiting()
    controller.move(target)
    # loading_people()


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
        # loading_people()
    else:
        print("Нам не по пути, иди в очередь")
        controller.add_to_queue(target_level)


# если лифт вызвали
# то подготовить лифт
# и проверить, можно ли подсадить вызвавшего пассажира
# если свободен - сразу ехать на вызов
def calling(target_level):
    if is_level_okay(target_level):
        controller.prepare_elevator(target_level)
        if controller.is_that_our_target(target_level):
            check_if_possible_to_pick_up(target_level)
        else:
            moving(target_level)
    else:
        print("неверный этаж")


def is_level_okay(level):
    if is_int(level) and 0 < int(level) <= NUMBER_OF_LEVELS:
        return True
    else:
        return False


request_queue = []


def command_distributor():
    while True:
        global request_queue
        # спрашиваем команду
        print_condition()

        command = input("Введите 'f' для вызова лифта, 't' для назначения или 'выход' для выхода : ")

        if command == 'выход':
            break
        if command == 'f':
            inputed_level = input("Введите номер этажа, с которого пришел вызов ")
            # проверка на повтор?
            request_queue.append(inputed_level)
            # проверка, если занят, то в очередь и не удалять элемент, пока не доедем до него
            calling(inputed_level)
            request_queue.remove(inputed_level)
        elif command == 't':
            while controller.if_elevator_empty():
                print("Лифт пустой, не может ехать")
                loading_people()
                inputed_level = input("Введите номер этажа, на который надо ехать ")
            # проверка на повтор?
            request_queue.append(inputed_level)
            moving(inputed_level)
            request_queue.remove(inputed_level)
        else:
            print("Некорректный ввод команды")


def calculate_time_for_waiting():
    global request_queue
    print("Длина очереди ", len(request_queue))
    time_for_wait = 0
    previous_target = controller.where_are_we_now()
    for el in request_queue:
        time_for_wait += math.fabs(previous_target - int(el)) * ELEVATOR_DELAY

        previous_target = int(el)
        print("Для {} этажа время ожидания составляет {} секунд".format(el, time_for_wait))


main_thread_for_input = threading.Thread(target=command_distributor)


main_thread_for_input.start()
main_thread_for_input.join()
