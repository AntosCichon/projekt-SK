import numpy as np
import matplotlib.pyplot as plt

data = [
"0;5;4",
"1;3;5",
"2;6;3"
]
cnt = len(data)

a = [data[i].split(';')[0] for i in range(cnt)]
b = [data[i].split(';')[-1] for i in range(cnt)]

fig, axs = plt.subplots(1, 1)
axs.bar(a, b)
plt.show()