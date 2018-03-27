import random
import matplotlib.pyplot as plt

data = [5, 10, 20, 25]

plt.xkcd()

plt.plot(data)
plt.xlabel('Time')
plt.ylabel('Metric')
plt.title('Counter')

plt.grid()
plt.show()
