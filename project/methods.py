import numpy as np

KNAPSACK_ITEMS = None


def random_search(v, n_iter, objective_func, bounds, minimize=True):
    """
    Performs random search optimization on a given objective function.
    :param v: Starting point for optimization.
    :param n_iter: Number of iterations for optimization.
    :param objective_func: Objective function to optimize.
    :param bounds: Tuple of arrays specifying the minimum and maximum bounds for search space. Defaults to None.
    :param minimize: Flag indicating whether to minimize or maximize objective function. Defaults to True.

    :returns ndarray: Best solution found during optimization.
    """
    best_x = list()
    best_x.append((v, objective_func(v), 0))

    for i in range(n_iter):
        x_new = np.random.uniform(bounds[0], bounds[1], v.shape)

        score = objective_func(x_new)
        if (minimize and score < best_x[-1][1]) or (
            not minimize and score > best_x[-1][1]
        ):
            best_x.append((x_new, score, i))

        v = x_new

    return best_x


def simulated_annealing(
    v,
    n_mpolis,
    temp,
    objective_func,
    f_temp,
    temp_target=0.1,
    stdev=0.1,
    bounds=None,
    space="spoj",
):
    """
    :param v: Starting point for optimization.
    :param n_mpolis: Number of metropolis iterations.
    :param temp: Starting temperature.
    :param objective_func: Objective function to optimize.
    :param f_temp: Function for temperature update.
    :param temp_target: Target temperature.
    :param stdev: Standard deviation for normal distribution.
    :param bounds: Tuple of arrays specifying the minimum and maximum bounds for search space. Defaults to None.
    :param space: Search space. Defaults to "spoj".
    :return:
    """
    v_best = list()
    v_best.append((v, objective_func(v), 0))
    while temp > temp_target:
        for i in range(n_mpolis):
            v_local = get_neighbours(space, v, stdev)
            if bounds is not None:
                v_local = np.clip(v_local, bounds[0], bounds[1])
            delta = objective_func(v_local) - objective_func(v)
            if delta < 0:
                v = v_local
                best_val = v_best[-1][1]
                new_val = objective_func(v_local)
                if new_val < best_val:
                    v_best.append((v_local, new_val, temp))
            elif np.random.uniform(0, 1) < np.exp(-delta / temp):
                v = v_local
        temp = temp - f_temp(temp)

    return v_best


def get_neighbours(space, v, stdev=0.1):
    if space == "spoj":
        return v + np.random.normal(0, stdev, v.shape)
    elif space == "disc":
        v_local = np.copy(v)
        for i in range(len(v)):
            if np.random.randint(0, len(v)) == len(v) - 1:
                v_local[i] = (v_local[i] + 1) % 2
        return v_local


def cooling(temp):
    return temp / (1 + temp * 0.95)


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


def knapsack(v, capacity=100) -> int:
    val = 0
    if len(v) > 30:
        capacity = 300
    elif len(v) > 15:
        capacity = 200

    for i in range(len(v)):
        if v[i] == 1:
            row = KNAPSACK_ITEMS[i]
            val += row[0]
            capacity -= row[1]
            if capacity < 0:
                return 1
    return -val


def generate_items(n=30):
    global KNAPSACK_ITEMS
    KNAPSACK_ITEMS = np.random.randint(1, 50, (n, 2))


if __name__ == "__main__":
    dejong_random = dict()
    dejong_annealing = dict()
    dejong2_random = dict()
    dejong2_annealing = dict()
    schwefel_random = dict()
    schwefel_annealing = dict()

    if False:
        for d in [5, 10]:
            dejong_random[d] = list()
            dejong_annealing[d] = list()
            dejong2_random[d] = list()
            dejong2_annealing[d] = list()
            schwefel_random[d] = list()
            schwefel_annealing[d] = list()

            for _ in range(30):
                vector1 = np.random.uniform(-50, 50, d)
                vector2 = np.random.uniform(0, 1000, d)

                dejong_random[d].append(
                    random_search(vector1, 10000, dejong, (-50, 50))
                )
                dejong_annealing[d].append(
                    simulated_annealing(
                        vector1, 10, 1000, dejong, cooling, 0.01, 0.5, (-50, 50)
                    )
                )
                dejong2_random[d].append(
                    random_search(vector1, 10000, dejong2, (-50, 50))
                )
                dejong2_annealing[d].append(
                    simulated_annealing(
                        vector1, 10, 1000, dejong2, cooling, 0.01, 0.5, (-50, 50)
                    )
                )
                schwefel_random[d].append(
                    random_search(vector2, 10000, schwefel, (0, 1000))
                )
                schwefel_annealing[d].append(
                    simulated_annealing(
                        vector2, 10, 1000, schwefel, cooling, 0.01, 0.5, (0, 1000)
                    )
                )

    knapsack_heuristic = dict()

    for d in [15, 30, 50]:
        knapsack_heuristic[d] = list()

        for _ in range(10):
            generate_items(d)
            knapsack_heuristic[d].append(
                simulated_annealing(
                    [0] * d, 10, 40 * d, knapsack, cooling, 0.01, 0.5, (0, 1), "disc"
                )
            )

    print("Konec")
    quit()
