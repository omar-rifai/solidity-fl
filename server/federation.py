import numpy as np
import math
import copy


def agg_params(params, edge_weights):
    rnets = range(len(params))
    rlayers = range(len(params[0]))
    new_params = []

    for l in rlayers:
        new_layer = []
        rsamples = range(len(params[0][l]))

        for s in rsamples:
            temp_list = [params[i][l][s] for i in rnets]
            new_sample = [np.average(i, weights=edge_weights)
                          for i in list(zip(*temp_list))]
            new_layer.append(list(new_sample))
        new_params.append(list(new_layer))

    return new_params


def local_updates(net_lst, data_lst, n_local_updates, testing_data, rs):
    batchsize = 10
    eta = 0.1
    acc_logs = {}
    # initialize empty logs lists
    for i in range(len(net_lst)):
        acc_logs[i] = []

    # run stochastic gradient descent and save results
    for i in range(len(net_lst)):
        accuracy_current_round = net_lst[i].SGD(
            data_lst[i], n_local_updates, batchsize, eta, testing_data, rs)
        for t in range(len(accuracy_current_round)):
            acc_logs[i].append(accuracy_current_round[t])
    return acc_logs


def broadcast_updates(main_params, edge_nets):

    for i in range(len(edge_nets)):
        edge_nets[i].weights = main_params[0]
        edge_nets[i].biases = main_params[1]
    return True


def split_dataset(training_data, n_edges, rs):

    n_data = len(training_data)
    edge_data = []
    edge_share = math.floor(n_data/n_edges)
    epsilon = int(edge_share / 5)
    local_data = copy.deepcopy(training_data)

    for i in range(n_edges):
        random_share = np.random.randint(
            edge_share-epsilon, edge_share+epsilon)
        temp_data = np.random.permutation(local_data)[:random_share]
        local_data = local_data[random_share:]
        edge_data.append(temp_data)

    return edge_data


def run_local(testing_data, edge_nets, edge_data, n_local_updates, rs):

    n_edges = len(edge_nets)
    accuracy_global = [[] for i in range(len(edge_nets))]
    accuracy_current = local_updates(edge_nets, edge_data,
                                     n_local_updates, testing_data,
                                     rs)
    for i in range(n_edges):

        for t in range(len(accuracy_current[i])):
            accuracy_global[i].append(accuracy_current[i][t])
    return accuracy_global


def federate_edges(edge_params, edge_cardinalities):

    agg_weights = agg_params(edge_params[0], edge_cardinalities)
    agg_biases = agg_params(edge_params[1], edge_cardinalities)

    return agg_weights, agg_biases
