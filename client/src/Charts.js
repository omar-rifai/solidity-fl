import React, { useState, useEffect, useDeepCompareEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";
const Results = ({ datapoints }) => {
  const [result, setResult] = useState();
  // Similar to componentDidMount and componentDidUpdate:
  useEffect(() => {
<<<<<<< Updated upstream
    console.log("charts props:", data.results);
    if (data.length != 0) {
      local_data = data.results;
    }
=======
    console.log("charts props:", datapoints);
    setResult(datapoints);
    console.log("results updated");
>>>>>>> Stashed changes
  });

  return (
    <LineChart
      width={500}
      height={300}
      data={datapoints}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line
        type="monotone"
        dataKey="uv"
        stroke="#8884d8"
        activeDot={{ r: 8 }}
      />
    </LineChart>
  );
};

export default Results;
