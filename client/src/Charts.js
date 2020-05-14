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
let local_data = [{}];
const Results = ({ data, count }) => {
  // Similar to componentDidMount and componentDidUpdate:

  useEffect(() => {
    console.log("charts props:", data);
    if (data.length != 0) {
      local_data = data[0];
    }
  });

  return (
    <LineChart
      width={500}
      height={300}
      data={data[0]}
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
