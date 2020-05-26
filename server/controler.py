from data_processing import *
from federation import *
import numpy as np
import network as nn
import matplotlib.pyplot as plt
import data_processing as dp


n_simulations = 1
n_global_updates = 1
n_local_updates = 10
n_edges = 10

federate = 0

n_inputs_network = 8
n_outputs_network = 1
hidden_layers_sizes = [32, 16]
accuracy_scenarios = []


def init_networks(n_input_network, n_output_network, hidden_layers_sizes, n_edges):
    # initialize networks
    edge_nets = []
    for i in range(n_edges):
        edge_nets.append(nn.Network(
            [n_inputs_network, *hidden_layers_sizes, n_outputs_network]))
    return edge_nets


def get_data(rs, n_edges):
    edge_data = []
    training_data, testing_data, _, _, _, _ = init_dataset(rs=rs)
    edge_data = split_dataset(training_data, n_edges, rs)

    return training_data, testing_data, edge_data


def update_scenario_results(n_edges, n_local_updates, results_scenario, results_temp):
    for e in range(n_edges):
        for t in range(n_local_updates):
            results_scenario[e].append(results_temp[e][t])
    return results_scenario


def setup_simulation(s):
    np.random.seed(s)
    training_data,\
        testing_data,\
        edge_data = get_data(s, n_edges)

    edge_nets = init_networks(n_inputs_network, n_outputs_network,
                              hidden_layers_sizes, n_edges)
    return testing_data, edge_nets, edge_data


def run_stage(testing_data, edge_nets, edge_data,
              results_scenario, n_local_updates, s):

    results_temp = run_local(testing_data, edge_nets,
                             edge_data, n_local_updates, s)

    results_scenario = update_scenario_results(
        n_edges, n_local_updates, results_scenario, results_temp)
    return results_scenario


def run_federation(edge_nets, edge_data):
    edge_cardinalities = [len(i) for i in edge_data]
    agg_weights, agg_biases = federate_edges([[a.weights for a in edge_nets],
                                              [a.biases for a in edge_nets]],
                                             edge_cardinalities)
    return agg_weights, agg_biases


def run_broadcast(agg_weights, agg_biases, edge_nets):
    broadcast_updates([agg_weights, agg_biases], edge_nets)
    return edge_nets


def write_network(net):
    json_net = {}
    json_net["weights"] = [w.tolist() for w in net.weights]
    json_net["biases"] = [b.tolist() for b in net.biases]
    json_net["num_layers"] = net.num_layers
    json_net["sizes"] = net.sizes
    return json_net


def read_network(net_dict):
    net_weights = net_dict["weights"]
    net_biases = net_dict["biases"]
    n_inputs_network = net_dict["sizes"][0]
    n_outputs_network = net_dict["sizes"][-1]
    hidden_layers_sizes = [net_dict["sizes"][i]
                           for i in range(1, net_dict["num_layers"]-1)]
    ret = nn.Network(
        [n_inputs_network, *hidden_layers_sizes, n_outputs_network])
    ret.weights = dp.toNpArray(net_weights)
    ret.biases = dp.toNpArray(net_biases)
    return ret


def main():
    return "success"


if __name__ == "__main__":
    main()
