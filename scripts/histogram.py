import random
import matplotlib.pyplot as plt

def generate_random_numbers(N):
    numbers = []
    for _ in range(N):
        numbers.append(random.uniform(15, 60))
    return numbers


if __name__ == '__main__':
    data = generate_random_numbers(100)

    plt.xkcd()

    plt.hist(data)
    plt.xlabel('Age Group')
    plt.title('Histogram')

    plt.grid()
    plt.show()
