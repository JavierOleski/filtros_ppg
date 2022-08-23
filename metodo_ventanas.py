import numpy as np


def blackman_design(fh1, fh2, fl1, fl2, ts):
    fh = fh2 - fh1
    fl = fl2 - fl1
    if fh < fl:
        f = fh
    else:
        f = fl
    f = round(f, 4)
    M = (5.56 * ts) / f
    M = round(M, 0)
    if M % 2 == 0:
        M = M + 1

    print("El orden recomendado es de:")
    print(M)
    return int(M)

def rectangular_design(fh1, fh2, fl1, fl2, ts):
    fh = fh2 - fh1
    fl = fl2 - fl1
    if fh < fl:
        f = fh
    else:
        f = fl
    f = round(f, 4)
    M = (0.92 * ts) / f
    M = round(M, 0)
    if M % 2 == 0:
        M = M + 1

    print("El orden recomendado es de:")
    print(M)
    return int(M)

def hann_hamm_design(fh1, fh2, fl1, fl2, ts):
    fh = fh2 - fh1
    fl = fl2 - fl1
    if fh < fl:
        f = fh
    else:
        f = fl
    f = round(f, 4)
    M = (3.11 * ts) / f
    M = round(M, 0)
    if M % 2 == 0:
        M = M + 1

    print("El orden recomendado es de:")
    print(M)
    return int(M)

def decimal_str(x: float, decimals: int = 22) -> str:
    return format(x, f".{decimals}f").lstrip().rstrip('0')

def rectangular_window():
    wn = 1
    return wn

def blackman_window(n, M):
    wn = 0.42 - 0.5 * (np.cos((2 * np.pi * n) / (M-1))) + 0.08 * (np.cos((4 * np.pi * n) / (M - 1)))
    return wn

def han_window(n, M):
    wn = 0.5 - 0.5 * (np.cos((2 * np.pi * n) / (M - 1)))
    return wn

def hamming_window(n, M):
    wn = 0.54 - 0.46 * (np.cos((2 * np.pi * n) / (M - 1)))
    return wn


fh1 = 0.05
fh2 = 0.15
fl1 = 9.5
fl2 = 10.5
ts = 50

wc1 = ((fh1 + fh2) * np.pi) / ts
wc2 = ((fl1 + fl2) * np.pi) / ts

b = []

M = hann_hamm_design(fh1, fh2, fl1, fl2, ts)

for n in range(M):
    nf = n - (M - 1) / 2
    if n == (M - 1) / 2:
        hd = (wc2 - wc1) / np.pi
    else:
        hd = (np.sin(wc2 * nf) - np.sin(wc1 * nf)) / (np.pi * nf)

    wn = han_window(n, M)
    hn = hd * wn

    b.append(decimal_str(hn))

chain = ""
for i in range(len(b)):
    chain = chain + ", {}".format(b[i])

print("Coeficientes: ")
print(chain)