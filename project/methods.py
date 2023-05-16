import numpy as np


def random_search(v, n, f, stdev=0.1, bounds=None, type="min"):
    best = v
    for i in range(n):
        v = v + np.random.normal(0, stdev, v.shape)
        if bounds is not None:
            v = np.clip(v, bounds[0], bounds[1])
        if type == "min":
            if f(v) < f(best):
                best = v
        else:
            if f(v) > f(best):
                best = v
    return v


def annealing(v, n, f):
    for i in range(n):
        v = v + np.random.normal(0, 0.1, v.shape)
        v = np.clip(v, -1.0, 1.0)
        if f(v) > f(v - np.random.normal(0, 0.1, v.shape)):
            v = v - np.random.normal(0, 0.1, v.shape)
        else:
            v = v - np.random.normal(0, 0.1, v.shape) * np.exp(-i / n)
    return v


def hill_climbing(v, n, f):
    for i in range(n):
        v = v + np.random.normal(0, 0.1, v.shape)
        v = np.clip(v, -1.0, 1.0)
        if f(v) > f(v - np.random.normal(0, 0.1, v.shape)):
            v = v - np.random.normal(0, 0.1, v.shape)
    return v


def dejong(v):
    result = 0
    for i in range(len(v)):
        result += v[i] ** 2
    return result


def dejong2(v):
    result = 0
    for i in range(len(v) - 1):
        result += 100 * (v[i] ** 2 - v[i + 1]) ** 2 + (1 - v[i]) ** 2
    return result


def schwefel(v):
    result = 0
    for i in range(len(v)):
        result += -v[i] * np.sin(np.sqrt(np.abs(v[i])))
    return result


def knapsack(v, n, f):
    for i in range(n):
        v = v + np.random.normal(0, 0.1, v.shape)
        v = np.clip(v, -1.0, 1.0)
        if f(v) > f(v - np.random.normal(0, 0.1, v.shape)):
            v = v - np.random.normal(0, 0.1, v.shape)
        else:
            v = v - np.random.normal(0, 0.1, v.shape) * np.exp(-i / n)
    return v


if __name__ == "__main__":
    start = [534, 232]
    vector1 = np.array(start)
    print("Random Search" + str(random_search(vector1, 10000, dejong, 0.1, (0, None))))
