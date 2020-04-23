pragma solidity >=0.5.16;
pragma experimental ABIEncoderV2;


contract Federation {
    uint256 total;
    uint256 counter;
    uint256[][][][] edges_params; //data structure to hold the edges' parameters
    uint256[][][] server_params; // data structure to hold the global parameters
    uint32 public constant toFloat = 1E9;
    address[] edges;

    mapping(address => bool) public participated;
    mapping(address => bool) public edges_mapping;

    /* Input: an array of edges params for one layer
   Output: the new layer params for the server which is the aggregation of the edges' params
   Remark: The output is to be broadcasted back to the edges after all layers have been processed */

    function averageLayer() internal returns (uint256[][][] memory) {
        uint256 n_clients = edges_params.length;
        uint256 n_layers = edges_params[0].length;
        uint256[][][] memory newParams = new uint256[][][](n_layers);

        for (uint256 i = 0; i < n_layers; i++) {
            uint256 n_neurons = edges_params[0][i].length;
            uint256 n_connections = edges_params[0][i][0].length;

            newParams[i] = new uint256[][](n_neurons);

            for (uint256 j = 0; j < n_neurons; j++) {
                newParams[i][j] = new uint256[](n_connections);

                for (uint256 k = 0; k < n_connections; k++) {
                    resetCounters();

                    for (uint256 z = 0; z < n_clients; z++) {
                        calcAverage(edges_params[z][i][j][k]);
                    }

                    uint256 temp_average = getAverage();
                    newParams[i][j][k] = temp_average;
                    emit displayParam(temp_average);
                }
            }
        }
        return newParams;
    }

    /* Input: an edge parameters' array (for a given layer)
       Output: parameters' array aggregated to the global parameters array
       Remark: helper function to prepare for the aggregation */

    function store_params(uint256[][][] memory _layer_params)
        public
        returns (uint256)
    {
        require(
            participated[msg.sender] == false,
            "Sender already stored parameters."
        );

        if (edges_mapping[msg.sender] == false) {
            edges.push(msg.sender);
            edges_mapping[msg.sender] = true;
        }

        edges_params.push(_layer_params);
        participated[msg.sender] = true;

        return 1;
    }

    function run_agg() public returns (uint256[][][] memory) {
        server_params = averageLayer();
        clearEdgesArray();
        resetAccounts();
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

    function clearEdgesArray() internal returns (uint256) {
        //for (uint i = 0; i <= edges_params.length; i++) {
        //  edges_params.pop();
        //}
        delete edges_params;
        return edges_params.length;
    }

    function resetAccounts() internal returns (bool) {
        for (uint256 i = 0; i < edges.length; i++) {
            participated[edges[i]] = false;
        }
        return true;
    }

    function read_edges_params() public view returns (uint256[][][][] memory) {
        return edges_params;
    }

    function read_params() public view returns (uint256[][][] memory) {
        return server_params;
    }

    // Event for debugging purposes

    event displayParam(uint256 _param);

    function displayAccount() public view returns (address) {
        return msg.sender;
    }
}
