'use client';

import React from 'react';
import { 
  AlertCircle, 
  TrendingUp, 
  ArrowUpRight, 
  Clock 
} from 'lucide-react';

/**
 * ActionableInsights - 彭博风格侧边栏推送组件
 * 功能：实时滚动推送‘涨价预警’或‘获客机会’
 */
const ActionableInsights = ({ insights }) => {
  const mockInsights = insights || [
    { 
      id: 1, 
      type: 'ALERT', 
      title: 'GERMAN HYDROGEN GRID SUBSIDY', 
      desc: 'Article 22a enforcement: 30 days until grant window partial close.', 
      urgent: true 
    },
    { 
      id: 2, 
      type: 'OPPORTUNITY', 
      title: 'SPAIN SOLAR EXEMPTION', 
      desc: 'New tax credits approved for residential storage installers.', 
      urgent: false 
    },
    { 
      id: 3, 
      type: 'PRICE_WARNING', 
      title: 'CBAM CARBON SURGE', 
      desc: 'Phase 2 border adjustments likely to increase costs by 15% in Q3.', 
      urgent: true 
    }
  ];

  return (
    <div className="w-80 h-full bg-[#0F0F0F] border-l border-zinc-800 flex flex-col">
      <div className="p-4 border-b border-zinc-800 bg-[#161616]">
        <h2 className="text-[#FFD700] text-xs font-bold font-mono tracking-tighter flex items-center gap-2">
          <TrendingUp size={14} /> LIVE ACTIONABLE INTELLIGENCE
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar">
        {mockInsights.map((item) => (
          <div 
            key={item.id} 
            className={`p-4 border-b border-zinc-800/50 hover:bg-zinc-900 transition-colors cursor-pointer group`}
          >
            <div className="flex justify-between items-start mb-2">
              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                item.urgent ? 'bg-red-600/20 text-red-500' : 'bg-blue-600/20 text-blue-400'
              }`}>
                {item.type}
              </span>
              <span className="text-[10px] text-zinc-600 flex items-center gap-1">
                <Clock size={10} /> 2m ago
              </span>
            </div>
            
            <h3 className="text-zinc-200 text-sm font-bold leading-tight group-hover:text-amber-400 transition-colors mb-1">
              {item.title}
            </h3>
            
            <p className="text-zinc-500 text-xs line-clamp-2 mb-3">
              {item.desc}
            </p>

            <div className="flex items-center gap-1 text-[10px] text-amber-500 font-bold opacity-0 group-hover:opacity-100 transition-opacity">
              EXECUTE STRATEGY <ArrowUpRight size={12} />
            </div>
          </div>
        ))}
      </div>

      <div className="p-2 border-t border-zinc-800 bg-[#0A0A0A]">
        <div className="flex gap-1">
          <div className="h-1 flex-1 bg-red-600/50"></div>
          <div className="h-1 flex-1 bg-zinc-800"></div>
          <div className="h-1 flex-1 bg-zinc-800"></div>
        </div>
        <p className="text-[9px] text-zinc-600 mt-2 font-mono text-center uppercase">System Healthy // Connection: Secure</p>
      </div>
    </div>
  );
};

export default ActionableInsights;
