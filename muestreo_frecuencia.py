import numpy as np
from scipy.signal import freqz
import matplotlib.pyplot as plt


def decimal_str(x: float, decimals: int = 22) -> str:
    return format(x, f".{decimals}f").lstrip().rstrip('0')


N = 300
Fs = 50
fc1 = 0.1
fc2 = 10

wc1 = (2 * np.pi * fc1) / Fs
wc2 = (2 * np.pi * fc2) / Fs

M = (N - 1) / 2

wk = []

for k in range(0, N-1):
    w = (2 * np.pi * k) / N
    if wc1 <= w and w <= wc2:
        wk.append(k)

#print(wk)

hn = []
a = [1]

for n in range(0, N-1):
    hk = 0
    for k in range(0, len(wk)):
        hk = hk + np.cos((2 * np.pi * wk[k] * (n - M)) / N)
    h = (2 / N) * hk
    hn.append(h)

print(hn)

chain = ""
for i in range(len(hn)):
    if i == 0:
        chain = chain + "["
    elif i == 1:
        chain = chain + "{}".format(hn[i])
    elif i == len(hn) - 1:
        chain = chain + ",{}".format(hn[i]) + "]"
    else:
        chain = chain + ",{}".format(hn[i])


print("Coeficientes: ")
print(chain)
