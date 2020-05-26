var Federation = artifacts.require("../contracts/Federation.sol");

module.exports = function(deployer) {
  deployer.deploy(Federation, { gas: 90000000 });
};
