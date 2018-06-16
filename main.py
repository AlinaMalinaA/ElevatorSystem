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


# флаг для остановки треда, следящего за очередью,
# чтобы вставить в очередь вызвавший этаж
# и тем самым подменить цель лифта на промежуточную
flag = True


def check_if_possible_to_pick_up(target_level: int):
    print("Проверяем, можно ли подобрать пассажира по пути")
    # здесь проверка, находится ли этаж, с которого пришел вызов
    # по пути следования лифта, то есть между актульными этажом и этажом-целью
    # если лифт едет наверх, то все просто
    # но если лифт едет вниз, надо проверять,
    # находится ли этаж между целью (меньшее число) и актуальным этажом (большее число)
    # так как вызов мог прийти с актуального этажа, и значит есть смысл остановиться
    if controller.is_that_not_our_target(target_level):
        a, b = controller.give_the_range_of_levels_that_left()
        temp = int(target_level)
        if not is_int(temp):
            print("ОПАНЬКИ! С темпом что-то не то ", temp)
        else:
            if temp in range(int(a), int(b)):
                print("Нам по пути")
                flag = False
                controller.stop_the_elevator()
                request_queue.insert(0, controller.where_do_we_go())
                request_queue.insert(0, target_level)
                flag = True
                # loading_people()
            else:
                print("Нам не по пути, иди в очередь")
                request_queue.append(target_level)
    else:
        request_queue.insert(0, target_level)


# если лифт вызвали
# то подготовить лифт
# и проверить, можно ли подсадить вызвавшего пассажира
# если свободен - сразу ехать на вызов
def calling(target_level: int):
    if is_level_okay(target_level):
        controller.prepare_elevator(target_level)
        if controller.is_that_not_our_target(target_level):
            check_if_possible_to_pick_up(int(target_level))
        else:
            moving(target_level)
    else:
        print("неверный этаж")


def is_level_okay(level):
    if is_int(level) and 0 < int(level) <= NUMBER_OF_LEVELS:
        return True
    else:
        return False

# очередь вызовов
# по заданию - запросы обрабатываются в порядке поступления,
# поэтому нет никаких проверок на минимальный, максимальный элементы и прочих оптимизаций
request_queue = []


# метод для треда, который следит за движением лифта и очередь
def moving_permanent():
    while True:
        while len(request_queue) > 0:
            if not controller.is_elev_moving():
                moving(request_queue.pop(0))


def command_distributor():
    while True:
        global request_queue
        # спрашиваем команду
        print_condition()
        command = input("Введите 'f' для вызова лифта, 't' для назначения или 'выход' для выхода : ")
        if command == 'выход':
            break

        inputed_level = input("Введите номер этажа, с которого пришел вызов ")
        if is_level_okay(inputed_level):
            if command == 'f':
                check_if_possible_to_pick_up(inputed_level)
            elif command == 't':
                while controller.if_elevator_empty():
                    print("Лифт пустой, не может ехать")
                    loading_people()
                request_queue.insert(0, inputed_level)
            else:
                print("Некорректный ввод команды")
        else:
            print("Некорректный номер этажа")


def calculate_time_for_waiting():
    global request_queue
    print("Длина очереди ", len(request_queue))
    time_for_wait = 0
    previous_target = controller.where_are_we_now()
    for el in request_queue:
        time_for_wait += math.fabs(previous_target - int(el)) * ELEVATOR_DELAY

        previous_target = int(el)
        print("Для {} этажа время ожидания составляет {} секунд".format(el, time_for_wait))

    print(request_queue)


# главный тред, в котором читается инпут и отдаются команды
main_thread_for_input = threading.Thread(target=command_distributor)
# тред для слежения за очередью
tread_for_moving = threading.Thread(target=moving_permanent)

main_thread_for_input.start()
tread_for_moving.start()
main_thread_for_input.join()
