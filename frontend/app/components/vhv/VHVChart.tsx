"use client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  ChartOptions,
  TooltipItem,
} from "chart.js";
import { Bar, Doughnut } from "react-chartjs-2";
import { motion } from "framer-motion";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface VHVChartProps {
  timeContribution: number;
  lifeContribution: number;
  resourceContribution: number;
  type?: "bar" | "doughnut";
}

export default function VHVChart({
  timeContribution,
  lifeContribution,
  resourceContribution,
  type = "bar",
}: VHVChartProps) {
  const data = {
    labels: ["Tiempo (T)", "Vida (V)", "Recursos (R)"],
    datasets: [
      {
        label: "Contribución (Maxos)",
        data: [timeContribution, lifeContribution, resourceContribution],
        backgroundColor: [
          "rgba(255, 107, 107, 0.7)", // Coral for Time
          "rgba(46, 204, 113, 0.7)",  // Green for Life
          "rgba(139, 69, 19, 0.7)",   // Brown for Resources
        ],
        borderColor: [
          "rgba(255, 107, 107, 1)",
          "rgba(46, 204, 113, 1)",
          "rgba(139, 69, 19, 1)",
        ],
        borderWidth: 2,
        borderRadius: 8,
      },
    ],
  };

  const options: ChartOptions<"bar" | "doughnut"> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: type === "doughnut",
        position: "bottom" as const,
        labels: {
          color: "rgba(255, 255, 255, 0.7)",
          font: {
            family: "Inter, sans-serif",
          },
        },
      },
      tooltip: {
        backgroundColor: "rgba(15, 15, 15, 0.9)",
        titleFont: { size: 14, family: "Inter, sans-serif" },
        bodyFont: { size: 13, family: "Inter, sans-serif" },
        padding: 12,
        cornerRadius: 8,
        displayColors: false,
        callbacks: {
          label: (context: TooltipItem<"bar" | "doughnut">) => `${context.formattedValue} Ⓜ`,
        },
      },
    },
    scales: type === "bar" ? {
      y: {
        beginAtZero: true,
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
        ticks: {
          color: "rgba(255, 255, 255, 0.5)",
          callback: (value) => `${value} Ⓜ`,
        },
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: "rgba(255, 255, 255, 0.7)",
        },
      },
    } : undefined,
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="w-full h-64 md:h-80"
    >
      {type === "bar" ? (
        <Bar data={data} options={options as ChartOptions<"bar">} />
      ) : (
        <Doughnut data={data} options={options as ChartOptions<"doughnut">} />
      )}
    </motion.div>
  );
}
