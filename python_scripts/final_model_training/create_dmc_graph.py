from rlcard.games.cego.utility.eval import create_cego_dmc_graph

if __name__ == '__main__':
    model_path = 'final_models/dmc_cego'
    create_cego_dmc_graph(model_path)
