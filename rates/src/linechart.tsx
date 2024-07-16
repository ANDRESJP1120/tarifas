import React from 'react';
import { Line } from 'react-chartjs-2';

interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    fill: boolean;
  }[];
}

interface Props {
  data: { periodo: string; tarifa: number }[];
}

const LineChart: React.FC<Props> = ({ data }) => {
  const chartData: ChartData = {
    labels: data.map(entry => entry.periodo),
    datasets: [
      {
        label: 'Tarifa Cu Liq',
        data: data.map(entry => entry.tarifa),
        borderColor: '#461E7D',
        fill: false,
      },
    ],
  };

  return <Line data={chartData} />;
};

export default LineChart;
