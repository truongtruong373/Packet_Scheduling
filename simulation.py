import numpy as np
import matplotlib.pyplot as plt

loads = np.arange(0.1, 0.99, 0.01)

fifo  = []

pim   = []

islip = []

ilru  = []

msm   = []

plt.figure(figsize=(5,6))

plt.plot(loads * 100, fifo,marker='.',linewidth=2,label='FIFO')
plt.plot(loads * 100, pim,marker='.',linewidth=2,label='PIM')
plt.plot(loads * 100, islip,marker='.',linewidth=2,label='iSLIP')
plt.plot(loads * 100, ilru,marker='.',linewidth=2,label='iLRU')
plt.plot(loads * 100, msm,marker='.',linewidth=2,label='MSM')

plt.xlabel("Tải (%)")

plt.ylabel("Trễ trung bình")

plt.legend()
plt.tight_layout()
plt.show()