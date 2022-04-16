# Построить модель бросания точек на квадрат 
# со стороной 2. Оценить площадь круга, 
# вписанного в этот квадрат на основании 
# 30, 60, 100, 1000, 10000 точек.

from random import random
from math import pi

a = 2
s_square = a ** 2
r = a / 2
s_circle = pi * r ** 2

# теоретическая вероятность попадания в круг
p = s_circle / s_square
print(f'Теоретическая вероятность попадания в круг: {p}')

cnt_dots = [30, 60, 100, 1000, 10000]
dots_max = cnt_dots[-1]
dots_in_square = 0
dots_in_circle = 0
for cnt in range(dots_max + 1):
    r = random()
    if r <= p:
        dots_in_circle += 1
    else:
        dots_in_square += 1
    if cnt_dots.count(cnt) != 0:
        print('-' * 50)
        print(f'Результаты для {cnt} точек:')
        print(f'\tЧисло точек внутри круга: {dots_in_circle}')
        print(f'\tЧисло точек внутри квадрата, но не круга: {dots_in_square}')
        print(f'\tОценка площади круга: {dots_in_circle / dots_in_square}')
        print(f'\tПлощадь идеально вписанного круга: {s_circle}\n')