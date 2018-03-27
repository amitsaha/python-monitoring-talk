import random
import matplotlib.pyplot as plt

data = [5, 3, 4, 6, 7, 5, 10]

plt.xkcd()

plt.plot(data)
plt.xlabel('Time')
plt.ylabel('Metric')
plt.title('Gauge')

plt.grid()
plt.show()
