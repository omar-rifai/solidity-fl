var Federation = artifacts.require("../contracts/Federation.sol");

module.exports = function(deployer) {
  deployer.deploy(Federation, { gas: 50000000 });
};
