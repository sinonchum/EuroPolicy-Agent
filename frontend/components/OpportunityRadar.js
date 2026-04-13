'use client';

import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import useStore from '../store/useStore';

/**
 * OpportunityRadar - 政策红利热力矩阵 (平面树图，节省 8G RAM 显存)
 */
const OpportunityRadar = ({ data }) => {
    const chartRef = useRef(null);
    const { setSelectedCountry } = useStore();

    useEffect(() => {
        if (!chartRef.current) return;
        const myChart = echarts.init(chartRef.current, 'dark');

        const option = {
            backgroundColor: 'transparent',
            tooltip: {},
            series: [{
                name: 'Policy Dividend Index',
                type: 'treemap',
                visibleMin: 300,
                data: [
                    { name: 'Germany', value: 95, itemStyle: { color: '#B91C1C' } },
                    { name: 'France', value: 82, itemStyle: { color: '#991B1B' } },
                    { name: 'Spain', value: 75, itemStyle: { color: '#881337' } },
                    { name: 'Netherlands', value: 88, itemStyle: { color: '#7C2D12' } },
                ],
                label: {
                    show: true,
                    formatter: '{b}\n{c}',
                    fontSize: 12,
                    fontFamily: 'monospace'
                },
                breadcrumb: { show: false },
                itemStyle: {
                    borderColor: '#0A0A0A',
                    borderWidth: 2,
                    gapWidth: 1
                }
            }]
        };

        myChart.setOption(option);

        // 点击交互逻辑
        myChart.on('click', (params) => {
            if (params.data && params.data.name) {
                console.log("🔗 [UI] 联动选择国家:", params.data.name);
                setSelectedCountry(params.data.name);
            }
        });

        return () => myChart.dispose();
    }, [data]);

    return (
        <div className="w-full h-full bg-[#0A0A0A] border border-zinc-800 rounded-xl overflow-hidden p-4">
            <h3 className="text-[#FFD700] text-xs font-mono font-bold uppercase mb-4 tracking-tighter">
                EU Policy Arbitrage Heat-Map
            </h3>
            <div ref={chartRef} className="w-full h-full min-h-[300px]" />
        </div>
    );
};

export default OpportunityRadar;
