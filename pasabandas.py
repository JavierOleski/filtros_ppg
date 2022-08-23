import numpy as np
from scipy.signal import convolve, freqz
import matplotlib.pyplot as plt


def bandpass_full_design(ts, wc_h, wc_l):
    nh_out = 1
    dh_out = 1
    for i, wc in enumerate(wc_h):
        n0h = 2 / (2 + ts * wc)
        n1h = -n0h
        d0h = 1
        d1h = -((2 - wc * ts) / (2 + wc * ts))
        nh = [n0h, n1h]
        dh = [d0h, d1h]
        print(i)
        if i == 0:
            nh_out = nh
            dh_out = dh
        else:
            nh_out = convolve(nh_out, nh)
            dh_out = convolve(dh_out, dh)

    for i, wc in enumerate(wc_l):
        n0l = (wc * ts) / (wc * ts + 2)
        n1l = n0l
        d0l = 1
        d1l = ((wc * ts - 2) / (wc * ts + 2))
        nl = [n0l, n1l]
        dl = [d0l, d1l]
        nh_out = convolve(nh_out, nl)
        dh_out = convolve(dh_out, dl)
    return nh_out, dh_out


def frequency_response(b, a, fs):
    SIZE = 18
    plt.rc('font', size=SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SIZE)  # legend fontsize
    plt.rc('figure', titlesize=SIZE)  # fontsize of the figure title

    w, h = freqz(b, a, worN=2000)
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="Respuesta pasa-banda")
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Ganancia')
    plt.legend(loc='best')
    plt.grid(True)


# Code begin

Fs = 50
ts = 1/Fs

wc_h = [0.522787128905071, 0.9305094524899372, 0.8639333328179312] # frecuencias de corte pasaalto

wc_l = [131.5858662053576, 142.56636098135337] # frecuencias de corte pasabajos

n, d = bandpass_full_design(ts, wc_h, wc_l)

frequency_response(n, d, Fs)

print("Numeradores:")
chain = ""
for i in range(len(n)):
    chain = chain + ", {}".format(n[i])
print(chain)

print("Denominadores:")
chain = ""

for i in range(len(d)):
    chain = chain + ", {}".format(d[i])
print(chain)
