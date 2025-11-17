import React from "react";
import { Line, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Card } from "react-bootstrap";
import "./ChartComponent.css";

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const ChartComponent = ({ data, type = "line", title }) => {
  if (!data || !data.labels || data.labels.length === 0) {
    return (
      <Card className="chart-card">
        <Card.Body>
          <p className="text-muted">No chart data available</p>
        </Card.Body>
      </Card>
    );
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
        labels: {
          font: {
            size: 12,
            family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          },
        },
      },
      title: {
        display: !!title,
        text: title,
        font: {
          size: 16,
          weight: "bold",
          family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        },
      },
      tooltip: {
        backgroundColor: "rgba(0, 0, 0, 0.8)",
        padding: 12,
        titleFont: {
          size: 14,
        },
        bodyFont: {
          size: 13,
        },
        cornerRadius: 6,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: "rgba(0, 0, 0, 0.05)",
        },
        ticks: {
          font: {
            size: 11,
          },
        },
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          font: {
            size: 11,
          },
        },
      },
    },
  };

  // Ensure datasets have proper structure
  const chartData = {
    labels: data.labels,
    datasets: data.datasets.map((dataset, index) => ({
      ...dataset,
      fill: type === "line" ? true : false,
      tension: 0.4,
      borderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
      pointBackgroundColor: dataset.borderColor || "#ffffff",
      pointBorderColor: dataset.borderColor || "#000000",
      pointHoverBackgroundColor: dataset.borderColor || "#ffffff",
      pointHoverBorderColor: dataset.borderColor || "#000000",
    })),
  };

  return (
    <Card className="chart-card">
      <Card.Body>
        <div className="chart-container">
          {type === "line" ? (
            <Line data={chartData} options={options} />
          ) : (
            <Bar data={chartData} options={options} />
          )}
        </div>
      </Card.Body>
    </Card>
  );
};

export default ChartComponent;
