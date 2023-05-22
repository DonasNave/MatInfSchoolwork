import numpy as np
import math
import matplotlib.pyplot as plt

KNAPSACK_ITEMS = None

FES = 20000
METROPOLIS_ITER = 10
TARGET_TEMP = 0.0001
INIT_TEMP = 1000


def random_search(v, n_iter, objective_func, bounds, minimize=True, space="spoj"):
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
        if space == "spoj":
            x_new = np.random.uniform(bounds[0], bounds[1], v.shape)
        elif space == "disc":
            x_new = np.random.randint(0, 2, len(v))

        score = objective_func(x_new)
        if (minimize and score < best_x[-1][1]) or (
                not minimize and score > best_x[-1][1]
        ):
            best_x.append((x_new, score, i))

        v = x_new

    best_x.append((best_x[-1][0], best_x[-1][1], n_iter))
    return best_x


def simulated_annealing(
        v,
        n_mpolis,
        temp,
        objective_func,
        f_temp,
        temp_target=0.1,
        stdev=lambda x: 0.1,
        bounds=None,
        minimize=True,
        space="spoj"
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
    :param minimize: Flag indicating whether to minimize or maximize objective function. Defaults to True.
    :param space: Search space. Defaults to "spoj".
    :return:
    """
    v_best = list()
    fes_counter = 0
    v_best.append((v, objective_func(v), temp))
    while temp > temp_target:
        for i in range(n_mpolis):
            fes_counter += 1
            v_local = get_neighbours(space, v, stdev(temp))
            if bounds is not None:
                v_local = np.clip(v_local, bounds[0], bounds[1])
            delta = objective_func(v_local) - objective_func(v)
            if not minimize:
                delta = -delta
            if delta < 0:
                v = v_local
                best_val = v_best[-1][1]
                new_val = objective_func(v_local)
                if minimize and new_val < best_val or new_val > best_val:
                    v_best.append((v_local, new_val, temp))
            elif np.random.uniform(0, 1) < np.exp(-delta / temp):
                v = v_local
        temp = temp - f_temp(temp)

    v_best.append((v_best[-1][0], v_best[-1][1], temp_target))
    print("FES: ", fes_counter)
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


def cooling_linear(temp):
    return temp / (1 + temp * 0.995)


def cooling_exp(temp):
    return temp - temp * 0.99163


def cooling_knapsack(temp):
    threshold = 0.975 + (1 - 0.975) * min((FES - 6000) / 12000, 0.65)
    return temp - temp * threshold


def cooling_adaptive(temp):
    return temp / (1 + temp * 0.989)


def deviation_adaptive(temp):
    if temp > 500:
        return 2.5
    if temp > 1:
        return 0.85
    return 0.25


def deviation_adaptive2(temp):
    if temp > 60:
        return 0.5
    if temp > 1:
        return 0.1
    return 0.005


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
                return -1
    return val


def generate_items(n=30):
    global KNAPSACK_ITEMS
    KNAPSACK_ITEMS = np.random.randint(1, 50, (n, 2))


def plot_step_rand(vals, title, xlabel, ylabel="Result", reverse=False, logarithmic=False):
    for i, lst in enumerate(vals):
        x = []
        y = []
        for tup in lst:
            x.append(tup[2])
            y.append(tup[1])
        plt.plot(x, y, label='List {}'.format(i + 1))

    plt.title(title)
    plt.xlabel(xlabel)
    if reverse:
        plt.gca().invert_xaxis()  # invert x-axis
    if logarithmic:
        plt.gca().set_yscale('log')
    plt.ylabel(ylabel)
    plt.show()


def plot_step_anneal(vals, title, xlabel, ylabel="Result", reverse=False, logarithmic_x=False, logarithmic_y=False):
    fig, ax = plt.subplots()

    for i, lst in enumerate(vals):
        x = []
        y = []
        for tup in lst:
            x.append(tup[2])
            y.append(tup[1])
        if logarithmic_x:
            threshold = 10
            above_threshold = np.array(x) > threshold
            below_threshold = np.array(x) <= threshold

            ax.plot(np.array(x)[above_threshold], np.array(y)[above_threshold], color=get_color(i))
            ax.plot(np.array(x)[below_threshold], np.array(y)[below_threshold], color=get_color(i))
            ax.set_xscale('log')
            if logarithmic_y:
                ax.set_yscale('log')

        else:
            ax.plot(x, y)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if reverse:
        ax.invert_xaxis()

    plt.show()


def plot_average_anneal(vals, title, temp_f, xlabel, ylabel="Result", reverse=False, logarithmic_x=False,
                        logarithmic_y=False):

    help_dictionary_vals = dict()
    help_dictionary_count = dict()
    average_values = []
    iteration_values = []

    temp = INIT_TEMP

    while temp >= TARGET_TEMP:
        iteration_values.append(temp)
        help_dictionary_vals[temp] = 0
        help_dictionary_count[temp] = 0
        temp = temp - temp_f(temp)

    for lst in vals:
        lst_temps = [t[2] for t in lst]
        last_index = -1
        for temp in iteration_values:
            if temp in lst_temps:
                last_index = lst_temps.index(temp)
                help_dictionary_vals[temp] += lst[last_index][1]
            else:
                help_dictionary_vals[temp] += lst[last_index][1]

    fig, ax = plt.subplots()

    for key in help_dictionary_vals.keys():
        help_dictionary_vals[key] /= len(vals)

    help_dictionary_vals = dict(sorted(help_dictionary_vals.items()))

    iteration_values = list(help_dictionary_vals.keys())
    average_values = list(help_dictionary_vals.values())

    if logarithmic_x:
        threshold = 100  # Adjust the threshold as needed
        above_threshold = np.array(iteration_values) > threshold
        below_threshold = np.array(iteration_values) <= threshold

        ax.plot(np.array(iteration_values)[above_threshold], np.array(average_values)[above_threshold],
                color=get_color(0))
        ax.plot(np.array(iteration_values)[below_threshold], np.array(average_values)[below_threshold],
                color=get_color(0))
        ax.set_xscale('log')
        if logarithmic_y:
            ax.set_yscale('log')

    else:
        ax.plot(iteration_values, average_values, label='Average')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if reverse:
        ax.invert_xaxis()

    plt.axhline(y=average_values[0], color='r', linestyle='--')
    ax.annotate(f'y = {round(average_values[0], 4)}', xy=(0.5, average_values[0]), xytext=(0, 20),
                textcoords='offset points', ha='center', color='r')
    plt.show()


def plot_average_rand(vals, bounds, increment, title, xlabel, ylabel="Result", reverse=False, logarithmic=False):
    average_values = []
    iteration_values = []
    for i in range(bounds[0], bounds[1], increment):
        iteration_values.append(i)
        x = 0
        for lst in vals:
            for tup in lst:
                if tup[2] > i:
                    x += tup[1]
                    break
        average_values.append(x / len(vals))

    plt.plot(iteration_values, average_values, label='Average')

    plt.title(title)
    plt.xlabel(xlabel)
    if reverse:
        plt.gca().invert_xaxis()  # invert x-axis
    if logarithmic:
        plt.gca().set_yscale('log')
    plt.ylabel(ylabel)
    plt.axhline(y=average_values[-1], color='r', linestyle='--')
    plt.annotate(f'y = {round(average_values[-1], 4)}', xy=(0.5, average_values[-1]), xytext=(0, 20),
                 textcoords='offset points', ha='center', color='r')
    plt.show()


def get_color(i):
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    return color_cycle[i % len(color_cycle)]


if __name__ == "__main__":

    methods_to_run = [
        # "dejong1",
        # "dejong2",
        "schwefel",
        # "knapsack"
    ]

    dejong_random = dict()
    dejong_annealing = dict()
    dejong2_random = dict()
    dejong2_annealing = dict()
    schwefel_random = dict()
    schwefel_annealing = dict()

    dejong1_stdev = lambda x: 0.01
    dejong2_stdev = deviation_adaptive2  # lambda x: 0.02
    schwefel_stdev = deviation_adaptive

    INIT_TEMP = FES / METROPOLIS_ITER

    for d in [5, 10]:
        dejong_random[d] = list()
        dejong_annealing[d] = list()
        dejong2_random[d] = list()
        dejong2_annealing[d] = list()

        for _ in range(30):
            vector1 = np.random.uniform(-5, 5, d)

            if "dejong1" in methods_to_run:
                dejong_random[d].append(
                    random_search(vector1, FES, dejong, (-5, 5))
                )
                dejong_annealing[d].append(
                    simulated_annealing(
                        vector1, METROPOLIS_ITER, INIT_TEMP, dejong, cooling_exp, TARGET_TEMP, dejong1_stdev, (-5, 5)
                    )
                )

            if "dejong2" in methods_to_run:
                dejong2_random[d].append(
                    random_search(vector1, FES, dejong2, (-5, 5))
                )
                dejong2_annealing[d].append(
                    simulated_annealing(
                        vector1, METROPOLIS_ITER, INIT_TEMP, dejong2, cooling_exp, TARGET_TEMP, dejong2_stdev,
                        (-5, 5)
                    )
                )

    if "schwefel" in methods_to_run:
        for d in [5, 10, 12]:
            schwefel_random[d] = list()
            schwefel_annealing[d] = list()

            for _ in range(30):
                vector2 = np.random.uniform(-500, 500, d)

                schwefel_random[d].append(
                    random_search(vector2, FES, schwefel, (-500, 500))
                )
                schwefel_annealing[d].append(
                    simulated_annealing(
                        vector2, METROPOLIS_ITER, INIT_TEMP, schwefel, cooling_exp, TARGET_TEMP, schwefel_stdev,
                        (-500, 500)
                    )
                )

    for d in [5, 10]:
        if "dejong1" in methods_to_run:
            plot_step_rand(dejong_random[d], "De Jong 1 - Random Search - D" + str(d), "Iteration", logarithmic=True)
            plot_step_anneal(dejong_annealing[d], "De Jong 1 - Simulated Annealing - D" + str(d), "Temperature",
                             logarithmic_x=True, reverse=True)
            plot_average_rand(dejong_random[d], (0, FES, 10), 100, "De Jong 1 - Average - Random Search - D" + str(d),
                              "Iteration", logarithmic=True)
            plot_average_anneal(dejong_annealing[d], "De Jong 1 - Average - Simulated Annealing - D" + str(d),
                                cooling_exp, "Temperature", reverse=True, logarithmic_x=True)

        if "dejong2" in methods_to_run:
            plot_step_rand(dejong2_random[d], "De Jong 2 - Random Search - D" + str(d), "Iteration", logarithmic=True)
            plot_step_anneal(dejong2_annealing[d], "De Jong 2 - Simulated Annealing - D" + str(d), "Temperature",
                             reverse=True, logarithmic_x=True, logarithmic_y=True)
            plot_average_rand(dejong2_random[d], (0, FES, 10), 100, "De Jong 2 - Average - Random Search - D" + str(d),
                              "Iteration", "Iteration", logarithmic=True)
            plot_average_anneal(dejong2_annealing[d], "De Jong 2 - Average - Simulated Annealing - D" + str(d),
                                cooling_exp, "Temperature", reverse=True, logarithmic_x=True, logarithmic_y=True)

        if "schwefel" in methods_to_run:
            plot_step_rand(schwefel_random[d], "Schwefel - Random Search - D" + str(d), "Iteration")
            plot_step_anneal(schwefel_annealing[d], "Schwefel - Simulated Annealing - D" + str(d), "Temperature",
                             reverse=True)
            plot_average_rand(schwefel_random[d], (0, FES, 10), 100,
                              "Schwefel - Average - Random Search - D" + str(d),
                              "Iteration")
            plot_average_anneal(schwefel_annealing[d], "Schwefel - Average - Simulated Annealing - D" + str(d),
                                cooling_exp, "Temperature", reverse=True)

    knapsack_heuristic = dict()
    knapsack_random = dict()

    if "knapsack" in methods_to_run:
        for d in [15, 30, 50]:
            knapsack_heuristic[d] = list()
            knapsack_random[d] = list()
            FES = 400 * d
            INIT_TEMP = FES / METROPOLIS_ITER

            for _ in range(10):
                generate_items(d)
                knapsack_heuristic[d].append(
                    simulated_annealing(
                        [0] * d,
                        METROPOLIS_ITER,
                        INIT_TEMP,
                        knapsack,
                        cooling_knapsack,
                        TARGET_TEMP,
                        dejong1_stdev,
                        (0, 1),
                        False,
                        "disc",
                    )
                )
                knapsack_random[d].append(
                    random_search([0] * d, FES, knapsack, (0, 1), False, "disc")
                )

        for d in [15, 30, 50]:
            INIT_TEMP = 40 * d
            FES = 400 * d
            plot_step_anneal(knapsack_heuristic[d], "Knapsack - Simulated Annealing - D" + str(d), "Temperature",
                             reverse=True)
            plot_step_rand(knapsack_random[d], "Knapsack - Random Search - D" + str(d), "Iteration")
            plot_average_anneal(knapsack_heuristic[d], "Knapsack - Average - Simulated Annealing - D" + str(d),
                                cooling_knapsack, "Temperature", reverse=True)
            plot_average_rand(knapsack_random[d], (0, 400 * d, 10), d, "Knapsack - Average - Random Search - D" + str(d),
                              "Iteration")

    print("Konec")
    quit()
