"use client";

import React from "react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
    TooltipItem
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

interface TrendChartProps {
    title: string;
    labels: string[];
    data: number[];
    label: string;
    color?: string;
}

export default function TrendChart({ 
    title, 
    labels, 
    data, 
    label,
    color = "rgb(16, 185, 129)" // Emerald 500
}: TrendChartProps) {
    const chartData = {
        labels,
        datasets: [
            {
                label,
                data,
                borderColor: color,
                backgroundColor: color.replace("rgb", "rgba").replace(")", ", 0.1)"),
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: color,
                pointBorderColor: "#0f172a", // Slate 950
                pointBorderWidth: 2,
                pointHoverRadius: 6,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                backgroundColor: "rgba(15, 23, 42, 0.9)",
                titleColor: "#fff",
                bodyColor: "#94a3b8",
                borderColor: "rgba(51, 65, 85, 0.5)",
                borderWidth: 1,
                padding: 12,
                displayColors: false,
                callbacks: {
                    label: (context: TooltipItem<"line">) => `${label}: ${context.parsed.y ?? ""}`,
                },
            },
        },
        scales: {
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    color: "#64748b",
                    font: {
                        size: 10,
                    },
                },
            },
            y: {
                grid: {
                    color: "rgba(51, 65, 85, 0.2)",
                    drawBorder: false,
                },
                ticks: {
                    color: "#64748b",
                    font: {
                        size: 10,
                    },
                    maxTicksLimit: 5,
                },
            },
        },
    };

    return (
        <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6 h-full">
            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">{title}</h3>
            <div className="h-[250px]">
                <Line data={chartData} options={options} />
            </div>
        </div>
    );
}
