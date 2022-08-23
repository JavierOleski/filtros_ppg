import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def decimal_str(x: float, decimals: int = 22) -> str:
    return format(x, f".{decimals}f").lstrip().rstrip('0')


Fs = 50
fc1 = 0.1
fc2 = 10

wc1 = (2 * fc1) / Fs
wc2 = (2 * fc2) / Fs

Wn = [wc1, wc2]

wk = []


b, a = signal.butter(3, Wn, btype='bandpass', analog=False, output='ba', fs=Fs)


print(b)
print(a)
