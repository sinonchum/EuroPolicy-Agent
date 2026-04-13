'use client';

import React from 'react';
import useStore from '../store/useStore';

/**
 * PulseTicker - 全球能源快讯滚动条
 * 风格：股票交易机 (Ticker), 极简, 动态
 */
const PulseTicker = () => {
  const { pulseTicker } = useStore();
  
  const displayMessages = pulseTicker.length > 0 ? pulseTicker : [
    "🛰️ [GEP] Scanning global energy signals...",
    "🛡️ [Security] Decoupled Zero-Ops Architecture Active.",
    "🌐 [i18n] Multi-language support enabled: EN/ZH/FR/DE"
  ];

  return (
    <div className="w-full bg-[#050505] border-y border-zinc-800 overflow-hidden py-2 select-none">
      <div className="flex animate-marquee whitespace-nowrap">
        {[...displayMessages, ...displayMessages].map((msg, idx) => (
          <span 
            key={idx} 
            className="text-[10px] font-mono font-bold mx-8 tracking-widest text-zinc-400 flex items-center gap-2"
          >
            <span className="w-1.5 h-1.5 bg-amber-500 rounded-full shadow-[0_0_5px_#f59e0b]" />
            {msg}
          </span>
        ))}
      </div>
      
      <style jsx>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-marquee {
          display: inline-flex;
          animation: marquee 40s linear infinite;
        }
      `}</style>
    </div>
  );
};

export default PulseTicker;
