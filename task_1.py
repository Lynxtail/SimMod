# распределение равномерное дискретное
from cmath import sqrt
from random import randint

S = 9
in_square_s = 1

ex_max = 10000

K = int(S / in_square_s)
f = open('output.txt', 'w')
for ex in range(ex_max):
    cnt = 0
    x = [False] * K # квадраты
    while not all(x):
        k = randint(0, K - 1) # случайное число [0, 9)
        x[k] = True
        cnt += 1
    f.write(f"{cnt}\n")
f.close()

f = open('output.txt', 'r')
e = 0
cnt_lines = 0
for line in f:
    e += int(line)
    cnt_lines += 1
e /= cnt_lines
f.close()

f = open('output.txt', 'r')
std = 0
for line in f:
    std += (int(line) - e)
std /= (cnt_lines - 1)
std = sqrt(std)
f.close()

print(f'Оценка мат. ожидания: {e}')
print(f'Среднее квадр. отклонение: {std}')