'use client';

import React from 'react';
import useStore from '../store/useStore';
import { Target, Zap, ShieldAlert } from 'lucide-react';

const LeadCardList = () => {
    const { opportunities, isLoading } = useStore();

    if (isLoading) return <div className="text-zinc-600 font-mono text-xs p-8">RE-CALIBRATING AGENT WEGHTS...</div>;

    return (
        <div className="flex flex-col gap-3">
            {opportunities.map((opp) => (
                <div key={opp.id} className="bg-[#111111] border border-zinc-800 p-4 rounded-lg hover:border-amber-500/50 transition-all group">
                    <div className="flex justify-between items-start mb-2">
                        <h4 className="text-[#FFD700] text-sm font-black font-mono tracking-tight group-hover:underline">
                            {opp.title}
                        </h4>
                        <div className="flex items-center gap-2">
                             <span className="text-[10px] font-mono text-zinc-500 uppercase">{opp.urgency}</span>
                             <div className="bg-amber-500/10 text-[#FFD700] px-2 py-0.5 rounded text-[11px] font-black border border-amber-500/30">
                                {opp.score}
                             </div>
                        </div>
                    </div>

                    <div className="flex gap-4 mb-3">
                        <div className="flex items-center gap-1.5 text-[10px] text-zinc-400">
                            <Target size={12} /> <span className="uppercase">{opp.target_sector}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-[10px] text-zinc-400">
                            <Zap size={12} /> <span className="uppercase">{opp.subsidy_type}</span>
                        </div>
                    </div>

                    <div className="bg-zinc-950/50 border-l-2 border-red-600 p-3 rounded-r">
                        <p className="text-[#E0E0E0] text-xs leading-relaxed italic">
                            <span className="text-red-500 font-bold not-italic font-mono mr-1">ACTION:</span>
                            {opp.sales_pitch}
                        </p>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default LeadCardList;
