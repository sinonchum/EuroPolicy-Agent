'use client';

import React from 'react';
import { 
  Radar, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  ResponsiveContainer 
} from 'recharts';

/**
 * Lead Generation Radar Chart
 * 风格：进攻性、深色背景、科技感发光、商机金 (Commercial Gold)
 */
const OpportunityRadar = ({ data }) => {
  // 模拟数据：展示不同维度的政策红利
  const chartData = data || [
    { subject: 'Subsidy Amount', A: 120, fullMark: 150 },
    { subject: 'Ease of Access', A: 98, fullMark: 150 },
    { subject: 'Urgency', A: 140, fullMark: 150 },
    { subject: 'Geo Advantage', A: 110, fullMark: 150 },
    { subject: 'Market Fit', A: 130, fullMark: 150 },
  ];

  return (
    <div className="w-full h-96 bg-zinc-950 rounded-3xl p-6 border border-zinc-800 shadow-2xl relative overflow-hidden group">
      {/* 进攻性背景装饰 */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-red-900/20 blur-3xl rounded-full -mr-16 -mt-16 group-hover:bg-red-600/30 transition-all duration-700" />
      <div className="absolute bottom-0 left-0 w-32 h-32 bg-amber-900/20 blur-3xl rounded-full -ml-16 -mb-16 group-hover:bg-amber-600/30 transition-all duration-700" />

      <h3 className="text-zinc-400 font-bold text-xs tracking-widest uppercase mb-4 flex items-center gap-2">
        <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
        Live Opportunity Pulse
      </h3>

      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
          <PolarGrid stroke="#27272a" />
          <PolarAngleAxis 
            dataKey="subject" 
            tick={{ fill: '#71717a', fontSize: 10, fontWeight: 600 }}
          />
          <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
          <Radar
            name="Incentive Strength"
            dataKey="A"
            stroke="#fbbf24" /* 商机金 */
            fill="#fbbf24"
            fillOpacity={0.25}
            dot={{ r: 4, fill: '#ef4444' }} /* 警示红 */
          />
        </RadarChart>
      </ResponsiveContainer>
      
      <div className="absolute bottom-4 right-6 text-right">
        <p className="text-[10px] text-zinc-600 font-mono">SCANNING EU DIRECTIVES v2.4</p>
        <p className="text-xs font-bold text-amber-500">AGGRESSIVE GROWTH DETECTED</p>
      </div>
    </div>
  );
};

export default OpportunityRadar;
