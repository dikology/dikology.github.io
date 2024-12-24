import React from 'react';
import { Bar } from 'react-chartjs-2';

export default function Charts({ chartData }) {
  const data = {
    labels: Object.keys(chartData).map(month => `Month ${month}`),
    datasets: [
      {
        label: 'Files Created',
        data: Object.values(chartData),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  return <Bar data={data} />;
}
