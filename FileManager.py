import pickle

with open('Data/strategy', 'rb') as strategy_file:
    strat = pickle.load(strategy_file)

strat[0].next()