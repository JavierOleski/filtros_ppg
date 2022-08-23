import numpy as np
from scipy.signal import convolve, freqz
import matplotlib.pyplot as plt


def calc_magnitude_1(w, wc):  #calculate the magnitude for one component of the filter
    return wc/((wc**2 + w**2)**0.5)


def calc_magnitude(w, wc):  #calculate the total magnitude for the frequency w
    magnitude = 1
    for j in range(len(wc)):
        magnitude = magnitude * calc_magnitude_1(w, wc[j])
    return magnitude


def calc_P_1(i, w, wc):  #calculate one component of the P vector for the frequency w
    magnitude = 1
    for j in range(len(wc)):
        if (i != j):
            magnitude = magnitude * calc_magnitude_1(w, wc[j])
    return magnitude


def calc_P(w, wc):  #calculate the P vector for the frequency w
    P=[]
    for j in range(len(wc)):
        P.append(calc_P_1(j, w, wc))
    return P


def calc_cost(w1, A1, w2, A2, wc):  #return the total cost
    cost = 0.5 * ((A1 - calc_magnitude(w1, wc))**2 + (A2 - calc_magnitude(w2, wc))**2)
    return cost


def calc_cost_derivative_1(w1, A1, w2, A2, P_w1, P_w2, wc, i):  #return the derivative of the cost respect to one wci
    derivative = (A1 - calc_magnitude(w1, wc))*((-P_w1[i]*(w1**2))/((wc[i]**2 + w1**2)**1.5)) + (A2 - calc_magnitude(w2, wc))*((-P_w2[i]*(w2**2))/((wc[i]**2 + w2**2)**1.5))
    return derivative


def cal_cost_derivative(w1, A1, w2, A2, P_w1, P_w2, wc):  #return the vector of the cost's derivative
    cost_derivative = []
    for i in range(len(wc)):
        cost_derivative.append(calc_cost_derivative_1(w1, A1, w2, A2, P_w1, P_w2, wc, i))
    return cost_derivative


def lowpass_filter_design(ts, wc_l):
    nh_out = []
    dh_out = []
    for i, wc in enumerate(wc_l):
        n0l = (wc * ts) / (wc * ts + 2)
        n1l = n0l
        d0l = 1
        d1l = ((wc * ts - 2) / (wc * ts + 2))
        nl = [n0l, n1l]
        dl = [d0l, d1l]
        if i == 0:
            nh_out = nl
            dh_out = dl
        else:
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


Fs = 50
ts = 1/Fs

f1 = 12
A1 = 0.95
w1 = 2 * np.pi * f1

f2 = 30
A2 = 0.2
w2 = 2 * np.pi * f2

alpha = 0.5
max_cost = 0.0273

wc = [60, 120]

J = calc_cost(w1, A1, w2, A2, wc)
Jdifference = 0
#print(J)

while J > max_cost:
    try:
        P_w1 = calc_P(w1, wc)
        P_w2 = calc_P(w2, wc)
        derivative = cal_cost_derivative(w1, A1, w2, A2, P_w1, P_w2, wc)
        for i in range(len(wc)):
            wc[i] = wc[i] - alpha*derivative[i]
        J = calc_cost(w1, A1, w2, A2, wc)
        print(J)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break

print("wc = {}".format(wc))
print("cost J = {}".format(J))

n, d = lowpass_filter_design(ts, wc)

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
