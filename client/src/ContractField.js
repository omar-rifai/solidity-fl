import React, { useEffect, useState } from "react";
import { TextField, Button } from "@material-ui/core/";
import Grid from "@material-ui/core/Grid";
import CardContent from "@material-ui/core/CardContent";
import Box from "@material-ui/core/Box";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Chart from "./Charts";

let results = [];
let params = [];

const useStyles = makeStyles({
  root: {
    maxWidth: 400
  },
  title: {
    fontSize: 20
  }
});

async function initializeState(e, contract, accounts) {
  await fetch("/init")
    .then(res => res.json())
    .then(data => {
      console.log(data);
    })
    .catch(console.log);
}

async function simulateLocal(e, contract, accounts, setState, count) {
  //e.preventDefault();
  console.log("Local stochastic gradient descent");

  await contract.methods.resetState().send({ gas: 5000000, from: accounts[0] });

  await fetch("/run_stage")
    .then(res => res.json())
    .then(data => {
      params = data;
    })
    .catch(console.log);
  console.log(contract);
  await fetch("/get_results")
    .then(res => res.json())
    .then(data => {
      if(results.length==0){
        let key = Object.key
        let datas = Object.values(data);
        for(var k in datas){
          results.push(datas[k]);
        }
      }
      else{
        results = results.concat(Object.values(data));
      }
    });
    console.log(results);
  setState(count + 1);
}

async function simulateFederated(e, contract, accounts) {
  e.preventDefault();
  console.log("Federation happening.");
  console.log(params);

  for (var i = 0; i < 4; i++) {
    await contract.methods
      .store_params(params.weights[i])
      .send({ from: accounts[i + 1], gas: 5000000 });
  }

  const aggres = await contract.methods
    .run_agg()
    .send({ gas: 5000000, from: accounts[0] });
  console.log("runagg:" + aggres);

  const weight_res = await contract.methods
    .read_params()
    .call({ gas: 500000000, from: accounts[0] });
  console.log(weight_res);

  for (var i = 0; i < 4; i++) {
    await contract.methods
      .store_params(params.biases[i])
      .send({ from: accounts[i + 1], gas: 5000000 });
  }

  const aggres2 = await contract.methods
    .run_agg()
    .send({ gas: 500000000, from: accounts[0] });
  console.log("runagg:" + aggres2);

  const bias_res = await contract.methods
    .read_params()
    .call({ gas: 500000000, from: accounts[0] });
  console.log(bias_res);

  let postres = [];

  await fetch("/post_params", {
    method: "POST",
    body: JSON.stringify({
      weights: JSON.stringify(weight_res),
      biases: JSON.stringify(bias_res)
    })
  })
    .then(res => res.json())
    .then(data => {
      postres = data;
    });
  console.log(postres);
}

const ClientField = props => {
  let [count, setState] = useState();
  const classes = useStyles();

  return (
    <Box border={0} borderColor="grey.500">
      <CardContent>
        <Typography className={classes.header} variant="h6">
          Simulation Panel
        </Typography>
      </CardContent>

      <CardContent>
        <Button
          variant="contained"
          size="small"
          style={{
            maxWidth: "100px",
            maxHeight: "30px",
            minWidth: "100px",
            minHeight: "30px",
            margin: "10px"
          }}
          onClick={e =>
            simulateLocal(e, props.instance, props.accounts, setState, count)
          }
        >
          Run Local
        </Button>

        <Button
          variant="contained"
          size="small"
          style={{
            maxWidth: "100px",
            maxHeight: "30px",
            minWidth: "100px",
            minHeight: "30px",
            margin: "10px"
          }}
          onClick={e => simulateFederated(e, props.instance, props.accounts)}
        >
          Federate
        </Button>

        <Button
          variant="contained"
          size="small"
          style={{
            maxWidth: "100px",
            maxHeight: "30px",
            minWidth: "100px",
            minHeight: "30px",
            margin: "10px"
          }}
          onClick={e => initializeState(e, props.instance, props.accounts)}
        >
          Initialize
        </Button>
      </CardContent>
      <CardContent
        style={{
          margin: "auto",
          minHeight: "300px",
          maxHeight: "300px",
          maxWidth: "400px"
        }}
      >
        <Chart data={results} count={count}></Chart>
      </CardContent>
    </Box>
  );
};

export default ClientField;
