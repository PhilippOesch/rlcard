import random
import os
from rlcard.games.cego.utility.training import save_args_params

def args_to_str(args):
    res = ''

    for val in args:
        res += '{}_{}_'.format(val, args[val])

    return res


def get_random_search_args(args) -> dict:
    res = {}

    for val in args:
        res[val] = random.choice(args[val])

    return res

def randomSearch(train_func, args: dict, random_search_folder: str, random_search_iterations: int):
    set_of_searches = init_search_set(random_search_folder)

    for i in range(len(set_of_searches), random_search_iterations):
        training_args = get_random_search_args(args)
        args_as_string = args_to_str(training_args)

        # rerole as long as args have already been trained
        while args_as_string in set_of_searches:
            training_args = get_random_search_args(args)
            args_as_string = args_to_str(training_args)

        set_of_searches.add(args_as_string)
        training_args["log_dir"] = random_search_folder + "/model_" + str(i)
        save_args_params(training_args)
        train_func(**training_args)
        save_search_set(random_search_folder, args_as_string)


def init_search_set(random_search_folder):
    res = set()
    if os.path.exists(random_search_folder + "/search_set.txt"):
        with open(random_search_folder + "/search_set.txt", "r") as f:
            search_set = set(f.read().splitlines())

            for val in search_set:
                res.add(val)

    return res


def save_search_set(random_search_folder, args_string):
    if not os.path.exists(random_search_folder + "/search_set.txt"):
        open(random_search_folder + "/search_set.txt", 'a').close()

    with open(random_search_folder + "/search_set.txt", 'a') as f:
        f.write(args_string + "\n")