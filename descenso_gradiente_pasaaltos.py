import numpy as np
from scipy.signal import convolve, freqz
import matplotlib.pyplot as plt


def calc_magnitude_1(w, wc):  #calculate the magnitude for one component of the filter
    return w/((wc**2 + w**2)**0.5)


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
    cost = 0.5 * ((A1 - calc_magnitude(w1,wc))**2 + (A2 - calc_magnitude(w2,wc))**2)
    return cost


def calc_cost_derivative_1(w1, A1, w2, A2, P_w1, P_w2, wc, i):  #return the derivative of the cost respect to one wci
    derivative = (A1 - calc_magnitude(w1,wc))*(P_w1[i]*wc[i]*w1/((wc[i]**2 + w1**2)**1.5)) + (A2 - calc_magnitude(w2,wc))*(P_w2[i]*wc[i]*w2/((wc[i]**2 + w2**2)**1.5))
    return derivative


def cal_cost_derivative(w1, A1, w2, A2, P_w1, P_w2, wc):  #return the vector of the cost's derivative
    cost_derivative = []
    for i in range(len(wc)):
        cost_derivative.append(calc_cost_derivative_1(w1, A1, w2, A2, P_w1, P_w2, wc, i))
    return cost_derivative

def highpass_filter_design(ts, w):
    nh_out = []
    dh_out = []
    for i in range(len(w)):
        print(i)
        n0h = 2 / (2 + ts * w[i])
        n1h = -n0h
        d0h = 1
        d1h = -((2 - w[i] * ts) / (2 + w[i] * ts))
        n = [n0h, n1h]
        d = [d0h, d1h]
        if i == 0:
            nh_out = n
            dh_out = d
        else:
            nh_out = convolve(nh_out, n)
            dh_out = convolve(dh_out, d)
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

f1 = 0.1
A1 = 0.25
w1 = 2 * np.pi * f1

f2 = 0.65
A2 = 0.96
w2 = 2 * np.pi * f2

alpha = 0.005
max_cost = 0.0001

#wc = [1,0.5,0.8,1.2,1.4]
wc = [1.0, 1.6, 1.5]

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


n, d = highpass_filter_design(ts, wc)

frequency_response(n, d, Fs)

print("numeradores")
chain = ""
for i in range(len(n)):
    chain = chain+", {}".format(n[i])
print(chain)

print("denominadores")
chain = ""
for i in range(len(d)):
    chain = chain+", {}".format(d[i])
print(chain)
