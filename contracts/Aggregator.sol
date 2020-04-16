pragma solidity ^0.5.16;
pragma experimental ABIEncoderV2;


contract Aggregator {
    uint256 total;
    uint256 counter;
    uint256[][][] edges_params; //data structure to hold the edges' parameters
    uint256[][] server_params; // data structure to hold the global parameters
    uint32 public constant toFloat = 1E9;

    /* Input: an array of edges params for one layer
   Output: the new layer params for the server which is the aggregation of the edges' params
   Remark: The output is to be broadcasted back to the edges after all layers have been processed */

    function averageLayer(uint256[][][] memory _layer_params)
        internal
        returns (uint256[][] memory)
    {
        uint256 n_clients = _layer_params.length;
        uint256 n_neurons = _layer_params[0].length;
        uint256 n_connections = _layer_params[0][0].length;
        uint256[][] memory newLayer = new uint256[][](n_neurons);

        for (uint256 i = 0; i < n_neurons; i++) {
            newLayer[i] = new uint256[](n_connections);

            for (uint256 j = 0; j < n_connections; j++) {
                resetCounters();

                for (uint256 k = 0; k < n_clients; k++) {
                    calcAverage(_layer_params[k][i][j]);
                }
                uint256 temp_average = getAverage();
                newLayer[i][j] = temp_average;
                emit displayParam(temp_average);
            }
        }
        return newLayer;
    }

    /* Input: an edge parameters' array (for a given layer)
       Output: parameters' array aggregated to the global parameters array
       Remark: helper function to prepare for the aggregation */

    function store_params(uint256[][] memory _layer_params)
        public
        returns (uint256)
    {
        // TODO: require that the address from which the parameter is read has not yet
        // called the function  in this round
        edges_params.push(_layer_params);
        return 1;
    }

    function getBalance() public view returns (uint256) {
        return 123;
    }

    function run_agg() public returns (uint256) {
        server_params = averageLayer(edges_params);
        return 1;
    }

    function read_params() public view returns (uint256[][] memory) {
        return server_params;
    }

    function calcAverage(uint256 _newValue) internal {
        total += _newValue;
        counter++;
    }

    function getAverage() internal view returns (uint256) {
        return ((total * toFloat) / counter);
    }

    function resetCounters() internal {
        counter = 0;
        total = 0;
    }

    // Event for debugging purposes

    event displayParam(uint256 _param);
}
