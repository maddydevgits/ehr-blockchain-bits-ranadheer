const ehr = artifacts.require("ehr");

module.exports = function (deployer) {
  deployer.deploy(ehr);
};
