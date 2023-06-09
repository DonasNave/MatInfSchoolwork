import numpy as np
import math
import matplotlib.pyplot as plt

KNAPSACK_ITEMS = None

FES = 20000
METROPOLIS_ITER = 20
TARGET_TEMP = 0.0001
INIT_TEMP = FES/METROPOLIS_ITER


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
        stdev=None,
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
    v_best.append((v, objective_func(v), temp, fes_counter))
    while temp > temp_target:
        for i in range(n_mpolis):
            fes_counter += 1
            stdev_val = None
            if stdev is not None:
                stdev_val = stdev(temp)
            v_local = get_neighbours(space, v, bounds, stdev_val)
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
                    v_best.append((v_local, new_val, temp, fes_counter))
            elif np.random.uniform(0, 1) < np.exp(-delta / temp):
                v = v_local
        temp = temp - f_temp(temp)

    v_best.append((v_best[-1][0], v_best[-1][1], temp_target, fes_counter))
    print(fes_counter)
    return v_best


def get_neighbours(space, v, bounds, stdev=None):
    if space == "spoj":
        if stdev is not None:
            new_v = np.random.normal(v, stdev, v.shape)
            np.clip(new_v, bounds[0], bounds[1])
            return new_v

        # Set the bounds and range percentage
        space_min = bounds[0]
        space_max = bounds[1]
        range_percentage = 0.1

        # Calculate the desired range
        range_size = (space_max - space_min) * range_percentage
        range_min = (space_max + space_min) / 2 - range_size / 2
        range_max = (space_max + space_min) / 2 + range_size / 2

        # Generate random values from a normal distribution
        random_values = np.random.normal(loc=0, scale=range_size / 6, size=len(v))

        # Clip the values to ensure they are within the desired range
        random_values = np.clip(random_values, range_min, range_max)

        # Add the random values to the original vector
        return v + random_values
    elif space == "disc":
        v_local = np.copy(v)
        for i in range(len(v)):
            if np.random.randint(0, len(v)) == len(v) - 1:
                v_local[i] = (v_local[i] + 1) % 2
        return v_local


def cooling_linear(temp):
    return temp / (1 + temp * 0.995)


def cooling_exp(temp):
    return temp - temp * 0.984


def cooling_knapsack(temp):
    return temp - temp * 0.9735


def cooling_adaptive(temp):
    return temp / (1 + temp * 0.989)


def deviation_adaptive(temp):
    if temp > 200:
        return 50
    if temp > 1:
        return 10
    return 5.5


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


def plot_step_rand(vals, title, xlabel, ylabel="Score", reverse=False, logarithmic=False):
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


def plot_combined(vals, title, xlabel, ylabel, logarithmic=False):
    for axis in vals:
        plt.plot(axis[0], axis[1], label=axis[2])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if logarithmic:
        plt.gca().set_yscale('log')
    plt.legend()
    plt.show()


def plot_step_anneal(vals, title, temp_f, xlabel, ylabel="Score", reverse=False, logarithmic_x=False,
                     logarithmic_y=False, maximaze=False):
    fig, ax = plt.subplots()

    iteration_values = []

    temp = INIT_TEMP

    while temp >= TARGET_TEMP:
        iteration_values.append(temp)
        temp = temp - temp_f(temp)

    for lst in vals:
        sub_values = []
        lst_temps = [t[2] for t in lst]
        last_index = 0
        for temp in iteration_values:
            if temp in lst_temps:
                new_index = len(lst_temps) - 1 - lst_temps[::-1].index(temp)  # index of last value at temp
                if not maximaze and lst[last_index][1] > lst[new_index][1]:
                    last_index = new_index
                elif maximaze and lst[last_index][1] < lst[new_index][1]:
                    last_index = new_index
            sub_values.append(lst[last_index][1])
        ax.plot(iteration_values, sub_values)

    if logarithmic_y:
        ax.set_yscale('log')

    if logarithmic_x:
        ax.set_xscale('log')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if reverse:
        ax.invert_xaxis()

    plt.show()


def plot_average_anneal(vals, title, temp_f, xlabel, ylabel="Score", reverse=False, logarithmic_x=False,
                        logarithmic_y=False, maximaze=False):

    help_dictionary_vals = dict()
    help_dictionary_count = dict()
    help_dictionary_fes = dict()
    iteration_values = []

    temp = INIT_TEMP

    while temp >= TARGET_TEMP:
        iteration_values.append(temp)
        help_dictionary_vals[temp] = 0
        help_dictionary_fes[temp] = 0
        temp = temp - temp_f(temp)

    iteration_values.append(TARGET_TEMP)
    help_dictionary_vals[TARGET_TEMP] = 0
    help_dictionary_fes[TARGET_TEMP] = 0

    for lst in vals:
        lst_temps = [t[2] for t in lst]
        last_index = 0
        new_index = 0
        for temp in iteration_values:
            # change index if temp is in list and if the value at that index is better than the current one
            if temp in lst_temps:
                new_index = len(lst_temps) - 1 - lst_temps[::-1].index(temp)  # index of last value at temp
                if not maximaze and lst[last_index][1] > lst[new_index][1]:
                    last_index = new_index
                elif maximaze and lst[last_index][1] < lst[new_index][1]:
                    last_index = new_index
            help_dictionary_vals[temp] += lst[last_index][1]
            help_dictionary_fes[temp] += lst[new_index][3]

    fig, ax = plt.subplots()

    for key in help_dictionary_vals.keys():
        help_dictionary_vals[key] /= len(vals)
        help_dictionary_fes[key] /= len(vals)

    help_dictionary_vals = dict(sorted(help_dictionary_vals.items()))

    iteration_values = list(help_dictionary_vals.keys())
    average_values = list(help_dictionary_vals.values())
    fes_values = list(help_dictionary_fes.values())

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

    average_values.reverse()
    return fes_values, average_values


def plot_average_rand(vals, bounds, increment, title, xlabel, ylabel="Score", reverse=False, logarithmic=False):
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
    return iteration_values, average_values


def get_color(i):
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    return color_cycle[i % len(color_cycle)]


def print_stats(vals, title):
    data = [t[-1][1] for t in vals]

    minimum = np.min(data)
    maximum = np.max(data)
    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)

    print("\n" + title)
    print(f"Minimum: {minimum}")
    print(f"Maximum: {maximum}")
    print(f"Mean: {mean}")
    print(f"Median: {median}")
    print(f"Standard Deviation: {std_dev}\n")


if __name__ == "__main__":

    methods_to_run = [
        # "dejong1",
        # "dejong2",
        # "schwefel",
        "knapsack"
    ]

    dejong_random = dict()
    dejong_annealing = dict()
    dejong2_random = dict()
    dejong2_annealing = dict()
    schwefel_random = dict()
    schwefel_annealing = dict()

    dejong1_stdev = lambda x: 0.01
    dejong2_stdev = deviation_adaptive2
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
                        vector1, METROPOLIS_ITER, INIT_TEMP, dejong2, cooling_exp, TARGET_TEMP, dejong2_stdev, (-5, 5)
                    )
                )

    if "schwefel" in methods_to_run:
        for d in [5, 10]:
            schwefel_random[d] = list()
            schwefel_annealing[d] = list()

            for _ in range(30):
                vector2 = np.random.uniform(-500, 500, d)

                schwefel_random[d].append(
                    random_search(vector2, FES, schwefel, (-500, 500))
                )
                schwefel_annealing[d].append(
                    simulated_annealing(
                        vector2, METROPOLIS_ITER, INIT_TEMP, schwefel, cooling_linear, TARGET_TEMP, None,
                        (-500, 500)
                    )
                )

    for d in [5, 10]:
        if "dejong1" in methods_to_run:
            print_stats(dejong_random[d], "De Jong 1 - Stats - Random Search - D" + str(d))
            print_stats(dejong_annealing[d], "De Jong 1 - Stats - Simulated Annealing - D" + str(d))

            plot_step_rand(dejong_random[d], "De Jong 1 - Random Search - D" + str(d), "Iteration", logarithmic=True)
            plot_step_anneal(dejong_annealing[d], "De Jong 1 - Simulated Annealing - D" + str(d), cooling_exp,
                             "Temperature", reverse=True, logarithmic_x=True)

            avg_rand_iter, avg_rand_vals = plot_average_rand(dejong_random[d], (0, FES, 10), 100,
                             "De Jong 1 - Average - Random Search - D" + str(d),
                              "Iteration", logarithmic=True)
            avg_anneal_iter, avg_anneal_vals = plot_average_anneal(dejong_annealing[d],
                               "De Jong 1 - Average - Simulated Annealing - D" + str(d),
                                cooling_exp, "Temperature", reverse=True, logarithmic_x=True)

            avg_comb = [(avg_rand_iter, avg_rand_vals, "Random Search - avg"),
                        (avg_anneal_iter, avg_anneal_vals, "Simulated Annealing - avg")]

            plot_combined(avg_comb, "De Jong 1 - Combined - D" + str(d), "FES", "Score")

        if "dejong2" in methods_to_run:
            print_stats(dejong2_random[d], "De Jong 2 - Stats - Random Search - D" + str(d))
            print_stats(dejong2_annealing[d], "De Jong 2 - Stats - Simulated Annealing - D" + str(d))

            plot_step_rand(dejong2_random[d], "De Jong 2 - Random Search - D" + str(d), "Iteration", logarithmic=True)
            plot_step_anneal(dejong2_annealing[d], "De Jong 2 - Simulated Annealing - D" + str(d), cooling_exp,
                             "Temperature",
                             reverse=True, logarithmic_y=True, logarithmic_x=True)

            avg_rand_iter, avg_rand_vals = plot_average_rand(dejong2_random[d], (0, FES, 10), 100,
                                                             "De Jong 2 - Average - Random Search - D" + str(d),
                                                             "Iteration", "Score", logarithmic=True)
            avg_anneal_iter, avg_anneal_vals = plot_average_anneal(dejong2_annealing[d],
                                                                   "De Jong 2 - Average - Simulated Annealing - D"
                                                                   + str(d), cooling_exp, "Temperature", reverse=True,
                                                                   logarithmic_x=True, logarithmic_y=True)

            avg_comb = [(avg_rand_iter, avg_rand_vals, "Random Search - avg"),
                        (avg_anneal_iter, avg_anneal_vals, "Simulated Annealing - avg")]

            plot_combined(avg_comb, "De Jong 2 - Combined - D" + str(d), "FES", "Score", True)

        if "schwefel" in methods_to_run:
            print_stats(schwefel_random[d], "Schwefel - Stats - Random Search - D" + str(d))
            print_stats(schwefel_annealing[d], "Schwefel - Stats - Simulated Annealing - D" + str(d))

            plot_step_rand(schwefel_random[d], "Schwefel - Random Search - D" + str(d), "Iteration")
            plot_step_anneal(schwefel_annealing[d], "Schwefel - Simulated Annealing - D" + str(d), cooling_linear,
                             "Temperature",
                             reverse=True)

            avg_rand_iter, avg_rand_vals = plot_average_rand(schwefel_random[d], (0, FES, 10), 100,
                                                             "Schwefel - Average - Random Search - D" + str(d),
                                                             "Iteration")
            avg_anneal_iter, avg_anneal_vals = plot_average_anneal(schwefel_annealing[d],
                                                                   "Schwefel - Average - Simulated Annealing - D"
                                                                   + str(d), cooling_linear, "Temperature", reverse=True)

            avg_comb = [(avg_rand_iter, avg_rand_vals, "Random Search - avg"),
                        (avg_anneal_iter, avg_anneal_vals, "Simulated Annealing - avg")]

            plot_combined(avg_comb, "Schwefel - Combined - D" + str(d), "FES", "Score")

    knapsack_heuristic = dict()
    knapsack_random = dict()

    if "knapsack" in methods_to_run:
        for d in [15, 30, 50]:
            knapsack_heuristic[d] = list()
            knapsack_random[d] = list()
            FES = 400 * d
            INIT_TEMP = 1200
            METROPOLIS_ITER = int(2 * d / 3)
            generate_items(d)

            for _ in range(10):
                knapsack_heuristic[d].append(
                    simulated_annealing(
                        [0] * d,
                        METROPOLIS_ITER,
                        INIT_TEMP,
                        knapsack,
                        cooling_knapsack,
                        TARGET_TEMP,
                        None,
                        (0, 1),
                        False,
                        "disc",
                    )
                )
                knapsack_random[d].append(
                    random_search([0] * d, FES, knapsack, (0, 1), False, "disc")
                )

        for d in [15, 30, 50]:
            FES = 400 * d
            print_stats(knapsack_random[d], "Knapsack - Stats - Random Search - D" + str(d))
            print_stats(knapsack_heuristic[d], "Knapsack - Stats - Simulated Annealing - D" + str(d))

            plot_step_rand(knapsack_random[d], "Knapsack - Random Search - D" + str(d), "Iteration")
            plot_step_anneal(knapsack_heuristic[d], "Knapsack - Simulated Annealing - D" + str(d), cooling_knapsack,
                             "Temperature", reverse=True, maximaze=True)

            avg_rand_iter, avg_rand_vals = plot_average_rand(knapsack_random[d], (0, 400 * d, 10), d,
                                                             "Knapsack - Average - Random Search - D" + str(d),
                                                             "Iteration")
            avg_anneal_iter, avg_anneal_vals = plot_average_anneal(knapsack_heuristic[d],
                                                                   "Knapsack - Average - Simulated Annealing - D"
                                                                   + str(d), cooling_knapsack, "Temperature",
                                                                   reverse=True, maximaze=True)

            avg_comb = [(avg_rand_iter, avg_rand_vals, "Random Search - avg"),
                        (avg_anneal_iter, avg_anneal_vals, "Simulated Annealing - avg")]

            plot_combined(avg_comb, "Knapsack - Combined - D" + str(d), "FES", "Score")
    print("Konec")
    quit()
