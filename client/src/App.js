import React, { Component } from "react";

import Federation from "./contracts/Federation.json";
import getWeb3 from "./getWeb3";
import ContractField from "./ContractField";
import { Grid, GridList, Typography } from "@material-ui/core";
import "./App.css";
import Dropzone from "react-dropzone";

class App extends Component {
  state = {
    storageValue: 0,
    web3: null,
    accounts: null,
    contract: null,
    currentTime: 0
  };
  onDrop = acceptedFiles => {
    console.log(acceptedFiles);
  };
  componentDidMount = async () => {
    try {
      // Get network provider and web3 instance.
      const web3 = await getWeb3();
      //web3.setProvider(provider);

      // Use web3 to get the user's accounts.
      const accounts = await web3.eth.getAccounts();
      console.log("my accounts:", accounts);
      // Get the contract instance.
      const networkId = await web3.eth.net.getId();
      const deployedNetwork = Federation.networks[networkId];
      const instance = await new web3.eth.Contract(
        Federation.abi,
        deployedNetwork && deployedNetwork.address
      );

      // Set web3, accounts, and contract to the state, and then proceed with an
      // example of interacting with the contract's methods.
      this.setState({ web3, accounts, contract: instance }, this.runExample);
    } catch (error) {
      // Catch any errors for any of the above operations.
      alert(
        `Failed to load web3, accounts, or contract. Check console for details.`
      );
      console.error(error);
    }
  };

  render() {
    if (!this.state.web3) {
      return <div>Loading Web3, accounts, and contract...</div>;
    }

    return (
      <div
        className="App"
        style={{
          display: "flex",
          //flex: "none",
          justifyContent: "center",
          alignItems: "center",
          paddingTop: "25px"
          //width: "200vh"
        }}
      >
        <GridList cellHeight="auto" cols={1}>
          <Grid>
            <ContractField
              name="Federation"
              instance={this.state.contract}
              accounts={this.state.accounts}
            ></ContractField>
          </Grid>
          <Grid>
            <Dropzone onDrop={acceptedFiles => console.log(acceptedFiles)}>
              {({ getRootProps, getInputProps }) => (
                <section>
                  <div {...getRootProps()}>
                    <input {...getInputProps()} />
                    <p>
                      Drag 'n' drop some files here, or click to select files
                    </p>
                  </div>
                </section>
              )}
            </Dropzone>
          </Grid>
        </GridList>
      </div>
    );
  }
}
export default App;
