# Дана СМО типа M/M/2/0/infty. 
# Построить имитационную модель системы. 
# На основании 10^6 выборочных значений оценить u, n 
# и вероятность отказа требованию в обслуживании. 

from math import log
from random import random
import numpy as np

class Demand:
    def __init__(self, born, begin_service, death):
        self.born_time = born
        self.begin_service = begin_service
        self.death_time = death

    def getinfo(self):
        print(f'Время поступления в СМО: {self.born_time}')
        print(f'Время поступления на прибор: {self.begin_service}')
        print(f'Время выхода из СМО: {self.death_time}')


# ввод параметров
t_modeling = 1000000 # время моделирования
lambda_ = 10
mu = 2
k = 2

t_act_source = 0 # момент генерации требования
t_act_device1 = 0 # момент начала обслуживания требования 1
t_act_device2 = 0 # момент начала обслуживания требования 2
t_now = 0 # текущее время
device1_free = True # индикатор занятости первого прибора
device2_free = True # индикатор занятости второго прибора
demands = [] # коллекция с прошедшими через систему требованиями
N = 0 # число требований в системе
cnt_refuse = 0 # число требований с отказом
n = []
t_born = [0] * k + [0] # моменты поступления требований
t_service1 = [0, 0] # поступил / обслужился
t_service2 = [0, 0]
cnt_getting_demands = 0

rnd = random() # здесь или в теле симуляции?

# начальные условия
t_act_source = 0
t_act_device1 = t_modeling + 0.000001
t_act_device2 = t_modeling + 0.000001

# симуляция
while t_now < t_modeling:
    indicator = False
    # генерация требования
    if (t_act_source == t_now):
        print(f"Момент формирования требования: {t_now}")
        indicator = True
        N += 1
        if t_born[0] == 0:
            t_born[0] = t_now
        elif t_born[1] == 0:
            t_born[1] = t_now
        else:
            t_born[2] = t_now
        cnt_getting_demands += 1
        # print(t_born)
        t_act_source = t_now - log(rnd) / lambda_
    
    # начало обслуживания требования прибором 1
    if (device1_free and N > 0):
        print(f"Момент начала обслуживания прибором 1: {t_now}")
        indicator = True
        device1_free = False
        t_act_device1 = t_now - log(rnd) / mu
        # t_act_source = t_now - log(rnd) / lambda_
        # N += 1 #???
        t_service1[0] = t_now
    # начало обслуживания требования прибором 2
    elif (device2_free and N > 1):
        print(f"Момент начала обслуживания прибором 2: {t_now}")
        indicator = True
        device2_free = False
        t_act_device2 = t_now - log(rnd) / mu
        # t_act_source = t_now - log(rnd) / lambda_
        # N += 1 #???
        t_service2[0] = t_now
    # отказ
    elif N > 2:
        N -= 1
        t_born[2] = 0
        cnt_refuse += 1
        
    # завершение обслуживания требования прибором 1
    if (t_act_device1 == t_now):
        print(f"Момент завершения обслуживания: {t_now}")
        t_service1[1] = t_now
        indicator = True
        device1_free = True
        t_act_device1 = t_modeling + 0.0000001
        print(f"Момент поступления: {t_service1[0]}\nМомент выхода из СМО: {t_now}")
        N -= 1
        demands.append(Demand(t_born[0], t_service1[0], t_service1[1]))
        t_born[0] = 0

    # завершение обслуживания требования прибором 2
    if (t_act_device2 == t_now):
        print(f"Момент завершения обслуживания: {t_now}")
        t_service2[1] = t_now
        indicator = True
        device2_free = True
        t_act_device2 = t_modeling + 0.0000001
        print(f"Момент поступления: {t_service2[0]}\nМомент выхода из СМО: {t_now}")
        N -= 1
        demands.append(Demand(t_born[1], t_service2[0], t_service2[1]))
        t_born[1] = 0

    # переход к следующему моменту
    if not indicator:
        n.append(N)
        # print(N)
        t_now = min(t_act_device1, t_act_device2, t_act_source)


# анализ данных
u = []
for item in demands:
    u.append(item.death_time - item.born_time)
    # print(u[-1])
n_ = np.mean(n)
u_ = np.mean(u)
p_ref = cnt_refuse / cnt_getting_demands
print(f'Число обслуженных требований: {len(demands)}')
print(f'М.о. длительности пребывания требований в системе u_ = {u_}')
print(f'М.о. числа требований в системе n_ = {n_}')
print(f'Вероятность отказа = {p_ref}')

# for item in demands:
#     print(f'Требование {demands.index(item)}')
#     item.getinfo()