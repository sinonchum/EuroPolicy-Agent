'use client';

import React from 'react';
import { AlertTriangle, TrendingDown, ArrowRight } from 'lucide-react';

/**
 * ImpactAlert - 权重重大变更警告组件
 * 风格：高优先级、警示红、动态闪烁
 */
const ImpactAlert = ({ originalScore, newScore, reason }) => {
  if (!newScore || newScore >= originalScore) return null;

  const dropPercentage = Math.round((1 - newScore / originalScore) * 100);

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 animate-bounce">
      <div className="bg-red-950/90 border-2 border-red-600 backdrop-blur-md px-6 py-4 rounded-2xl shadow-[0_0_30px_rgba(220,38,38,0.3)] flex items-center gap-6 max-w-lg">
        <div className="bg-red-600 p-2 rounded-lg">
          <AlertTriangle className="text-white" size={24} />
        </div>
        
        <div className="flex-1">
          <h4 className="text-white font-bold text-sm tracking-tight leading-none mb-1">
            CRITICAL OPPORTUNITY DOWNGRADE
          </h4>
          <p className="text-red-400 text-xs font-medium">
            Global market signals detected a {dropPercentage}% valuation drop.
          </p>
        </div>

        <div className="flex items-center gap-3 bg-black/40 px-3 py-2 rounded-xl border border-red-900/50">
          <span className="text-zinc-500 text-xs line-through font-mono">{originalScore}</span>
          <ArrowRight size={14} className="text-white" />
          <span className="text-red-500 text-lg font-black font-mono">{newScore}</span>
        </div>
      </div>
    </div>
  );
};

export default ImpactAlert;
