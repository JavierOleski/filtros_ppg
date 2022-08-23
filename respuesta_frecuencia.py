import numpy as np
from scipy.signal import freqz
import matplotlib.pyplot as plt


def frequency_response(b, a, fs, resolucion):
    SIZE = 18
    plt.rc('font', size=SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SIZE)  # legend fontsize
    plt.rc('figure', titlesize=SIZE)  # fontsize of the figure title

    w, h = freqz(b, a, worN=resolucion)

    w1 = (fs * 0.5 / np.pi) * w
    h1 = abs(h)

    plt.plot(w1, h1, label="Filtro clásico con aproximación Descenso de Gradiente")
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Ganancia')
    plt.legend(loc='best')
    plt.grid(True)

    return w1, h1


def tRetraso(w, h):
    #tiempo al alcanzar el 50% del valor final
    for i in range(0, len(w)):
        if h[i] > 0.5:
            Tr = w[i]
            break
    return round(Tr, 4)


def tSubida(w, h):
    #tiempo de 0 a 1
    for i in range(0, len(w)):
        if h[i] >= 0.98:
            Ts = w[i]
            break
    return round(Ts, 4)


def tBajada(w, h):
    #tiempo de 1 a 0
    T1 = 0
    for i in range(0, len(w)):
        if T1 == 0:
            if h[i] >= 0.985:
                T1 = 1
        elif T1 == 1:
            if h[i] <= 0.001:
                Tb = w[i]
                break
    return round(Tb, 4)


def sobrePico(w, h):
    #diferencia porcentual entre pico máximo y valor de estabilidad
    Ve = 0.96
    Pm = 0
    for i in range(0, len(w)):
        if h[i] > Pm :
            Pm = h[i]

    sP = abs((Ve - Pm)/Ve)*100
    return round(sP, 2)

def tEstablecimiento(w, h):
    #el tiempo requerido para que la respuesta se establezca en un porcentaje específico de su valor final
    for i in range(0, len(w)):
        if h[i] > 0.9:
            Te = w[i]
            break
    return round(Te, 4)




fs = 50
resolucion = 10000

b = [0.32633285275629853, -0.32633285275629853, -0.6526657055125971, 0.6526657055125971, 0.32633285275629853, -0.32633285275629853]
a = [1.0, -2.642156547213316, 2.0113972003244114, -0.11825555764430618, -0.2281305582548424, -0.022850148503988095]



print(b)

print(len(b))

w, h = frequency_response(b, a, fs, resolucion)

Tr = tRetraso(w, h)

print("Tiempo de retraso: ", Tr, "Hz")


Ts = tSubida(w, h)

print("Tiempo de subida: ", Ts, "Hz")


Tb = tBajada(w, h)

print("Tiempo de bajada: ", Tb, "Hz")


sP = sobrePico(w, h)

#print("Sobre pico: ", sP, "Hz")

Te = tEstablecimiento(w, h)

print("Tiempo de establecimiento: ", Te, "Hz")


print("Cantidad de memoria: ", (len(a) + len(b))*4, "bytes")
