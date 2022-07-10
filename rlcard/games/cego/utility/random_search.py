import random


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
