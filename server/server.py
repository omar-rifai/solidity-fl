#!/Users/omar_rifai/workspace/truffle/venv/bin/python

from flask import Flask, render_template, jsonify
import time
from flask import Flask
import controler
import sys
import network as nn
from flask import request
from pymongo import MongoClient
import numpy as np
import data_processing as dp
app = Flask(__name__)


app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")  # host uri
db = client.nnetworks  # Select the database


def call_init():
    s = 123
    n_global_updates = 1
    n_local_updates = 10
    testing_data, edge_nets, edge_data = controler.setup_simulation(s)
    results_scenario = [[] for e in range(len(edge_nets))]
    db.params.update({'s': s}, {'s': s, 'n_global_updates': n_global_updates,
                                'n_local_updates': n_local_updates}, upsert=True)
    db.networks.update({'s': s},
                       {'s': s, 'edge_nets': [controler.write_network(e) for e in edge_nets], 'edge_data': [dp.toList(edge_data)]}, upsert=True)
    db.data.update({'s': s},
                   {'s': s, 'testing_data': dp.toList(testing_data)}, upsert=True)


@app.route('/init')
def initAPI():
    call_init()
    return {'time': time.time()}


@app.route('/run_stage')
def runStageAPI():
    s = 123
    db_params = db.params.find_one({"s": s})
    db_edges = db.networks.find_one({"s": s})
    db_data = db.data.find_one({'s': s})

    n_global_updates = db_params["n_global_updates"]
    n_local_updates = db_param["n_local_updates"]
    edges_nets = db_edges["edge_nets"]
    testing_data = db_data

    #testing_data, edge_nets, edge_data = controler.setup_simulation(s)
    results_scenario = [[] for e in range(len(edge_nets))]

    results_scenario = controler.run_stage(
        testing_data, edge_nets, edge_data,
        results_scenario, n_local_updates, s)

    db.results.update({'s': s},
                      {'s': s, 'results_scenario': results_scenario}, upsert=True)

    list_nets = [controler.write_network(e) for e in edge_nets]
    net_weights = [e["weights"] for e in list_nets]
    net_biases = [e["biases"] for e in list_nets]

    return{'weights': net_weights,
           'biases': net_biases}


@app.route('/post_params', methods=['GET', 'POST'])
def submitParamsAPI():
    s = 123
    db_networks = db.networks.find_one({"s": s})
    edge_nets = db_networks["edge_nets"]
    for e in range(len(edge_nets)):
        edge_nets[e]["weights"] = request.args["weights"]
        edge_nets[e]["biases"] = request.args["biases"]

    return {'response': True}


@app.route('/get_results', methods=['GET'])
def getResultsAPI():
    db_results = db.results.find_one()
    results_scenario = db_results['results_scenario']

    n_samples = len(results_scenario[0])
    names = [str(i) for i in range(n_samples)]
    vals = results_scenario[0]
    results_list = []

    for i in range(n_samples):
        results_list.append({'name': names[i], 'uv': vals[i]})

    return {'results': results_list}


@app.route('/calc_accuracy', methods=['POST', 'GET'])
def calcAccuracyAPI():
    return True
