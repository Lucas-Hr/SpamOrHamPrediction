'use client'
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// Register the necessary components from Chart.js
ChartJS.register(ArcElement, Tooltip, Legend);

type DoughnutChartProps = {
    spam : number;
    ham : number;
};

const DoughnutChart = ({spam , ham} : DoughnutChartProps) => {
  // Define your data
  const data = {
    labels: ['Ham', 'Spam',],
    datasets: [
      {
        // label: '# of Votes',
        data: [spam, ham],
        backgroundColor: [
            'rgba(62, 178, 255, 1)',
          'rgba(255, 41, 87, 1)',
        ],
        borderColor: [
            'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  // Define chart options (e.g., responsiveness, plugins)
  const options = {
    responsive: true,
    maintainAspectRatio: false, // Allows you to control size with parent container
    plugins: {
      legend: {
        position: 'top' as const, // Position the legend at the top
      },
      title: {
        display: true,
        text: 'Sample Doughnut Chart',
      },
    },
    cutout: '60%', // Adjust the size of the hole for a doughnut effect
  } as const;

  return (
     <div className="bg-white px-10 rounded-lg shadow-md border border-gray-200 py-8 h-75">
      <Doughnut data={data} options={options}  />
    </div>
  );
};

export default DoughnutChart;
