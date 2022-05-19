import os
import csv
import matplotlib.pyplot as plt

def save_args_params(args):
    if not os.path.exists(args["log_dir"]):
        os.makedirs(args["log_dir"])

    with open(args["log_dir"] + 'model_params.txt', 'w') as f:
        for key, value in args.items():
            f.write("{}: {}\n".format(key, value))

def create_cego_dmc_graph(model_path):
    file = open(model_path + '/dmc/logs.csv')

    csvreader= csv.DictReader(file)

    y = []
    x_cego = []
    x_other = []
    tick = 0

    for row in csvreader:
        if isfloat(row['mean_episode_return_1']):
            x_cego.append(float(row['mean_episode_return_0']))
            y.append(tick)
            tick += 1
        if isfloat(row['mean_episode_return_1']):
            x_other.append(float(row['mean_episode_return_1']))

    fig, ax = plt.subplots()
    ax.plot(y, x_cego, label='Cego Player')
    ax.plot(y, x_other, label='Other Players')
    ax.set(xlabel='Tick', ylabel='reward')
    ax.legend()
    ax.grid()

    fig.savefig(model_path+ '/fig.png')

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

    