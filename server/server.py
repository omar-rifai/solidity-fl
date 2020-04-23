#!/Users/omar_rifai/workspace/truffle/venv/bin/python

from flask import Flask, render_template, jsonify
import time
from flask import Flask
import controler
import sys
import network as nn
app = Flask(__name__)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/federation')
def federationAPI():

    s = 123
    n_global_updates = 1
    n_local_updates = 10
    testing_data, edge_nets, edge_data = controler.setup_simulation(s)
    results_scenario = [[] for e in range(len(edge_nets))]
    
    for j in range(n_global_updates):
        
        results_scenario = controler.run_stage(\
            testing_data, edge_nets, edge_data,\
            results_scenario, n_local_updates,s)
        
        agg_weights, agg_biases = controler.run_federation(edge_nets, edge_data)
    
    #edge_nets = run_broadcast(agg_weights, agg_biases, edge_nets)
    print(sys.path)
    return{'response' : [nn.toList(e) for e in edge_nets]}