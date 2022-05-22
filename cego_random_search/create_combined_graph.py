import json
import os
import csv
import matplotlib.pyplot as plt

path_to_models= 'random_search_results/dqn'

def create_combined_graph(path_to_models, data_per_graph= 10):
    model_dirs= [x[0] for x in os.walk(path_to_models)]

    ys = []
    xs = []

    i= 0

    fig, ax = plt.subplots()
    for model_dir in model_dirs:
        if not os.path.exists(model_dir+ '/performance.csv'):
            continue

        i+= 1
        ys.append([])
        xs.append([])

        file = open(model_dir+ '/performance.csv')

        csvreader = csv.DictReader(file)
        for row in csvreader:
            ys[(i-1)%data_per_graph].append(int(row['timestep']))
            xs[(i-1)%data_per_graph].append(float(row['reward']))

        if i%data_per_graph== 0:
            fig, ax = plt.subplots()
        ax.set(xlabel='timestep', ylabel='reward')
        for idx in range(len(ys)):
            ax.plot(ys[idx], xs[idx], label= "model_"+str(idx+ i-5), linewidth=0.5)
        ax.legend()
        ax.grid()

        if i%data_per_graph== 0:
            fig.savefig(path_to_models + '/fig'+ str(i//data_per_graph)+ '.png', dpi=200)
            ys = []
            xs = []


if __name__ == '__main__':
    create_combined_graph(path_to_models, 5)
