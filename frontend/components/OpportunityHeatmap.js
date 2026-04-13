'use client';

import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * OpportunityHeatmap - 彭博风格专业看板组件
 * 功能：展示欧盟各国的补贴力度热力图
 * 视觉风格：深色系、高对比度、商机金
 */
const OpportunityHeatmap = ({ data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    const myChart = echarts.init(chartRef.current, 'dark');
    
    // 模拟欧盟各国补贴强度数据 (强度 0-100)
    const mockData = [
      { name: 'Germany', value: 95 },
      { name: 'France', value: 88 },
      { name: 'Netherlands', value: 92 },
      { name: 'Italy', value: 65 },
      { name: 'Spain', value: 72 },
      { name: 'Poland', value: 58 },
      { name: 'Sweden', value: 84 },
    ];

    const option = {
      backgroundColor: 'transparent',
      title: {
        text: 'EU Subsidy Intensity Map',
        textStyle: { color: '#FFD700', fontSize: 14, fontWeight: 'bold' },
        left: 'center',
        top: 20
      },
      tooltip: {
        trigger: 'item',
        formatter: '{b}: <span style="color:#FFD700;font-weight:bold">{c}</span> (Potential Index)'
      },
      visualMap: {
        min: 0,
        max: 100,
        left: 'left',
        top: 'bottom',
        text: ['High', 'Low'],
        calculable: true,
        inRange: {
          color: ['#1a1a1a', '#450a0a', '#991b1b', '#FF4500', '#FFD700']
        }
      },
      series: [
        {
          name: 'Subsidy Intensity',
          type: 'map',
          map: 'world', // 实际使用时需要加载 GeoJSON
          roam: true,
          emphasis: {
            label: { show: true, color: '#fff' },
            itemStyle: { areaColor: '#FFD700' }
          },
          data: mockData
        }
      ]
    };

    myChart.setOption(option);

    return () => myChart.dispose();
  }, [data]);

  return (
    <div className="relative w-full h-[500px] bg-[#0A0A0A] border border-zinc-800 rounded-lg shadow-2xl overflow-hidden p-4">
      <div className="absolute top-4 left-6 z-10">
        <div className="flex items-center gap-2">
          <span className="flex h-2 w-2 rounded-full bg-amber-400 animate-pulse"></span>
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-widest">Live Market Intelligence</span>
        </div>
      </div>
      <div ref={chartRef} className="w-full h-full" />
    </div>
  );
};

export default OpportunityHeatmap;
