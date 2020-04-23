import React from "react";
import { TextField, Button } from "@material-ui/core/";
import Grid from "@material-ui/core/Grid";
import CardContent from "@material-ui/core/CardContent";
import Box from "@material-ui/core/Box";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles({
  root: {
    maxWidth: 400
  },
  title: {
    fontSize: 20
  }
});

function handleTextFieldChange(e) {
  this.setState({
    textFieldValue: e.target.value
  });
}
async function simulateLocal(e, contract, accounts) {
  e.preventDefault();
  console.log("Storage action.");
  console.log("before read params");
  let params = await contract.methods
    .read_params()
    .call({ data: "test data field" });
  console.log(params);
  console.log("after read_params in run example");

  // Stores a given value, 5 by default.
  /*await contract.methods
    .store_params([
      [
        [2, 3],
        [1, 2]
      ]
    ])
    .send({ from: accounts[0], gas: 3000000 });
  console.log("Client 0 stored parameters [[2,3],[1,2]]");
  await contract.methods
    .store_params([
      [
        [20, 30],
        [11, 200]
      ]
    ])
    .send({ from: accounts[1], gas: 3000000 });*/
  console.log("Client 1 stored parameters [[20,30],[11,200]]");
}

async function handleDisplay(e, contract, accounts) {
  e.preventDefault();
  console.log("Display action");
  const res_array = await contract.methods.read_params().call();
  let val1 = res_array[0][0] / 1e9;
  let val2 = res_array[0][1] / 1e9;
  let val3 = res_array[1][0] / 1e9;
  let val4 = res_array[1][1] / 1e9;
  const response = val1 + " " + val2 + " " + val3 + " " + val4;
  console.log(res_array);
}
async function simulateFederated(e, contract, accounts) {
  e.preventDefault();
  console.log("Federation happening.");
  // Get the value from the contract to prove it worked.
  await contract.methods.run_agg().send({ from: accounts[3], gas: 3000000 });
}

function ClientField(props) {
  console.log(props);
  const classes = useStyles();
  return (
    <Box border={1} borderColor="grey.500">
      <Grid container>
        <Grid item>
          <CardContent>
            <Typography className={classes.header} variant="h6">
              Simulation Panel
            </Typography>
          </CardContent>

          <Grid item style={{ textAlign: "center" }}>
            <CardContent>
              <Button
                variant="contained"
                size="small"
                style={{
                  maxWidth: "100px",
                  maxHeight: "40px",
                  minWidth: "100px",
                  minHeight: "40px"
                }}
                onClick={e => simulateLocal(e, props.instance, props.accounts)}
              >
                Simulate Local
              </Button>
            </CardContent>
            <CardContent>
              <Button
                variant="contained"
                size="small"
                style={{
                  maxWidth: "100px",
                  maxHeight: "40px",
                  minWidth: "100px",
                  minHeight: "40px"
                }}
                onClick={e =>
                  simulateFederated(e, props.instance, props.accounts)
                }
              >
                Simulate Federated
              </Button>
            </CardContent>
            <CardContent>
              <Button
                variant="contained"
                style={{
                  maxWidth: "100px",
                  maxHeight: "40px",
                  minWidth: "100px",
                  minHeight: "40px"
                }}
                onClick={e => handleDisplay(e, props.instance, props.accounts)}
              >
                Submit Data
              </Button>
            </CardContent>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
}

export default ClientField;
